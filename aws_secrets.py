import os
import json
from cachetools import cached, LRUCache

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except Exception:
    boto3 = None
    BotoCoreError = Exception
    ClientError = Exception

_cache = LRUCache(maxsize=4)


@cached(_cache)
def get_openai_api_key() -> str | None:
    """Return OPENAI API key from env or Secrets Manager.

    Priority:
      1. `OPENAI_API_KEY` env var
      2. `OPENAI_SECRET_NAME` secret from AWS Secrets Manager
         - secret value can be the raw key, or a JSON object with `OPENAI_API_KEY`.
    """
    # 1) env var
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key

    # 2) secrets manager
    secret_name = os.environ.get("OPENAI_SECRET_NAME")
    if not secret_name:
        return None

    if boto3 is None:
        return None

    region = os.environ.get("AWS_REGION")
    client = boto3.client("secretsmanager", region_name=region) if region else boto3.client("secretsmanager")

    try:
        resp = client.get_secret_value(SecretId=secret_name)
        secret_str = resp.get("SecretString")
        if not secret_str:
            return None
        try:
            data = json.loads(secret_str)
            return data.get("OPENAI_API_KEY") or data.get("openai_api_key") or data.get("api_key") or data.get("key")
        except json.JSONDecodeError:
            # secret is raw key
            return secret_str
    except (BotoCoreError, ClientError):
        return None
