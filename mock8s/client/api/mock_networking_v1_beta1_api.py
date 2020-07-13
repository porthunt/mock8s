from mock8s.core.resources.ingresses import Ingresses


class MockNetworkingV1beta1Api:
    def __init__(self, api_client=None):
        self.api_client = api_client if api_client else ""
        self.ingress = Ingresses()

    def create_namespaced_ingress(self, namespace, body, **kwargs):
        return self.ingress.create(namespace, body, **kwargs)

    def read_namespaced_ingress(self, name, namespace, **kwargs):
        return self.ingress.read(name, namespace, **kwargs)

    def list_ingress_for_all_namespaces(self, **kwargs):
        return self.ingress.list_all(**kwargs)

    def list_namespaced_ingress(self, namespace, **kwargs):
        return self.ingress.list(namespace, **kwargs)

    def patch_namespaced_ingress(self, name, namespace, body, **kwargs):
        return self.ingress.patch(name, namespace, body, **kwargs)

    def replace_namespaced_ingress(self, name, namespace, body, **kwargs):
        return self.ingress.replace(name, namespace, body, **kwargs)

    def delete_namespaced_ingress(self, name, namespace, **kwargs):
        return self.ingress.delete(name, namespace, **kwargs)
