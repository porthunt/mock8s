import os
from kubernetes.config.config_exception import ConfigException


class MockConfig:

    @staticmethod
    def load_kube_config(config_file=None, context=None,
                         client_configuration=None,
                         persist_config=True):
        pass

    @staticmethod
    def list_kube_config_contexts(config_file=None):
        pass

    @staticmethod
    def new_client_from_config(config_file=None, context=None,
                               persist_config=True):
        pass

    @staticmethod
    def incluster_config():
        pass
