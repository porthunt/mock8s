# from kubernetes.client.models.v1_service_spec import V1ServiceSpec
from mock8s.config import MOCK_CLUSTER_IP
import six
import pprint


class MockV1ServiceSpec(object):
    openapi_types = {
        "cluster_ip": "str",
        "external_i_ps": "list[str]",
        "external_name": "str",
        "external_traffic_policy": "str",
        "health_check_node_port": "int",
        "load_balancer_ip": "str",
        "load_balancer_source_ranges": "list[str]",
        "ports": "list[V1ServicePort]",
        "publish_not_ready_addresses": "bool",
        "selector": "dict(str, str)",
        "session_affinity": "str",
        "session_affinity_config": "V1SessionAffinityConfig",
        "type": "str",
    }

    attribute_map = {
        "cluster_ip": "clusterIP",
        "external_i_ps": "externalIPs",
        "external_name": "externalName",
        "external_traffic_policy": "externalTrafficPolicy",
        "health_check_node_port": "healthCheckNodePort",
        "load_balancer_ip": "loadBalancerIP",
        "load_balancer_source_ranges": "loadBalancerSourceRanges",
        "ports": "ports",
        "publish_not_ready_addresses": "publishNotReadyAddresses",
        "selector": "selector",
        "session_affinity": "sessionAffinity",
        "session_affinity_config": "sessionAffinityConfig",
        "type": "type",
    }

    def __init__(
        self,
        cluster_ip=None,
        external_i_ps=None,
        external_name=None,
        external_traffic_policy=None,
        health_check_node_port=None,
        load_balancer_ip=None,
        load_balancer_source_ranges=None,
        ports=None,
        publish_not_ready_addresses=None,
        selector=None,
        session_affinity=None,
        session_affinity_config=None,
        type=None,
    ):

        self.cluster_ip = cluster_ip if cluster_ip else MOCK_CLUSTER_IP
        self._cluster_ip = self.cluster_ip

        self.external_i_ps = external_i_ps
        self._external_i_ps = self.external_i_ps

        self.external_name = external_name
        self._external_name = external_name

        self.external_traffic_policy = external_traffic_policy
        self._external_traffic_policy = external_traffic_policy

        self.health_check_node_port = health_check_node_port
        self._health_check_node_port = health_check_node_port

        self.load_balancer_ip = load_balancer_ip
        self._load_balancer_ip = load_balancer_ip

        self.load_balancer_source_ranges = load_balancer_source_ranges
        self._load_balancer_source_ranges = load_balancer_source_ranges

        self.ports = ports
        self._ports = ports

        self.publish_not_ready_addresses = publish_not_ready_addresses
        self._publish_not_ready_addresses = publish_not_ready_addresses

        self.selector = selector
        self._selector = selector

        self.session_affinity = session_affinity
        self._session_affinity = session_affinity

        self.session_affinity_config = session_affinity_config
        self._session_affinity_config = session_affinity_config

        self.type = type
        self._type = type

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
        if not isinstance(other, MockV1ServiceSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
