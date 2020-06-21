from kubernetes.client.models.v1_api_service import V1APIService
from mock8s.client.models.mock_v1_object_meta import MockV1ObjectMeta
from mock8s.client.models.mock_v1_service_spec import MockV1ServiceSpec
from mock8s.client.models.mock_v1_service_status import MockV1ServiceStatus
from kubernetes.client.rest import ApiException

import pprint
import six


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
            if kind != "Service":
                raise ApiException(400, "Bad Request")
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

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value,
                    )
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MockV1APIService):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def __hash__(self):
        return hash(self.metadata.uid)
