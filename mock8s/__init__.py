import decorator

from mock import patch
from mock8s.client.api.mock_core_v1_api import MockCoreV1Api
from mock8s.client.api.mock_apps_v1_api import MockAppsV1Api
from mock8s.client.api.mock_networking_v1_beta1_api import (
    MockNetworkingV1beta1Api,
)
from mock8s.client.models.mock_v1_service import MockV1Service
from mock8s.client.models.mock_v1_pod import MockV1Pod
from mock8s.client.models.mock_v1_deployment import MockV1Deployment
from mock8s.client.models.mock_v1_ingress import MockV1Ingress
from mock8s.config.mock_kube_config import mock_load_kube_config


def mock8s(function):
    def wrapper_mock8s(f, *args, **kwargs):
        with patch("kubernetes.client.CoreV1Api", new=MockCoreV1Api), patch(
            "kubernetes.client.AppsV1Api", new=MockAppsV1Api
        ), patch(
            "kubernetes.client.NetworkingV1beta1Api",
            new=MockNetworkingV1beta1Api,
        ), patch(
            "kubernetes.client.models.V1Service", new=MockV1Service
        ), patch(
            "kubernetes.client.models.V1Pod", new=MockV1Pod
        ), patch(
            "kubernetes.client.models.NetworkingV1beta1Ingress",
            new=MockV1Ingress,
        ), patch(
            "kubernetes.client.models.V1Deployment", new=MockV1Deployment
        ), patch(
            "kubernetes.config.load_kube_config", new=mock_load_kube_config
        ):
            return f(*args, **kwargs)

    return decorator.decorator(wrapper_mock8s, function)
