import json
import os

import chain


def _response(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """Simple AWS Lambda handler for API Gateway Proxy events.

    Expects JSON body: {"prompt": "...", "max_tokens": 150}
    Uses `OPENAI_API_KEY` from environment.
    """
    # Handle CORS preflight OPTIONS requests
    http_method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")
    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    try:
        # Debug logging
        print(f"Event: {json.dumps(event)}")
        
        body = event.get("body") if isinstance(event, dict) else None
        if isinstance(body, str):
            data = json.loads(body) if body else {}
        elif isinstance(body, dict):
            data = body
        else:
            data = {}

        # Fallback to query string parameters for quick testing in browser
        if not data:
            data = event.get("queryStringParameters") or {}

        prompt = data.get("prompt")
        if not prompt:
            return _response(400, {"error": "Missing 'prompt' in request body"})

        max_tokens = int(data.get("max_tokens", 150))
        # enforce an upper bound to avoid runaway billing
        if max_tokens > 1024:
            max_tokens = 1024

        result = chain.get_completion(prompt, max_tokens=max_tokens)
        return _response(200, {"result": result})

    except Exception as e:
        return _response(500, {"error": str(e)})
