import pytest
import yaml

from mock8s import mock8s
from kubernetes import config
from kubernetes import client
from kubernetes.client.rest import ApiException


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
def test_list_service_for_all_namespaces(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1


@mock8s
def test_list_service_for_all_namespaces_label_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(label_selector="xxx")
    assert len(filtered.items) == 0


@mock8s
def test_list_service_for_all_namespaces_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(field_selector="barbaz")
    assert len(filtered.items) == 1


@mock8s
def test_list_service_for_all_namespaces_label_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(
        label_selector="group=abc", field_selector="barbaz"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_service_for_all_namespaces_bad_label_correct_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(
        label_selector="group=def", field_selector="barbaz"
    )
    assert len(filtered.items) == 0


@mock8s
def test_list_service_for_all_namespaces_correct_label_bad_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(
        label_selector="group=abc", field_selector="xxx"
    )
    assert len(filtered.items) == 0


@mock8s
def test_list_service_for_all_namespaces_empty():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    assert len(v1.list_service_for_all_namespaces().items) == 0


@mock8s
def test_create_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.metadata.name == "foobar"
    assert new_service.metadata.namespace == "default"
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
def test_create_namespaced_service_wrong_kind(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    service_yaml = service_yaml.replace("kind: Service", "kind: Servii")
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_service("default", body=body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_create_namespaced_service_wrong_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_service("no-namespace", body=body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    v1.delete_namespaced_service("foobar", "default")
    assert len(v1.list_service_for_all_namespaces().items) == 0


@mock8s
def test_delete_namespaced_service_name_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_service("no-service", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_service_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_service("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_list_namespaced_service_on_namespace(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    services = v1.list_namespaced_service("default")
    assert len(services.items) == 1


@mock8s
def test_list_namespaced_service_label_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service("default", label_selector="xxx")
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 0


@mock8s
def test_list_namespaced_service_label_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default", label_selector="abc", field_selector="barbaz"
    )
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 1


@mock8s
def test_list_namespaced_service_bad_label_correct_field_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default", label_selector="xxx", field_selector="barbaz"
    )
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 0


@mock8s
def test_list_namespaced_service_correct_label_bad_field_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default", label_selector="abc", field_selector="xxx"
    )
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 0


@mock8s
def test_list_namespaced_service_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default", field_selector="barbaz"
    )
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 1


@mock8s
def test_list_namespaced_service_on_namespace_empty():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    services = v1.list_namespaced_service("default")
    assert len(services.items) == 0


@mock8s
def test_list_namespaced_service_namespace_doesnt_exist():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_service("no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_service = v1.create_namespaced_service("default", body=body)
    read_service = v1.read_namespaced_service("foobar", "default")
    assert read_service.metadata.name == "foobar"
    assert read_service.metadata.namespace == "default"
    assert read_service.metadata.labels == {"group": "abc"}
    assert read_service.kind == "Service"
    assert read_service == new_service


@mock8s
def test_read_namespaced_service_service_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_service("no-service", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_service_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_service("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    new_service_yaml = service_yaml.replace('"group": "abc"', '"group": "def"')
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = yaml.load(new_service_yaml, Loader=yaml.FullLoader)
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.metadata.labels == {"group": "abc"}
    replaced_service = v1.replace_namespaced_service(
        "foobar", "default", new_body
    )
    assert new_service != replaced_service
    assert replaced_service.metadata.labels == {"group": "def"}


@mock8s
def test_replace_namespaced_service_service_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = None
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_service("no-service", "default", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_service_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = None
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_service("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_service_invalid_body(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    new_service_yaml = service_yaml.replace("kind: Service", "kind: Servii")
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = yaml.load(new_service_yaml, Loader=yaml.FullLoader)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_service("foobar", "default", new_body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_patch_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    new_service_yaml = service_yaml.replace('"group": "abc"', '"group": "def"')
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = yaml.load(new_service_yaml, Loader=yaml.FullLoader)
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.metadata.labels == {"group": "abc"}
    replaced_service = v1.patch_namespaced_service(
        "foobar", "default", new_body
    )
    assert new_service == replaced_service
    assert replaced_service.metadata.labels == {"group": "def"}


@mock8s
def test_patch_namespaced_service_service_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = None
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_service("no-service", "default", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_patch_namespaced_service_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(service_yaml, Loader=yaml.FullLoader)
    new_body = None
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_service("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"
