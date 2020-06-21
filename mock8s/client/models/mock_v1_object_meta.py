# from kubernetes.client.models.v1_object_meta import V1ObjectMeta
import six
import pprint
import uuid


class MockV1ObjectMeta:
    openapi_types = {
        "annotations": "dict(str, str)",
        "cluster_name": "str",
        "creation_timestamp": "datetime",
        "deletion_grace_period_seconds": "int",
        "deletion_timestamp": "datetime",
        "finalizers": "list[str]",
        "generate_name": "str",
        "generation": "int",
        "initializers": "V1Initializers",
        "labels": "dict(str, str)",
        "managed_fields": "list[V1ManagedFieldsEntry]",
        "name": "str",
        "namespace": "str",
        "owner_references": "list[V1OwnerReference]",
        "resource_version": "str",
        "self_link": "str",
        "uid": "str",
    }

    def __init__(
        self,
        annotations=None,
        cluster_name=None,
        creation_timestamp=None,
        deletion_grace_period_seconds=None,
        deletion_timestamp=None,
        finalizers=None,
        generate_name=None,
        generation=None,
        initializers=None,
        labels=None,
        managed_fields=None,
        name=None,
        namespace=None,
        owner_references=None,
        resource_version=None,
        self_link=None,
        uid=None,
    ):
        self.annotations = annotations
        self._annotations = self.annotations

        self.cluster_name = cluster_name
        self._cluster_name = self.cluster_name

        self.creation_timestamp = creation_timestamp
        self._creation_timestamp = self.creation_timestamp

        self.deletion_grace_period_seconds = deletion_grace_period_seconds
        self._deletion_grace_period_seconds = (
            self.deletion_grace_period_seconds
        )

        self.deletion_timestamp = deletion_timestamp
        self._deletion_timestamp = self.deletion_timestamp

        self.finalizers = finalizers
        self._finalizers = self.finalizers

        self.generate_name = generate_name
        self._generate_name = self.generate_name

        self.generation = generation
        self._generation = self.generation

        self.initializers = initializers
        self._initializers = self.initializers

        self.labels = labels
        self._labels = self.labels

        self.managed_fields = managed_fields
        self._managed_fields = self.managed_fields

        self.name = name
        self._name = self.name

        self.namespace = namespace
        self._namespace = self.namespace

        self.owner_references = owner_references
        self._owner_references = self.owner_references

        self.resource_version = resource_version
        self._resource_version = self.resource_version

        self.self_link = self_link
        self._self_link = self.self_link

        if uid:
            self.uid = uid
        else:
            self.uid = str(uuid.uuid4())
        self._uid = self.uid

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value,
                    )
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MockV1ObjectMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
