from kubernetes.client.rest import ApiException

from mock8s.core.resources.services import Services


class MockCoreV1Api:
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ""

        self.api_client = api_client

        self.services = Services()
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

        if not field_selector.startswith(
            "metadata.name"
        ) and not field_selector.startswith("metadata.namespace"):
            raise ApiException(400, "Bad Request")

        selector_name = "metadata.name={}".format(resource.metadata.name)
        selector_namespace = "metadata.namespace={}".format(
            resource.metadata.namespace
        )

        if (
            field_selector == selector_name
            or field_selector == selector_namespace
        ):
            return True

        return False

    def list_service_for_all_namespaces(self, **kwargs):
        return self.services.list_all(**kwargs)

    # SERVICES

    def create_namespaced_service(self, namespace, body, **kwargs):
        return self.services.create(namespace, body, **kwargs)

    def read_namespaced_service(self, name, namespace, **kwargs):
        return self.services.read(name, namespace, **kwargs)

    def list_namespaced_service(self, namespace, **kwargs):
        return self.services.list(namespace, **kwargs)

    def patch_namespaced_service(self, name, namespace, body, **kwargs):
        return self.services.patch(name, namespace, body, **kwargs)

    def replace_namespaced_service(self, name, namespace, body, **kwargs):
        return self.services.replace(name, namespace, body, **kwargs)

    def delete_namespaced_service(self, name, namespace, **kwargs):
        return self.services.delete(name, namespace, **kwargs)

    # PODS

    def create_namespaced_pod(self, namespace, body, **kwargs):
        return self.pods.create(namespace, body, **kwargs)

    def read_namespaced_pod(self, name, namespace, **kwargs):
        return self.pods.read(name, namespace, **kwargs)

    def list_namespaced_pod(self, namespace, **kwargs):
        return self.pods.list_all(namespace, **kwargs)

    def patch_namespaced_pod(self, name, namespace, body, **kwargs):
        return self.pods.patch(name, namespace, body, **kwargs)

    def replace_namespaced_pod(self, name, namespace, body, **kwargs):
        return self.pods.replace(name, namespace, body, **kwargs)

    def delete_namespaced_pod(self, name, namespace, **kwargs):
        return self.pods.delete(name, namespace, **kwargs)

    # POD LOGS

    def read_namespaced_pod_log(self, name, namespace, **kwargs):
        pass
