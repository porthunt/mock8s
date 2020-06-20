import pytest
import yaml

from mock8s import mock8s
from kubernetes import config
from kubernetes import client


@pytest.fixture
def service_yaml():
    return """
    apiVersion: v1
    kind: Service
    metadata:
        name: foobar
        labels:
            "group": "abc"
    spec:
        type: ClusterIP
        selector:
            app: "barbaz"
        ports:
            - protocol: TCP
              port: 80
              targetPort: 80
    """


@mock8s
def test_create_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.kind == "Service"
    assert new_service.metadata.__class__.__name__ == "MockV1ObjectMeta"
    assert new_service.spec.__class__.__name__ == "MockV1ServiceSpec"
    assert new_service.status.__class__.__name__ == "MockV1ServiceStatus"
    assert new_service.spec.cluster_ip == "localhost"
    assert new_service.spec.selector == {"app": "barbaz"}
    assert new_service.spec.type == "ClusterIP"
    assert (
        new_service.status.load_balancer.__class__.__name__
        == "MockV1LoadBalancerStatus"
    )
