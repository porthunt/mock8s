import os
from kubernetes.config.kube_config import load_kube_config
from kubernetes.config.config_exception import ConfigException


def load_kube_config(config_file=None, context=None,
                     client_configuration=None,
                     persist_config=True):
    print("A")
