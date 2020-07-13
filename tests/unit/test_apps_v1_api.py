import pytest
import yaml

from mock8s import mock8s
from kubernetes import config
from kubernetes import client
from kubernetes.client.rest import ApiException


@pytest.fixture
def deployment_yaml():
    return """
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: foobar
      labels:
        "app": "foo"
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: foobar-service
      template:
        metadata:
          labels:
            app: foobar-service
        spec:
          containers:
          - name: foobar-service
            image: ubuntu:latest
            ports:
            - containerPort: 8080
              name: foobar-service
            env:
              - name: ENVIRONMENT
                value: dev
    """


def generate_deployment(body):
    return client.models.V1Deployment(
        api_version=body.get("apiVersion"),
        kind=body.get("kind"),
        metadata=body.get("metadata"),
        spec=body.get("spec"),
        status=body.get("status", {}),
    )


@mock8s
def test_list_deployment_for_all_namespaces(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1


@mock8s
def test_list_deployment_for_all_namespaces_label_selector(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    filtered = v1.list_deployment_for_all_namespaces(label_selector="app=foo")
    assert len(filtered.items) == 1


@mock8s
def test_list_deployment_for_all_namespaces_label_selector_not_found(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    filtered = v1.list_deployment_for_all_namespaces(label_selector="xxx")
    assert len(filtered.items) == 0


@mock8s
def test_list_deployment_for_all_namespaces_field_selector(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    filtered = v1.list_deployment_for_all_namespaces(
        field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_deployment_for_all_namespaces_label_field_selector(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    filtered = v1.list_deployment_for_all_namespaces(
        label_selector="app=foo", field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 1


@mock8s
def test_list_deployment_for_all_namespaces_bad_label_correct_selector(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    filtered = v1.list_deployment_for_all_namespaces(
        label_selector="app=bar", field_selector="metadata.name=foobar"
    )
    assert len(filtered.items) == 0


@mock8s
def test_list_deployment_for_all_namespaces_correct_label_bad_selector(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    filtered = v1.list_deployment_for_all_namespaces(
        label_selector="app=foo", field_selector="metadata.name=barbaz"
    )
    assert len(filtered.items) == 0


@mock8s
def test_list_deployment_for_all_namespaces_empty():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    assert len(v1.list_deployment_for_all_namespaces().items) == 0


@mock8s
def test_create_namespaced_deployment(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 0
    new_deployment = v1.create_namespaced_deployment("default", body=body)
    assert new_deployment.metadata.name == "foobar"
    assert new_deployment.metadata.namespace == "default"
    assert new_deployment.kind == "Deployment"
    assert new_deployment.spec.selector == {
        "matchLabels": {"app": "foobar-service"}
    }
    assert len(v1.list_deployment_for_all_namespaces().items) == 1


@mock8s
def test_create_namespaced_deployment_already_exists(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_deployment("default", body=body)
    assert err.value.status == 409
    assert err.value.reason == "AlreadyExists"


@mock8s
def test_create_namespaced_deployment_no_body():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    with pytest.raises(ValueError) as err:
        v1.create_namespaced_deployment("default", body=None)
    assert "Missing the required parameter `body`" in str(err.value)


@mock8s
def test_create_namespaced_deployment_wrong_kind(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    deployment_yaml = deployment_yaml.replace(
        "kind: Deployment", "kind: Deploy"
    )
    raw_body = yaml.safe_load(deployment_yaml)
    with pytest.raises(ApiException) as err:
        body = generate_deployment(raw_body)
        v1.create_namespaced_deployment("default", body=body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_create_namespaced_deployment_wrong_namespace_doesnt_exist(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    with pytest.raises(ApiException) as err:
        v1.create_namespaced_deployment("no-namespace", body=body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_deployment(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    assert len(v1.list_deployment_for_all_namespaces().items) == 1
    v1.delete_namespaced_deployment("foobar", "default")
    assert len(v1.list_deployment_for_all_namespaces().items) == 0


@mock8s
def test_delete_namespaced_deployment_name_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_deployment("no-service", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_delete_namespaced_deployment_namespace_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.delete_namespaced_deployment("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_list_namespaced_deployment_on_namespace(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    deployment = v1.list_namespaced_deployment("default")
    assert len(deployment.items) == 1


@mock8s
def test_list_namespaced_deployment_label_selector(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    deployments = v1.list_namespaced_deployment("default")
    deployments_filter = v1.list_namespaced_deployment(
        "default", label_selector="xxx"
    )
    assert len(deployments.items) == 1
    assert len(deployments_filter.items) == 0


@mock8s
def test_list_namespaced_deployment_label_field_selector(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    deployments = v1.list_namespaced_deployment("default")
    deployments_filter = v1.list_namespaced_deployment(
        "default",
        label_selector="app=foo",
        field_selector="metadata.namespace=default",
    )
    assert len(deployments.items) == 1
    assert len(deployments_filter.items) == 1


@mock8s
def test_list_namespaced_deployment_bad_label_correct_field_selector(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    deployments = v1.list_namespaced_deployment("default")
    deployments_filter = v1.list_namespaced_deployment(
        "default", label_selector="xxx", field_selector="metadata.name=foobar"
    )
    assert len(deployments.items) == 1
    assert len(deployments_filter.items) == 0


@mock8s
def test_list_namespaced_deployment_correct_label_bad_field_selector(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_deployment(
            "default", label_selector="app=foo", field_selector="xxx"
        )
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_list_namespaced_deployment_field_selector(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    deployments = v1.list_namespaced_deployment("default")
    deployments_filter = v1.list_namespaced_deployment(
        "default", field_selector="metadata.name=foobar"
    )
    assert len(deployments.items) == 1
    assert len(deployments_filter.items) == 1


@mock8s
def test_list_namespaced_deployment_on_namespace_empty():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    deployments = v1.list_namespaced_deployment("default")
    assert len(deployments.items) == 0


@mock8s
def test_list_namespaced_deployment_namespace_doesnt_exist():
    config.load_kube_config()
    v1 = client.AppsV1Api()
    with pytest.raises(ApiException) as err:
        v1.list_namespaced_deployment("no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_deployment(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    new_deployment = v1.create_namespaced_deployment("default", body=body)
    read_deployment = v1.read_namespaced_deployment("foobar", "default")
    assert read_deployment.metadata.name == "foobar"
    assert read_deployment.metadata.namespace == "default"
    assert read_deployment.metadata.labels == {"app": "foo"}
    assert read_deployment.kind == "Deployment"
    assert read_deployment == new_deployment


@mock8s
def test_read_namespaced_deployment_deployment_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_deployment("no-deployment", "default")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_read_namespaced_deployment_namespace_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    raw_body = yaml.safe_load(deployment_yaml)
    body = generate_deployment(raw_body)
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.read_namespaced_deployment("foobar", "no-namespace")
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_deployment(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    new_deployment_yaml = deployment_yaml.replace(
        '"app": "foo"', '"app": "baz"'
    )
    body = generate_deployment(yaml.safe_load(deployment_yaml))
    new_body = generate_deployment(yaml.safe_load(new_deployment_yaml))
    new_deployment = v1.create_namespaced_deployment("default", body=body)
    assert new_deployment.metadata.labels == {"app": "foo"}
    replaced_deployment = v1.replace_namespaced_deployment(
        "foobar", "default", new_body
    )
    assert new_deployment != replaced_deployment
    assert replaced_deployment.metadata.labels == {"app": "baz"}


@mock8s
def test_replace_namespaced_deployment_deployment_doesnt_exist(
    deployment_yaml,
):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    body = generate_deployment(yaml.safe_load(deployment_yaml))
    new_body = None
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ValueError) as err:
        v1.replace_namespaced_deployment("no-service", "default", new_body)
    assert "Missing the required parameter `body`" in str(err.value)


@mock8s
def test_replace_namespaced_deployment_namespace_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    body = generate_deployment(yaml.safe_load(deployment_yaml))
    new_body = None
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.replace_namespaced_deployment("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"


@mock8s
def test_replace_namespaced_deployment_invalid_body(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    with pytest.raises(ApiException) as err:
        new_deployment_yaml = deployment_yaml.replace(
            "kind: Deployment", "kind: Deploy"
        )
        body = generate_deployment(yaml.safe_load(deployment_yaml))
        new_body = generate_deployment(yaml.safe_load(new_deployment_yaml))
        v1.create_namespaced_deployment("default", body=body)
        v1.replace_namespaced_deployment("foobar", "default", new_body)
    assert err.value.status == 400
    assert err.value.reason == "Bad Request"


@mock8s
def test_patch_namespaced_deployment(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    new_deployment_yaml = deployment_yaml.replace(
        '"app": "foo"', '"app": "bar"'
    )
    body = generate_deployment(yaml.safe_load(deployment_yaml))
    new_body = generate_deployment(yaml.safe_load(new_deployment_yaml))
    new_deployment = v1.create_namespaced_deployment("default", body=body)
    assert new_deployment.metadata.labels == {"app": "foo"}
    patched_deployment = v1.patch_namespaced_deployment(
        "foobar", "default", new_body
    )
    assert new_deployment == patched_deployment
    assert patched_deployment.metadata.labels == {"app": "bar"}


@mock8s
def test_patch_namespaced_deployment_deployment_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    body = generate_deployment(yaml.safe_load(deployment_yaml))
    new_body = None
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ValueError) as err:
        v1.patch_namespaced_deployment("no-service", "default", new_body)
    assert "Missing the required parameter `body`" in str(err.value)


@mock8s
def test_patch_namespaced_deployment_namespace_doesnt_exist(deployment_yaml):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    body = generate_deployment(yaml.safe_load(deployment_yaml))
    new_body = None
    v1.create_namespaced_deployment("default", body=body)
    with pytest.raises(ApiException) as err:
        v1.patch_namespaced_deployment("foobar", "no-namespace", new_body)
    assert err.value.status == 404
    assert err.value.reason == "Not Found"
