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


@pytest.fixture
def pod_yaml():
    return """
    apiVersion: v1
    kind: Pod
    metadata:
        name: barbaz
        labels:
            "group": "def"
    spec:
        containers:
            - name: web
              image: nginx
              ports:
                - name: web
                  containerPort: 80
                  protocol: TCP
    """


def generate_service(body):
    return client.models.V1Service(
        api_version=body.get("apiVersion"),
        kind=body.get("kind"),
        metadata=body.get("metadata"),
        spec=body.get("spec"),
        status=body.get("status", {}),
    )


def generate_pod(body):
    return client.models.V1Pod(
        api_version=body.get("apiVersion"),
        kind=body.get("kind"),
        metadata=body.get("metadata"),
        spec=body.get("spec"),
        status=body.get("status", {}),
    )


@mock8s
def test_list_service_for_all_namespaces(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1


@mock8s
def test_list_service_for_all_namespaces_label_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(label_selector="group=abc")
    assert len(filtered.items) == 1


@mock8s
def test_list_service_for_all_namespaces_label_selector_not_found(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(label_selector="xxx")
    assert len(filtered.items) == 0


@mock8s
def test_list_service_for_all_namespaces_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(
        field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_service_for_all_namespaces_label_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(
        label_selector="group=abc", field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_service_for_all_namespaces_bad_label_correct_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
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
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    filtered = v1.list_service_for_all_namespaces(
        label_selector="group=abc", field_selector="metadata.name=barbaz"
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
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    assert len(v1.list_service_for_all_namespaces().items) == 0
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.metadata["name"] == "foobar"
    assert new_service.metadata["namespace"] == "default"
    assert new_service.kind == "Service"
    assert new_service.spec["selector"] == {"app": "barbaz"}
    assert new_service.spec["type"] == "ClusterIP"
    assert len(v1.list_service_for_all_namespaces().items) == 1


@mock8s
def test_create_namespaced_service_wrong_kind(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    service_yaml = service_yaml.replace("kind: Service", "kind: Servii")
    raw_body = yaml.safe_load(service_yaml)
    with pytest.raises(ApiException) as err:
        body = generate_service(raw_body)
        v1.create_namespaced_service("default", body=body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_create_namespaced_service_wrong_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_service("no-namespace", body=body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    assert len(v1.list_service_for_all_namespaces().items) == 1
    v1.delete_namespaced_service("foobar", "default")
    assert len(v1.list_service_for_all_namespaces().items) == 0


@mock8s
def test_delete_namespaced_service_name_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_service("no-service", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_service_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_service("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_list_namespaced_service_on_namespace(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    services = v1.list_namespaced_service("default")
    assert len(services.items) == 1


@mock8s
def test_list_namespaced_service_label_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service("default", label_selector="xxx")
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 0


@mock8s
def test_list_namespaced_service_label_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default",
        label_selector="group=abc",
        field_selector="metadata.namespace=default",
    )
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 1


@mock8s
def test_list_namespaced_service_bad_label_correct_field_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default", label_selector="xxx", field_selector="metadata.name=foobar"
    )
    assert len(servs.items) == 1
    assert len(servs_filter.items) == 0


@mock8s
def test_list_namespaced_service_correct_label_bad_field_selector(
    service_yaml,
):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_service(
            "default", label_selector="group=abc", field_selector="xxx"
        )
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_list_namespaced_service_field_selector(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    servs = v1.list_namespaced_service("default")
    servs_filter = v1.list_namespaced_service(
        "default", field_selector="metadata.name=foobar"
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
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    new_service = v1.create_namespaced_service("default", body=body)
    read_service = v1.read_namespaced_service("foobar", "default")
    assert read_service.metadata["name"] == "foobar"
    assert read_service.metadata["namespace"] == "default"
    assert read_service.metadata["labels"] == {"group": "abc"}
    assert read_service.kind == "Service"
    assert read_service == new_service


@mock8s
def test_read_namespaced_service_service_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_service("no-service", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_service_namespace_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(service_yaml)
    body = generate_service(raw_body)
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
    body = generate_service(yaml.safe_load(service_yaml))
    new_body = generate_service(yaml.safe_load(new_service_yaml))
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.metadata["labels"] == {"group": "abc"}
    replaced_service = v1.replace_namespaced_service(
        "foobar", "default", new_body
    )
    assert new_service != replaced_service
    assert replaced_service.metadata["labels"] == {"group": "def"}


@mock8s
def test_replace_namespaced_service_service_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = generate_service(yaml.safe_load(service_yaml))
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
    body = generate_service(yaml.safe_load(service_yaml))
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
    with pytest.raises(ApiException) as err:
        new_service_yaml = service_yaml.replace(
            "kind: Service", "kind: Servii"
        )
        body = generate_service(yaml.safe_load(service_yaml))
        new_body = generate_service(yaml.safe_load(new_service_yaml))
        v1.create_namespaced_service("default", body=body)
        v1.replace_namespaced_service("foobar", "default", new_body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_patch_namespaced_service(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    new_service_yaml = service_yaml.replace('"group": "abc"', '"group": "def"')
    body = generate_service(yaml.safe_load(service_yaml))
    new_body = generate_service(yaml.safe_load(new_service_yaml))
    new_service = v1.create_namespaced_service("default", body=body)
    assert new_service.metadata["labels"] == {"group": "abc"}
    patched_service = v1.patch_namespaced_service(
        "foobar", "default", new_body
    )
    assert new_service == patched_service
    assert patched_service.metadata["labels"] == {"group": "def"}


@mock8s
def test_patch_namespaced_service_service_doesnt_exist(service_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = generate_service(yaml.safe_load(service_yaml))
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
    body = generate_service(yaml.safe_load(service_yaml))
    new_body = None
    v1.create_namespaced_service("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_service("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_create_namespaced_pod(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    new_pod = v1.create_namespaced_pod("default", body=body)
    assert new_pod.metadata["name"] == "barbaz"
    assert new_pod.metadata["namespace"] == "default"
    assert new_pod.kind == "Pod"
    assert new_pod.spec["containers"][0]["name"] == "web"
    assert new_pod.spec["containers"][0]["image"] == "nginx"
    assert new_pod.spec["containers"][0]["ports"][0]["name"] == "web"
    assert new_pod.spec["containers"][0]["ports"][0]["containerPort"] == 80
    assert new_pod.spec["containers"][0]["ports"][0]["protocol"] == "TCP"


@mock8s
def test_create_namespaced_pod_wrong_kind(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pod_yaml = pod_yaml.replace("kind: Pod", "kind: Pdo")
    raw_body = yaml.safe_load(pod_yaml)
    with pytest.raises(ApiException) as err:
        body = generate_pod(raw_body)
        v1.create_namespaced_pod("default", body=body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_create_namespaced_pod_wrong_namespace_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_pod("no-namespace", body=body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_pod(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    pod = v1.create_namespaced_pod("default", body=body)
    read_pod = v1.read_namespaced_pod("barbaz", "default")
    assert pod == read_pod
    v1.delete_namespaced_pod("barbaz", "default")
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_pod("barbaz", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_pod_name_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_service("barbazbaz", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_pod_namespace_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_service("barbaz", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_list_namespaced_pod_on_namespace(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    pod = v1.create_namespaced_pod("default", body=body)
    pods = v1.list_namespaced_pod("default")
    assert len(pods.items) == 1
    assert pods.items.pop() == pod


@mock8s
def test_list_namespaced_pod_label_selector(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    pods = v1.list_namespaced_pod("default")
    pods_filter = v1.list_namespaced_service("default", label_selector="xxx")
    assert len(pods.items) == 1
    assert len(pods_filter.items) == 0


@mock8s
def test_list_namespaced_pod_correct_label_selector(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    v1.read_namespaced_pod("barbaz", "default")
    filtered = v1.list_namespaced_pod("default", label_selector="group=def")
    assert len(filtered.items) == 1


@mock8s
def test_list_namespaced_pod_namespace_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    v1.read_namespaced_pod("barbaz", "default")
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_pod("no-namespace", label_selector="group=def")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_pod(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    new_pod = v1.create_namespaced_pod("default", body=body)
    read_pod = v1.read_namespaced_pod("barbaz", "default")
    assert read_pod.metadata["name"] == "barbaz"
    assert read_pod.metadata["namespace"] == "default"
    assert read_pod.metadata["labels"] == {"group": "def"}
    assert read_pod.kind == "Pod"
    assert read_pod == new_pod


@mock8s
def test_read_namespaced_pod_pod_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_pod("barbazbaz", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_pod_namespace_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    raw_body = yaml.safe_load(pod_yaml)
    body = generate_pod(raw_body)
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_pod("barbaz", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_pod(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    new_pod_yaml = pod_yaml.replace('"group": "def"', '"group": "xxx"')
    body = generate_pod(yaml.safe_load(pod_yaml))
    new_body = generate_pod(yaml.safe_load(new_pod_yaml))
    new_pod = v1.create_namespaced_pod("default", body=body)
    assert new_pod.metadata["labels"] == {"group": "def"}
    replaced_pod = v1.replace_namespaced_pod("barbaz", "default", new_body)
    assert new_pod != replaced_pod
    assert replaced_pod.metadata["labels"] == {"group": "xxx"}


@mock8s
def test_replace_namespaced_pod_pod_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = generate_pod(yaml.safe_load(pod_yaml))
    new_body = None
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_pod("no-pod", "default", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_pod_namespace_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = generate_pod(yaml.safe_load(pod_yaml))
    new_body = None
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_pod("barbaz", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_pod_invalid_body(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    with pytest.raises(ApiException) as err:
        new_pod_yaml = pod_yaml.replace("kind: Pod", "kind: Pdo")
        body = generate_pod(yaml.safe_load(pod_yaml))
        new_body = generate_pod(yaml.safe_load(new_pod_yaml))
        v1.create_namespaced_pod("default", body=body)
        v1.replace_namespaced_pod("barbaz", "default", new_body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_patch_namespaced_pod(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    new_pod_yaml = pod_yaml.replace('"group": "def"', '"group": "xxx"')
    body = generate_pod(yaml.safe_load(pod_yaml))
    new_body = generate_pod(yaml.safe_load(new_pod_yaml))
    new_pod = v1.create_namespaced_pod("default", body=body)
    assert new_pod.metadata["labels"] == {"group": "def"}
    patched_pod = v1.patch_namespaced_pod("barbaz", "default", new_body)
    assert new_pod == patched_pod
    assert patched_pod.metadata["labels"] == {"group": "xxx"}


@mock8s
def test_patch_namespaced_pod_pod_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = generate_pod(yaml.safe_load(pod_yaml))
    new_body = None
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_pod("no-pod", "default", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_patch_namespaced_pod_namespace_doesnt_exist(pod_yaml):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = generate_pod(yaml.safe_load(pod_yaml))
    new_body = None
    v1.create_namespaced_pod("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_pod("barbaz", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"
