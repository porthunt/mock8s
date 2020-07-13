import copy
from mock8s.core.resources import Resources
from mock8s.client.models.mock_v1_pod import MockV1Pod
from kubernetes.client.models.v1_pod_list import V1PodList
from kubernetes.client.models.v1_pod_spec import V1PodSpec
from kubernetes.client.models.v1_pod_status import V1PodStatus


class Pods(Resources):
    def __init__(self):
        super().__init__()

    def create(self, namespace: str, body: MockV1Pod, **kwargs):
        if not body:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_pod`"
            )

        body = copy.copy(body)
        body.spec = V1PodSpec(**body.spec)
        body.status = V1PodStatus(**body.status)
        try:
            return super().create(namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `create_namespaced_pod`"
            )

    def read(self, name: str, namespace: str, **kwargs):
        return super().read(name, namespace, **kwargs)

    def list_all(self, **kwargs):
        pods = super().list_all(**kwargs)
        return V1PodList(items=pods)

    def list(self, namespace: str, **kwargs):
        pods = super().list(namespace, **kwargs)
        return V1PodList(items=pods)

    def patch(self, name: str, namespace: str, body: MockV1Pod, **kwargs):
        try:
            return super().patch(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `patch_namespaced_pod`"
            )

    def replace(self, name: str, namespace: str, body: MockV1Pod, **kwargs):
        try:
            return super().replace(name, namespace, body, **kwargs)
        except ValueError:
            raise ValueError(
                "Missing the required parameter `body` "
                "when calling `replace_namespaced_pod`"
            )

    def delete(self, name: str, namespace: str, **kwargs):
        return super().delete(name, namespace, **kwargs)
