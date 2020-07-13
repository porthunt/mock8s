from kubernetes.client.models.v1_service import V1Service
from kubernetes.client.rest import ApiException


class MockV1Service(V1Service):
    def __init__(
        self,
        api_version=None,
        kind=None,
        metadata=None,
        spec=None,
        status=None,
    ):
        if kind and kind != "Service":
            raise ApiException(400, "Bad Request")
        super().__init__(api_version, kind, metadata, spec, status)

    def __hash__(self):
        return hash(self.metadata.name)
