import os

from aws_secrets import get_openai_api_key


def test_env_precedence(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    import aws_secrets
    aws_secrets._cache.clear()
    assert get_openai_api_key() == "env-key"


def test_no_env_no_secret(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_SECRET_NAME", raising=False)
    import aws_secrets
    aws_secrets._cache.clear()
    assert get_openai_api_key() is None
