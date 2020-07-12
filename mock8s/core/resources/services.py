from mock8s.core.resources import Resources
from mock8s.client.models.mock_v1_service import MockV1Service
from mock8s.client.models.mock_v1_service_list import MockV1ServiceList


class Services(Resources):
    def __init__(self):
        super().__init__()

    def create(self, namespace: str, body: MockV1Service, **kwargs):
        return super().create(namespace, body, **kwargs)

    def read(self, name: str, namespace: str, **kwargs):
        return super().read(name, namespace, **kwargs)

    def list_all(self, **kwargs):
        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        services = []

        if not label_selector and not field_selector:
            services = self._items
        else:
            for service in self._items:
                if label_selector and field_selector:
                    if self._label_in_resource(
                        service, label_selector
                    ) and self._field_in_resource(service, field_selector):
                        services.append(service)
                elif label_selector:
                    if self._label_in_resource(service, label_selector):
                        services.append(service)
                elif field_selector:
                    if self._field_in_resource(service, field_selector):
                        services.append(service)

        return MockV1ServiceList(items=services)

    def list(self, namespace: str, **kwargs):
        services = super().list(namespace, **kwargs)
        return MockV1ServiceList(items=services)

    def patch(self, name: str, namespace: str, body: MockV1Service, **kwargs):
        return super().patch(name, namespace, body, **kwargs)

    def replace(
        self, name: str, namespace: str, body: MockV1Service, **kwargs
    ):
        return super().replace(name, namespace, body, **kwargs)

    def delete(self, name: str, namespace: str, **kwargs):
        return super().delete(name, namespace, **kwargs)
