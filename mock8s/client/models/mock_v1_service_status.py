from kubernetes.client.models.v1_service_status import V1ServiceStatus
from mock8s.client.models.mock_v1_load_balancer_status import \
    MockV1LoadBalancerStatus

import pprint
import six


class MockV1ServiceStatus:
    openapi_types = {
        'load_balancer': 'V1LoadBalancerStatus'
    }

    attribute_map = {
        'load_balancer': 'loadBalancer'
    }

    def __init__(self, load_balancer=None):
        if not load_balancer:
            self.load_balancer = MockV1LoadBalancerStatus()

        self._load_balancer = self.load_balancer
        self.discriminator = None

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, V1ServiceStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
