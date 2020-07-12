# mock8s - Mock Kubernetes
`mock8s` is an easy way to test your kubernetes resources.

## Summary
```python
def delete_service(namespace):
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    api_instance.delete_namespaced_service("foobar", "default")
```

Using the previous code, `kubernetes-client` will try to delete the resource `Service` with the name "foobar". If you want to have a unit test for this, you don't want your test to actually modify your cluster. To avoid this situation, you can use `mock8s`.

Simply add a decorator `@mock8s` and mock8s will mock the cluster for you. So you can simply use

```python
@mock8s
def delete_service(namespace):
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    api_instance.delete_namespaced_service("foobar", "default")
```

With this decorator, all the supported interactions with the cluster are mocked.

## Support
Check the [wiki page](https://github.com/porthunt/mock8s/wiki) to verify if the class/method you want to test is supported.

## Install
Since mock8s is still not available on pip, you can install it using:
```
$ pip install git+https://https://github.com/porthunt/mock8s.git@0.1.0
```
