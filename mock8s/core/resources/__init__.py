from kubernetes.client.rest import ApiException
from kubernetes.client.models.v1_object_meta import V1ObjectMeta


class Resources:
    def __init__(self):
        self._namespaced_items = {"default": set()}
        self._items = set()

    @staticmethod
    def _label_in_resource(resource, label_selector: str):
        if resource.metadata.labels:
            labels = [
                "{}={}".format(key, value)
                for key, value in resource.metadata.labels.items()
            ]
            for label in labels:
                if label_selector.startswith(label):
                    return True

        return False

    @staticmethod
    def _field_in_resource(resource, field_selector: str):
        if not field_selector:
            return False

        if not field_selector.startswith(
            "metadata.name"
        ) and not field_selector.startswith("metadata.namespace"):
            raise ApiException(400, "Bad Request")

        selector_name = "metadata.name={}".format(resource.metadata.name)
        selector_namespace = "metadata.namespace={}".format(
            resource.metadata.namespace
        )

        if (
            field_selector == selector_name
            or field_selector == selector_namespace
        ):
            return True

        return False

    def create(self, namespace: str, body, **kwargs):
        if not body:
            raise ValueError

        body.metadata = dict(body.metadata, **{"namespace": namespace})
        body.metadata = V1ObjectMeta(**body.metadata)

        if namespace not in self._namespaced_items:
            raise ApiException(404, "Not Found")

        if body in self._namespaced_items[namespace]:
            raise ApiException(409, "AlreadyExists")
        self._items.add(body)
        self._namespaced_items[namespace].add(body)
        return body

    def read(self, name: str, namespace: str, **kwargs):  # noqa
        if namespace not in self._namespaced_items:
            raise ApiException(404, "Not Found")

        for resource in self._namespaced_items[namespace]:
            if resource.metadata.name == name:
                return resource
        else:
            raise ApiException(404, "Not Found")

    def list_all(self, **kwargs):
        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        resources = []

        if not label_selector and not field_selector:
            resources = self._items
        else:
            for resource in self._items:
                if label_selector and field_selector:
                    if self._label_in_resource(
                        resource, label_selector
                    ) and self._field_in_resource(resource, field_selector):
                        resources.append(resource)
                elif label_selector:
                    if self._label_in_resource(resource, label_selector):
                        resources.append(resource)
                elif field_selector:
                    if self._field_in_resource(resource, field_selector):
                        resources.append(resource)

        return resources

    def list(self, namespace: str, **kwargs):
        if namespace not in self._namespaced_items:
            raise ApiException(404, "Not Found")

        label_selector = kwargs.get("label_selector")
        field_selector = kwargs.get("field_selector")

        services = []

        if not label_selector and not field_selector:
            services = self._namespaced_items[namespace]
        else:
            for service in self._namespaced_items[namespace]:
                if label_selector and field_selector:
                    if self._label_in_resource(
                        service, label_selector
                    ) and self._field_in_resource(service, field_selector):
                        services.append(service)
                elif label_selector:
                    if self._label_in_resource(service, label_selector):
                        services.append(service)
                elif field_selector:
                    if self._field_in_resource(service, field_selector):
                        services.append(service)

        return services

    def patch(self, name: str, namespace: str, body, **kwargs):
        if namespace not in self._namespaced_items:
            raise ApiException(404, "Not Found")

        if not body:
            raise ValueError

        body.metadata = dict(body.metadata, **{"namespace": namespace})
        body.metadata = V1ObjectMeta(**body.metadata)

        for resource in self._namespaced_items[namespace]:
            if resource.metadata.name == name:
                self._namespaced_items[namespace].remove(resource)
                self._items.remove(resource)
                break
        else:
            raise ApiException(404, "Not Found")

        if hasattr(body, "metadata"):
            resource.metadata = body.metadata

        if hasattr(body, "spec"):
            resource.spec = body.spec

        if hasattr(body, "status"):
            resource.status = body.status

        self._namespaced_items[namespace].add(resource)
        self._items.add(resource)
        return resource

    def replace(self, name: str, namespace: str, body, **kwargs):
        if namespace not in self._namespaced_items:
            raise ApiException(404, "Not Found")

        if not body:
            raise ValueError

        for service in self._namespaced_items[namespace]:
            if service.metadata.name == name:
                self._namespaced_items[namespace].remove(service)
                self._items.remove(service)
                break
        else:
            raise ApiException(404, "Not Found")

        return self.create(namespace, body)

    def delete(self, name: str, namespace: str, **kwargs):
        if namespace not in self._namespaced_items.keys():
            raise ApiException(404, "Not Found")

        for service in self._items:
            if service.metadata.name == name:
                self._items.remove(service)
                self._namespaced_items[namespace].remove(service)
                break
        else:
            raise ApiException(404, "Not Found")
