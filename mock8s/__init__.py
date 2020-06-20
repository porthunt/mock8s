from mock import patch
from mock8s.client.api.mock_core_v1_api import MockCoreV1Api
from mock8s.config.mock_kube_config import load_kube_config


def mock8s(function):
    with patch('kubernetes.client.CoreV1Api', new=MockCoreV1Api), \
         patch('kubernetes.config.kube_config.load_kube_config',
               new=load_kube_config):
        return function()
