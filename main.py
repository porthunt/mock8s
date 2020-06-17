from kubernetes import config, client
from mock8s import mock8s

@mock8s
def foobar():
    #config.load_kube_config()
    v1 = client.CoreV1Api()
    services = v1.list_service_for_all_namespaces()
    return "abc"


print(foobar())
