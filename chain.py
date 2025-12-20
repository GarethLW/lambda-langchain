import os
from cachetools import LRUCache, cached

from langchain.chat_models import init_chat_model

from aws_secrets import get_openai_api_key


_cache = LRUCache(maxsize=128)


def _make_llm(max_tokens: int = None):
    api_key = get_openai_api_key()
    if not api_key:
        # Fail fast with a clear message so the handler can return an actionable error
        raise RuntimeError("OpenAI API key not found. Set OPENAI_API_KEY or OPENAI_SECRET_NAME in Secrets Manager.")
    model_name = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    # If user provided a bare model name like `gpt-3.5-turbo`, prefix with the provider for init_chat_model
    model_spec = model_name if ":" in model_name else f"openai:{model_name}"
    # Keep temperature low for deterministic results on a hobby budget
    kwargs = {"temperature": 0, "openai_api_key": api_key}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    llm = init_chat_model(model_spec, **kwargs)
    return llm


@cached(_cache)
def get_completion(prompt: str, max_tokens: int = 150) -> str:
    """Return a completion for `prompt`. Uses an in-memory LRU cache to
    reduce repeated calls (useful for development / demos).
    """
    llm = _make_llm(max_tokens=max_tokens)
    # Try to invoke the model and normalize the result to a string
    res = llm.invoke(prompt)
    # Common result shapes: string, object with .content, object with .message, or generations
    if isinstance(res, str):
        return res
    if hasattr(res, "content"):
        return res.content
    if hasattr(res, "message"):
        msg = res.message
        return getattr(msg, "content", getattr(msg, "text", str(res)))
    if hasattr(res, "generations"):
        try:
            return res.generations[0][0].text
        except Exception:
            return str(res)
    return str(res)
