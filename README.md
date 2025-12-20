# LangChain on AWS Lambda (Python)

A small hobby example showing how to run a simple LangChain prompt using OpenAI from an AWS Lambda container image exposed via API Gateway.

## Quick start

1. Create an OpenAI API key and set it locally:

   ```bash
   export OPENAI_API_KEY="sk-..."
   export OPENAI_MODEL="gpt-3.5-turbo"  # optional
   ```

2. Build the container image and push to ECR (SAM expects an image URI in `template.yaml`):

   ```bash
   docker build -t langchain-lambda:latest .
   # create ECR repo, tag and push (replace with your account/region)
   ```

3. Update `template.yaml` with your ECR image URI, then deploy with SAM / CloudFormation.

## Local testing

- Run unit tests:

  ```bash
  pip install -r requirements.txt
  pytest -q
  ```

- You can invoke `handler.lambda_handler` directly for quick checks.

## Cost & billing tips (hobby)

- Use `gpt-3.5-turbo` or small models to keep costs low. Limit `max_tokens` from the client.
- The handler enforces a `max_tokens` upper bound of 1024.
- For repeated prompts, the example includes an in-memory LRU cache to avoid repeated API calls during development.

## Environment variables

- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (optional, defaults to `gpt-3.5-turbo`)

## Next steps

- Add Secret Manager or Parameter Store integration to store credentials securely. (Implemented)
- Add CI to build/publish the container image to ECR automatically. (Implemented example)

---

## Deploying with AWS SAM (basic flow)

1. Build and push an image to ECR:

   ```bash
   # Example: tag and push; use your account/region/repo
   docker build -t langchain-lambda:latest .
   # create repo and push (example steps omitted)
   ```

2. Set the `ImageUri` parameter and deploy with SAM:

   ```bash
   sam deploy --template-file template.yaml --stack-name langchain-lambda \
     --parameter-overrides ImageUri=123456789012.dkr.ecr.us-east-1.amazonaws.com/langchain:latest \
     --capabilities CAPABILITY_IAM
   ```

3. If you're using Secrets Manager, store a secret containing either the raw API key or a JSON object with `OPENAI_API_KEY`:

   ```bash
   aws secretsmanager create-secret --name my-openai-key --secret-string "sk-..."
   # or
   aws secretsmanager create-secret --name my-openai-json --secret-string '{"OPENAI_API_KEY":"sk-..."}'
   ```

   Then deploy with `OpenAISecretName` pointing to that secret name or ARN.

## Using the Secrets Manager integration

- The Lambda will first look for `OPENAI_API_KEY` in the environment for local dev convenience.
- If unset, and if `OPENAI_SECRET_NAME` is set, the function will try to fetch the secret from AWS Secrets Manager and read either the raw string or the `OPENAI_API_KEY` field from a JSON secret.

---

## CI / GitHub Actions example

A basic workflow is included (`.github/workflows/deploy.yml`) to build, tag and push the image, then run `sam deploy`. You will need to set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, and `ECR_REPOSITORY` as repository secrets.

