from mock import patch
from mock8s.client.api.mock_core_v1_api import MockCoreV1Api
from mock8s.config.mock_kube_config import MockConfig


def mock8s(function):
    with patch('kubernetes.client.CoreV1Api', new=MockCoreV1Api):
        return function()
