from kubernetes import config, client
from mock8s import mock8s
import yaml

manifest = """
    apiVersion: v1
    kind: Service
    metadata:
      name: foobar
      labels:
        "group": "abc"
    spec:
      selector:
        app: "barbaz"
      ports:
        - protocol: TCP
          port: 80
          targetPort: 80
"""

@mock8s
def foobar():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    body = yaml.load(manifest, Loader=yaml.FullLoader)
    a = v1.create_namespaced_service("default", body=body)
    services = v1.list_service_for_all_namespaces(label_selector="abc")
    return "abc"


print(foobar())
