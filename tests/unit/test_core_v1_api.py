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
    assert len(v1.list_service_for_all_namespaces().items) == 0
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
    assert len(v1.list_service_for_all_namespaces().items) == 1

@mock8s
def test_create_service_wrong_kind():
    pass

@mock8s
def test_delete_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    v1.delete_namespaced_service("foobar", "default")
    assert len(v1.list_service_for_all_namespaces().items) == 0

@mock8s
def test_delete_service_name_doesnt_exist():
    pass


@mock8s
def test_delete_service_namespace_doesnt_exist():
    pass

@mock8s
def test_list_services_on_namespace(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    services = v1.list_namespaced_service("default")
    assert len(services.items) == 1

@mock8s
def test_list_services_on_namespace_empty():
    pass

@mock8s
def test_list_services_on_namespace_namespace_doesnt_exist():
    pass
