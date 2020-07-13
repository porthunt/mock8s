from mock8s.core.resources.deployments import Deployments


class MockAppsV1Api:
    def __init__(self, api_client=None):
        self.api_client = api_client if api_client else ""
        self.deployments = Deployments()

    def create_namespaced_deployment(self, namespace, body, **kwargs):
        return self.deployments.create(namespace, body, **kwargs)

    def read_namespaced_deployment(self, name, namespace, **kwargs):
        return self.deployments.read(name, namespace, **kwargs)

    def list_deployment_for_all_namespaces(self, **kwargs):
        return self.deployments.list_all(**kwargs)

    def list_namespaced_deployment(self, namespace, **kwargs):
        return self.deployments.list(namespace, **kwargs)

    def patch_namespaced_deployment(self, name, namespace, body, **kwargs):
        return self.deployments.patch(name, namespace, body, **kwargs)

    def replace_namespaced_deployment(self, name, namespace, body, **kwargs):
        return self.deployments.replace(name, namespace, body, **kwargs)

    def delete_namespaced_deployment(self, name, namespace, **kwargs):
        return self.deployments.delete(name, namespace, **kwargs)
