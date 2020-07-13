from kubernetes.client.models.v1_pod import V1Pod
from kubernetes.client.rest import ApiException


class MockV1Pod(V1Pod):
    def __init__(
        self,
        api_version=None,
        kind=None,
        metadata=None,
        spec=None,
        status=None,
    ):
        if kind and kind != "Pod":
            raise ApiException(400, "Bad Request")
        super().__init__(api_version, kind, metadata, spec, status)

    def __hash__(self):
        return hash(self.metadata.name)
