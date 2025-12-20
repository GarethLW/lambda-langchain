import json

import pytest


def test_missing_prompt():
    from handler import lambda_handler

    event = {"body": json.dumps({})}
    resp = lambda_handler(event, None)
    assert resp["statusCode"] == 400


def test_success(monkeypatch):
    import chain

    monkeypatch.setattr(chain, "get_completion", lambda prompt, max_tokens=150: "mocked result")
    from handler import lambda_handler

    event = {"body": json.dumps({"prompt": "hello"})}
    resp = lambda_handler(event, None)
    assert resp["statusCode"] == 200
    body = json.loads(resp["body"])
    assert body["result"] == "mocked result"
