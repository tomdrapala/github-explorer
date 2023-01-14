import pytest
import requests


@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    # Making sure that no requestes to external API will be sent during tests
    # in case there is a breach in mocking.
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())
