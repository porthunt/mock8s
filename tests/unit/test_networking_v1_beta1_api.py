import pytest
import yaml

from mock8s import mock8s
from kubernetes import config
from kubernetes import client
from kubernetes.client.rest import ApiException


@pytest.fixture
def ingress_yaml():
    return """
    apiVersion: networking.k8s.io/v1beta1
    kind: Ingress
    metadata:
      name: foobar
      labels:
        "app": "foo"
    spec:
      rules:
      - host: example.com
        http:
          paths:
          -  backend:
              serviceName: foobar
              servicePort: 80
    """


def generate_ingress(body):
    return client.models.NetworkingV1beta1Ingress(
        api_version=body.get("apiVersion"),
        kind=body.get("kind"),
        metadata=body.get("metadata"),
        spec=body.get("spec"),
        status=body.get("status", {}),
    )


@mock8s
def test_list_ingress_for_all_namespaces(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1


@mock8s
def test_list_ingress_for_all_namespaces_label_selector(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    filtered = v1.list_ingress_for_all_namespaces(label_selector="app=foo")
    assert len(filtered.items) == 1


@mock8s
def test_list_ingress_for_all_namespaces_label_selector_not_found(
    ingress_yaml,
):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    filtered = v1.list_ingress_for_all_namespaces(label_selector="xxx")
    assert len(filtered.items) == 0


@mock8s
def test_list_ingress_for_all_namespaces_field_selector(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    filtered = v1.list_ingress_for_all_namespaces(
        field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_ingress_for_all_namespaces_label_field_selector(ingress_yaml,):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    filtered = v1.list_ingress_for_all_namespaces(
        label_selector="app=foo", field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_ingress_for_all_namespaces_bad_label_correct_selector(
    ingress_yaml,
):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    filtered = v1.list_ingress_for_all_namespaces(
        label_selector="app=bar", field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 0


@mock8s
def test_list_ingress_for_all_namespaces_correct_label_bad_selector(
    ingress_yaml,
):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    filtered = v1.list_ingress_for_all_namespaces(
        label_selector="app=foo", field_selector="metadata.name=barbaz"
    )
    assert len(filtered.items) == 0


@mock8s
def test_list_ingress_for_all_namespaces_empty():
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    assert len(v1.list_ingress_for_all_namespaces().items) == 0


@mock8s
def test_create_namespaced_ingress(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 0
    new_ingress = v1.create_namespaced_ingress("default", body=body)
    assert new_ingress.metadata.name == "foobar"
    assert new_ingress.metadata.namespace == "default"
    assert new_ingress.kind == "Ingress"
    assert new_ingress.spec.rules[0]["host"] == "example.com"
    assert len(v1.list_ingress_for_all_namespaces().items) == 1


@mock8s
def test_create_namespaced_ingress_already_exists(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_ingress("default", body=body)
    assert err.value.status == 409
    assert err.value.reason == "AlreadyExists"


@mock8s
def test_create_namespaced_ingress_no_body():
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    with pytest.raises(ValueError) as err:
        v1.create_namespaced_ingress("default", body=None)
    assert "Missing the required parameter `body`" in str(err.value)


@mock8s
def test_create_namespaced_ingress_wrong_kind(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    ingress_yaml = ingress_yaml.replace("kind: Ingress", "kind: Igres")
    raw_body = yaml.safe_load(ingress_yaml)
    with pytest.raises(ApiException) as err:
        body = generate_ingress(raw_body)
        v1.create_namespaced_ingress("default", body=body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_create_namespaced_ingress_wrong_namespace_doesnt_exist(ingress_yaml,):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_ingress("no-namespace", body=body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_ingress(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    assert len(v1.list_ingress_for_all_namespaces().items) == 1
    v1.delete_namespaced_ingress("foobar", "default")
    assert len(v1.list_ingress_for_all_namespaces().items) == 0


@mock8s
def test_delete_namespaced_ingress_name_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_ingress("no-service", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_ingress_namespace_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_ingress("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_list_namespaced_ingress_on_namespace(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    ingress = v1.list_namespaced_ingress("default")
    assert len(ingress.items) == 1


@mock8s
def test_list_namespaced_ingress_label_selector(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    ingresss = v1.list_namespaced_ingress("default")
    ingresss_filter = v1.list_namespaced_ingress(
        "default", label_selector="xxx"
    )
    assert len(ingresss.items) == 1
    assert len(ingresss_filter.items) == 0


@mock8s
def test_list_namespaced_ingress_label_field_selector(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    ingresss = v1.list_namespaced_ingress("default")
    ingresss_filter = v1.list_namespaced_ingress(
        "default",
        label_selector="app=foo",
        field_selector="metadata.namespace=default",
    )
    assert len(ingresss.items) == 1
    assert len(ingresss_filter.items) == 1


@mock8s
def test_list_namespaced_ingress_bad_label_correct_field_selector(
    ingress_yaml,
):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    ingresss = v1.list_namespaced_ingress("default")
    ingresss_filter = v1.list_namespaced_ingress(
        "default", label_selector="xxx", field_selector="metadata.name=foobar"
    )
    assert len(ingresss.items) == 1
    assert len(ingresss_filter.items) == 0


@mock8s
def test_list_namespaced_ingress_correct_label_bad_field_selector(
    ingress_yaml,
):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_ingress(
            "default", label_selector="app=foo", field_selector="xxx"
        )
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_list_namespaced_ingress_field_selector(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    ingresss = v1.list_namespaced_ingress("default")
    ingresss_filter = v1.list_namespaced_ingress(
        "default", field_selector="metadata.name=foobar"
    )
    assert len(ingresss.items) == 1
    assert len(ingresss_filter.items) == 1


@mock8s
def test_list_namespaced_ingress_on_namespace_empty():
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    ingresss = v1.list_namespaced_ingress("default")
    assert len(ingresss.items) == 0


@mock8s
def test_list_namespaced_ingress_namespace_doesnt_exist():
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_ingress("no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_ingress(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    new_ingress = v1.create_namespaced_ingress("default", body=body)
    read_ingress = v1.read_namespaced_ingress("foobar", "default")
    assert read_ingress.metadata.name == "foobar"
    assert read_ingress.metadata.namespace == "default"
    assert read_ingress.metadata.labels == {"app": "foo"}
    assert read_ingress.kind == "Ingress"
    assert read_ingress == new_ingress


@mock8s
def test_read_namespaced_ingress_ingress_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_ingress("no-ingress", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_ingress_namespace_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    raw_body = yaml.safe_load(ingress_yaml)
    body = generate_ingress(raw_body)
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_ingress("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_ingress(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    new_ingress_yaml = ingress_yaml.replace('"app": "foo"', '"app": "baz"')
    body = generate_ingress(yaml.safe_load(ingress_yaml))
    new_body = generate_ingress(yaml.safe_load(new_ingress_yaml))
    new_ingress = v1.create_namespaced_ingress("default", body=body)
    assert new_ingress.metadata.labels == {"app": "foo"}
    replaced_ingress = v1.replace_namespaced_ingress(
        "foobar", "default", new_body
    )
    assert new_ingress != replaced_ingress
    assert replaced_ingress.metadata.labels == {"app": "baz"}


@mock8s
def test_replace_namespaced_ingress_ingress_doesnt_exist(ingress_yaml,):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    body = generate_ingress(yaml.safe_load(ingress_yaml))
    new_body = None
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ValueError) as err:
        v1.replace_namespaced_ingress("no-service", "default", new_body)
    assert "Missing the required parameter `body`" in str(err.value)


@mock8s
def test_replace_namespaced_ingress_namespace_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    body = generate_ingress(yaml.safe_load(ingress_yaml))
    new_body = None
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_ingress("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_ingress_invalid_body(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    with pytest.raises(ApiException) as err:
        new_ingress_yaml = ingress_yaml.replace("kind: Ingress", "kind: Igres")
        body = generate_ingress(yaml.safe_load(ingress_yaml))
        new_body = generate_ingress(yaml.safe_load(new_ingress_yaml))
        v1.create_namespaced_ingress("default", body=body)
        v1.replace_namespaced_ingress("foobar", "default", new_body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_patch_namespaced_ingress(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    new_ingress_yaml = ingress_yaml.replace('"app": "foo"', '"app": "bar"')
    body = generate_ingress(yaml.safe_load(ingress_yaml))
    new_body = generate_ingress(yaml.safe_load(new_ingress_yaml))
    new_ingress = v1.create_namespaced_ingress("default", body=body)
    assert new_ingress.metadata.labels == {"app": "foo"}
    patched_ingress = v1.patch_namespaced_ingress(
        "foobar", "default", new_body
    )
    assert new_ingress == patched_ingress
    assert patched_ingress.metadata.labels == {"app": "bar"}


@mock8s
def test_patch_namespaced_ingress_ingress_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    body = generate_ingress(yaml.safe_load(ingress_yaml))
    new_body = None
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ValueError) as err:
        v1.patch_namespaced_ingress("no-service", "default", new_body)
    assert "Missing the required parameter `body`" in str(err.value)


@mock8s
def test_patch_namespaced_ingress_namespace_doesnt_exist(ingress_yaml):
    config.load_kube_config()
    v1 = client.NetworkingV1beta1Api()
    body = generate_ingress(yaml.safe_load(ingress_yaml))
    new_body = None
    v1.create_namespaced_ingress("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_ingress("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"
