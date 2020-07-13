from kubernetes.client.models.networking_v1beta1_ingress import (
    NetworkingV1beta1Ingress,
)
from kubernetes.client.rest import ApiException


class MockV1Ingress(NetworkingV1beta1Ingress):
    def __init__(
        self,
        api_version=None,
        kind=None,
        metadata=None,
        spec=None,
        status=None,
    ):
        if kind and kind != "Ingress":
            raise ApiException(400, "Bad Request")
        super().__init__(api_version, kind, metadata, spec, status)

    def __hash__(self):
        return hash(self.metadata.name)
