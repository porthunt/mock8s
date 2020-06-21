from kubernetes.client.api import CoreV1Api
from mock8s.client.models.mock_v1_service_list import MockV1ServiceList
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
        self._services_items = set()

    def __label_in_service(self, service, label_selector):
        if service.metadata.labels:
            labels = [
                "{}={}".format(key, value)
                for key, value in service.metadata.labels.items()
            ]
            for label in labels:
                if label_selector in label:
                    return True

        return False

    def __field_in_service(self, service, field_selector):
        if service.spec.selector:
            selectors = [
                "{}={}".format(key, value)
                for key, value in service.spec.selector.items()
            ]
            for selector in selectors:
                if field_selector in selector:
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
                    if self.__label_in_service(
                        service, label_selector
                    ) and self.__field_in_service(service, field_selector):
                        services.append(service)
                elif label_selector:
                    if self.__label_in_service(service, label_selector):
                        services.append(service)
                elif field_selector:
                    if self.__field_in_service(service, field_selector):
                        services.append(service)

        return MockV1ServiceList(items=services)

    def create_namespaced_service(self, namespace, body, **kwargs):
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

    def delete_namespaced_service(self, name, namespace, **kwargs):
        if namespace not in self._namespaced_services_items.keys():
            raise ApiException(404, "Not Found")

        for service in self._services_items:
            if service.metadata.name == name:
                self._services_items.remove(service)
                self._namespaced_services_items[namespace].remove(service)
                break
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
                    if self.__label_in_service(
                        service, label_selector
                    ) and self.__field_in_service(service, field_selector):
                        services.append(service)
                elif label_selector:
                    if self.__label_in_service(service, label_selector):
                        services.append(service)
                elif field_selector:
                    if self.__field_in_service(service, field_selector):
                        services.append(service)

        return MockV1ServiceList(items=services)

    def read_namespaced_service(self, name, namespace, **kwargs):
        if namespace not in self._namespaced_services_items:
            raise ApiException(404, "Not Found")

        for service in self._namespaced_services_items[namespace]:
            if service.metadata.name == name:
                return service
        else:
            raise ApiException(404, "Not Found")

    def patch_namespaced_service(self, name, namespace, body, **kwargs):
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

    def replace_namespaced_service(self, name, namespace, body, **kwargs):
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
