import copy
from mock8s.core.resources import Resources
from mock8s.client.models.mock_v1_deployment import MockV1Deployment
from kubernetes.client.models.v1_deployment_list import V1DeploymentList
from kubernetes.client.models.v1_deployment_spec import V1DeploymentSpec
from kubernetes.client.models.v1_deployment_status import V1DeploymentStatus


class Deployments(Resources):
    def __init__(self):
        super().__init__()

    def create(self, namespace: str, body: MockV1Deployment, **kwargs):
        if not body:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_deployment`"
            )

        body = copy.copy(body)
        body.spec = V1DeploymentSpec(**body.spec)
        body.status = V1DeploymentStatus(**body.status)
        try:
            return super().create(namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_deployment`"
            )

    def read(self, name: str, namespace: str, **kwargs):
        return super().read(name, namespace, **kwargs)

    def list_all(self, **kwargs):
        services = super().list_all(**kwargs)
        return V1DeploymentList(items=services)

    def list(self, namespace: str, **kwargs):
        services = super().list(namespace, **kwargs)
        return V1DeploymentList(items=services)

    def patch(
        self, name: str, namespace: str, body: MockV1Deployment, **kwargs
    ):
        try:
            return super().patch(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `patch_namespaced_deployment`"
            )

    def replace(
        self, name: str, namespace: str, body: MockV1Deployment, **kwargs
    ):
        try:
            return super().replace(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `replace_namespaced_deployment`"
            )

    def delete(self, name: str, namespace: str, **kwargs):
        return super().delete(name, namespace, **kwargs)
