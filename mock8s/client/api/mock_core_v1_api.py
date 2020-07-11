from kubernetes.client.api import CoreV1Api
from mock8s.client.models.mock_v1_service_list import MockV1ServiceList
from mock8s.client.models.mock_v1_pod_list import MockV1PodList
from mock8s.client.models.mock_v1_api_service import MockV1APIService
from mock8s.client.models.mock_v1_object_meta import MockV1ObjectMeta
from mock8s.client.models.mock_v1_service_status import MockV1ServiceStatus
from mock8s.client.models.mock_v1_service_spec import MockV1ServiceSpec
from kubernetes.client.rest import ApiException


class MockCoreV1Api:
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ""

        self.api_client = api_client

        self._namespaced_services_items = {"default": set()}
        self._namespaced_pods_items = {"default": set()}
        self._services_items = set()
        self._pods_items = set()

    @staticmethod
    def __label_in_resource(resource, label_selector):
        if resource.metadata.labels:
            labels = [
                "{}={}".format(key, value)
                for key, value in resource.metadata.labels.items()
            ]
            for label in labels:
                if label_selector.startswith(label):
                    return True

        return False

    @staticmethod
    def __field_in_resource(resource, field_selector):
        if not field_selector:
            return False

        if not field_selector.startswith("metadata.name") and \
                not field_selector.startswith("metadata.namespace"):
            raise ApiException(400, "Bad Request")

        selector_name = "metadata.name={}".format(resource.metadata.name)
        selector_namespace = "metadata.namespace={}".format(
            resource.metadata.namespace
        )

        if field_selector == selector_name or \
                field_selector == selector_namespace:
            return True

        return False

    def list_service_for_all_namespaces(self, **kwargs):
        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        services = []

        if not label_selector and not field_selector:
            services = self._services_items
        else:
            for service in self._services_items:
                if label_selector and field_selector:
                    if self.__label_in_resource(
                        service, label_selector
                    ) and self.__field_in_resource(service, field_selector):
                        services.append(service)
                elif label_selector:
                    if self.__label_in_resource(service, label_selector):
                        services.append(service)
                elif field_selector:
                    if self.__field_in_resource(service, field_selector):
                        services.append(service)

        return MockV1ServiceList(items=services)

    # SERVICES

    def create_namespaced_service(self, namespace, body, **kwargs):  # noqa
        _metadata = body.get("metadata")
        _metadata["namespace"] = namespace
        service = MockV1APIService(
            api_version=body.get("apiVersion"),
            kind=body.get("kind"),
            metadata=_metadata,
            spec=body.get("spec"),
            status=body.get("status", {}),
        )

        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        self._services_items.add(service)
        self._namespaced_services_items[namespace].add(service)
        return service

    def read_namespaced_service(self, name, namespace, **kwargs):  # noqa
        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        for service in self._namespaced_services_items[namespace]:
            if service.metadata.name == name:
                return service
        else:
            raise ApiException(404, "Not Found")

    def list_namespaced_service(self, namespace, **kwargs):
        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        services = []

        if not label_selector and not field_selector:
            services = self._namespaced_services_items[namespace]
        else:
            for service in self._namespaced_services_items[namespace]:
                if label_selector and field_selector:
                    if self.__label_in_resource(
                        service, label_selector
                    ) and self.__field_in_resource(service, field_selector):
                        services.append(service)
                elif label_selector:
                    if self.__label_in_resource(service, label_selector):
                        services.append(service)
                elif field_selector:
                    if self.__field_in_resource(service, field_selector):
                        services.append(service)

        return MockV1ServiceList(items=services)

    def patch_namespaced_service(self, name, namespace, body, **kwargs):  # noqa
        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        for service in self._namespaced_services_items[namespace]:
            if service.metadata.name == name:
                self._namespaced_services_items[namespace].remove(service)
                self._services_items.remove(service)
                break
        else:
            raise ApiException(404, "Not Found")

        if "metadata" in body:
            service.metadata = MockV1ObjectMeta(**body["metadata"])

        if "spec" in body:
            service.spec = MockV1ServiceSpec(**body["spec"])

        if "status" in body:
            service.status = MockV1ServiceStatus(**body["status"])

        self._namespaced_services_items[namespace].add(service)
        self._services_items.add(service)
        return service

    def replace_namespaced_service(self, name, namespace, body, **kwargs):  # noqa
        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        for service in self._namespaced_services_items[namespace]:
            if service.metadata.name == name:
                self._namespaced_services_items[namespace].remove(service)
                self._services_items.remove(service)
                break
        else:
            raise ApiException(404, "Not Found")

        return self.create_namespaced_service(namespace, body)

    def delete_namespaced_service(self, name, namespace, **kwargs):  # noqa
        if namespace not in self._namespaced_services_items.keys():
            raise ApiException(404, "Not Found")

        for service in self._services_items:
            if service.metadata.name == name:
                self._services_items.remove(service)
                self._namespaced_services_items[namespace].remove(service)
                break
        else:
            raise ApiException(404, "Not Found")

    # PODS

    def create_namespaced_pod(self, namespace, body, **kwargs):
        pass

    def read_namespaced_pod(self, name, namespace, **kwargs):  # noqa
        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        for pod in self._namespaced_pods_items[namespace]:
            if pod.metadata.name == name:
                return pod
        else:
            raise ApiException(404, "Not Found")

    def list_namespaced_pod(self, namespace, **kwargs):
        if namespace not in self._namespaced_pods_items:
            raise ApiException(404, "Not Found")

        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        pods = []

        if not label_selector and not field_selector:
            pods = self._namespaced_pods_items[namespace]
        else:
            for pod in self._namespaced_pods_items[namespace]:
                if label_selector and field_selector:
                    if self.__label_in_resource(
                            pod, label_selector
                    ) and self.__field_in_resource(pod, field_selector):
                        pods.append(pod)
                elif label_selector:
                    if self.__label_in_resource(pod, label_selector):
                        pods.append(pod)
                elif field_selector:
                    if self.__field_in_resource(pod, field_selector):
                        pods.append(pod)

        return MockV1PodList(items=pods)

    def patch_namespaced_pod(self, name, namespace, body, **kwargs):
        pass

    def replace_namespaced_pod(self, name, namespace, body, **kwargs):
        pass

    def delete_namespaced_pod(self, name, namespace, **kwargs):  # noqa
        if namespace not in self._namespaced_pods_items.keys():
            raise ApiException(404, "Not Found")

        for pod in self._pods_items:
            if pod.metadata.name == name:
                self._pods_items.remove(pod)
                self._namespaced_pods_items[namespace].remove(pod)
                break
        else:
            raise ApiException(404, "Not Found")

    # POD LOGS

    def read_namespaced_pod_log(self, name, namespace, **kwargs):
        pass
