import pytest
import kubernetes
import mock8s


@pytest.fixture
def clientpatch(monkeypatch):
    monkeypatch.setattr(kubernetes.client, "CoreV1Api", mock8s.MockCoreV1Api)



def test_abc(clientpatch):

