from kubernetes.config.kube_config import load_kube_config  # noqa
from kubernetes.config.config_exception import ConfigException  # noqa


def mock_load_kube_config(
    config_file=None,
    context=None,
    client_configuration=None,
    persist_config=True,
):
    print("A")
