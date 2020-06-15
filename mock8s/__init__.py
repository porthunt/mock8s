from mock8s.client.api.mock_core_v1_api import MockCoreV1Api
from mock8s.config.mock_kube_config import MockConfig


def mock8s(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper
