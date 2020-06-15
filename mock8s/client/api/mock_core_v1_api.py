from mock8s.client.models.mock_v1_service_list import MockV1ServiceList


class MockCoreV1Api():

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ""  # ApiClient()
        self.api_client = api_client

    @staticmethod
    def list_service_for_all_namespaces():
        return MockV1ServiceList()
