import copy
from mock8s.core.resources import Resources
from mock8s.client.models.mock_v1_service import MockV1Service
from kubernetes.client.models.v1_service_list import V1ServiceList
from kubernetes.client.models.v1_service_spec import V1ServiceSpec
from kubernetes.client.models.v1_service_status import V1ServiceStatus


class Services(Resources):
    def __init__(self):
        super().__init__()

    def create(self, namespace: str, body: MockV1Service, **kwargs):
        if not body:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_service`"
            )

        body = copy.copy(body)
        body.spec = V1ServiceSpec(**body.spec)
        body.status = V1ServiceStatus(**body.status)
        try:
            return super().create(namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_service`"
            )

    def read(self, name: str, namespace: str, **kwargs):
        return super().read(name, namespace, **kwargs)

    def list_all(self, **kwargs):
        services = super().list_all(**kwargs)
        return V1ServiceList(items=services)

    def list(self, namespace: str, **kwargs):
        services = super().list(namespace, **kwargs)
        return V1ServiceList(items=services)

    def patch(self, name: str, namespace: str, body: MockV1Service, **kwargs):
        try:
            return super().patch(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `patch_namespaced_service`"
            )

    def replace(
        self, name: str, namespace: str, body: MockV1Service, **kwargs
    ):
        try:
            return super().replace(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `replace_namespaced_service`"
            )

    def delete(self, name: str, namespace: str, **kwargs):
        return super().delete(name, namespace, **kwargs)
