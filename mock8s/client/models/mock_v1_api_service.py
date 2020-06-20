# from kubernetes.client.models.v1_api_service import V1APIService
from mock8s.client.models.mock_v1_object_meta import MockV1ObjectMeta
from mock8s.client.models.mock_v1_service_spec import MockV1ServiceSpec
from mock8s.client.models.mock_v1_service_status import MockV1ServiceStatus


class MockV1APIService(object):

    openapi_types = {
        "api_version": "str",
        "kind": "str",
        "metadata": "V1ObjectMeta",
        "spec": "V1APIServiceSpec",
        "status": "V1APIServiceStatus",
    }

    attribute_map = {
        "api_version": "apiVersion",
        "kind": "kind",
        "metadata": "metadata",
        "spec": "spec",
        "status": "status",
    }

    def __init__(
        self,
        api_version=None,
        kind=None,
        metadata=None,
        spec=None,
        status=None,
    ):
        self._api_version = None
        self._kind = None
        self._metadata = None
        self._spec = None
        self._status = None
        self.discriminator = None

        if api_version is not None:
            self.api_version = api_version
            self._api_version = self.api_version
        if kind is not None:
            self.kind = kind
            self._kind = self.kind
        if metadata is not None:
            self.metadata = MockV1ObjectMeta(**metadata)
            self._metadata = self.metadata
        if spec is not None:
            self.spec = MockV1ServiceSpec(**spec)
            self._spec = self.spec

        self.status = MockV1ServiceStatus(**status)
        self._status = self.status
