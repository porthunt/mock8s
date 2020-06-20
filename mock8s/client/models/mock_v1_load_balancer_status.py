#from kubernetes.client.models.v1_load_balancer_status import V1LoadBalancerStatus
import pprint
import six


class MockV1LoadBalancerStatus:

    openapi_types = {
        'ingress': 'list[V1LoadBalancerIngress]'
    }

    attribute_map = {
        'ingress': 'ingress'
    }

    def __init__(self, ingress=None):  # noqa: E501
        self._ingress = None
        self.discriminator = None

        self.ingress = ingress
        self._ingress = self.ingress

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
        if not isinstance(other, V1LoadBalancerStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
