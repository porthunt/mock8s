from kubernetes.client.api import CoreV1Api
from mock8s.client.models.mock_v1_service_list import MockV1ServiceList
from mock8s.client.models.mock_v1_api_service import MockV1APIService


class MockCoreV1Api:
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ""
        self.api_client = api_client
        self.namespaced_items = {}
        self._items = set()

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

    def list_service_for_all_namespaces(self, **kwargs):
        label_selector = kwargs.get("label_selector")

        if label_selector:
            services = []
            for service in self._items:
                if self.__label_in_service(service, label_selector):
                    services.append(service)
        else:
            services = self._items

        return MockV1ServiceList(items=services)

    def create_namespaced_service(self, namespace, body, **kwargs):
        _metadata = body.get("metadata")
        _metadata["namespace"] = namespace
        service = MockV1APIService(
            api_version=body.get("apiVersion"),
            kind=body.get("kind"),
            metadata=_metadata,
            spec=body.get("spec"),
            status=body.get("status", {})
        )
        self._items.add(service)
        if namespace in self.namespaced_items:
            self.namespaced_items[namespace].add(service)
        else:
            self.namespaced_items[namespace] = {service}
        return service

    def delete_namespaced_service(self, name, namespace, **kwargs):
        for service in self._items:
            if service.metadata.name == name:
                self._items.remove(service)
                self.namespaced_items[namespace].remove(service)
                break

    def list_namespaced_service(self, namespace, **kwargs):
        if namespace in self.namespaced_items:
            return MockV1ServiceList(items=self.namespaced_items[namespace])

    def patch_namespaced_service(self, name, namespace, body, **kwargs):
        pass

    def read_namespaced_service(self, name, namespace, **kwargs):
        pass

    def replace_namespaced_service(self, name, namespace, body, **kwargs):
        pass
