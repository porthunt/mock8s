import copy
from mock8s.core.resources import Resources
from mock8s.client.models.mock_v1_ingress import MockV1Ingress
from kubernetes.client.models.networking_v1beta1_ingress_list import (
    NetworkingV1beta1IngressList,
)
from kubernetes.client.models.networking_v1beta1_ingress_spec import (
    NetworkingV1beta1IngressSpec,
)
from kubernetes.client.models.networking_v1beta1_ingress_status import (
    NetworkingV1beta1IngressStatus,
)


class Ingresses(Resources):
    def __init__(self):
        super().__init__()

    def create(self, namespace: str, body: MockV1Ingress, **kwargs):
        if not body:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_service`"
            )

        body = copy.copy(body)
        body.spec = NetworkingV1beta1IngressSpec(**body.spec)
        body.status = NetworkingV1beta1IngressStatus(**body.status)
        try:
            return super().create(namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_ingress`"
            )

    def read(self, name: str, namespace: str, **kwargs):
        return super().read(name, namespace, **kwargs)

    def list_all(self, **kwargs):
        services = super().list_all(**kwargs)
        return NetworkingV1beta1IngressList(items=services)

    def list(self, namespace: str, **kwargs):
        services = super().list(namespace, **kwargs)
        return NetworkingV1beta1IngressList(items=services)

    def patch(self, name: str, namespace: str, body: MockV1Ingress, **kwargs):
        try:
            return super().patch(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `patch_namespaced_ingress`"
            )

    def replace(
        self, name: str, namespace: str, body: MockV1Ingress, **kwargs
    ):
        try:
            return super().replace(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `replace_namespaced_ingress`"
            )

    def delete(self, name: str, namespace: str, **kwargs):
        return super().delete(name, namespace, **kwargs)
