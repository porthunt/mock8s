from mock8s.core.resources import Resources
from mock8s.client.models.mock_v1_pod import MockV1Pod
from mock8s.client.models.mock_v1_pod_list import MockV1PodList


class Pods(Resources):
    def __init__(self):
        super().__init__()

    def create(self, namespace: str, body: MockV1Pod, **kwargs):
        return super().create(namespace, body, **kwargs)

    def read(self, name: str, namespace: str, **kwargs):
        return super().read(name, namespace, **kwargs)

    def list_all(self, **kwargs):
        pods = super().list_all(**kwargs)
        return MockV1PodList(items=pods)

    def list(self, namespace: str, **kwargs):
        pods = super().list(namespace, **kwargs)
        return MockV1PodList(items=pods)

    def patch(self, name: str, namespace: str, body: MockV1Pod, **kwargs):
        return super().patch(name, namespace, body, **kwargs)

    def replace(
        self, name: str, namespace: str, body: MockV1Pod, **kwargs
    ):
        return super().replace(name, namespace, body, **kwargs)

    def delete(self, name: str, namespace: str, **kwargs):
        return super().delete(name, namespace, **kwargs)
