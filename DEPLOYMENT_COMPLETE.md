# LangChain + OpenAI Lambda Deployment - COMPLETE ✅

## Status
**LIVE AND OPERATIONAL** - Lambda function successfully deployed and responding to API requests.

## API Endpoint
```
https://odlpp1br7j.execute-api.ca-west-1.amazonaws.com/Prod/langchain
```

## Deployment Details

### Infrastructure
- **AWS Region**: ca-west-1
- **Lambda Runtime**: Python 3.11 (container image)
- **Memory**: 512 MB
- **Timeout**: 30 seconds
- **Execution Role**: `LangChainExecutionRole` (with ECR + Secrets Manager permissions)

### Build & Deployment
- **Source**: GitHub (GarethLW/lambda-langchain)
- **CI/CD**: GitHub Actions with OIDC authentication
- **Container Registry**: AWS ECR (274196731158.dkr.ecr.ca-west-1.amazonaws.com/langchain-lambda)
- **IaC**: AWS SAM (Serverless Application Model)
- **API Gateway**: Automatically created by SAM

### Key Fixes Applied
1. **ECR Repository Policy** - Set resource-based policy to allow Lambda service and account root access to pull images
2. **Increased Lambda Memory** - Changed from 128 MB to 512 MB to handle cold starts and LangChain initialization
3. **Extended Timeout** - Set to 30 seconds to allow OpenAI API calls to complete
4. **Separate IAM Role** - Created dedicated `LangChainExecutionRole` with:
   - AWSLambdaBasicExecutionRole (CloudWatch Logs)
   - Custom ECR access policy (GetAuthorizationToken, BatchGetImage, GetDownloadUrlForLayer, BatchCheckLayerAvailability)
   - Custom Secrets Manager access policy (GetSecretValue)

## Usage

### Request Format
```bash
curl -X POST "https://odlpp1br7j.execute-api.ca-west-1.amazonaws.com/Prod/langchain" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your question here?", "max_tokens": 150}'
```

### Response Format
```json
{
  "result": "Response from OpenAI's GPT model..."
}
```

### Example Requests

**Simple arithmetic:**
```bash
curl -X POST "https://odlpp1br7j.execute-api.ca-west-1.amazonaws.com/Prod/langchain" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 2+2?"}'
```
Response: `{"result": "2 + 2 equals 4."}`

**Complex question:**
```bash
curl -X POST "https://odlpp1br7j.execute-api.ca-west-1.amazonaws.com/Prod/langchain" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum entanglement in one sentence."}'
```
Response: `{"result": "Quantum entanglement is a phenomenon where two or more particles become connected in such a way that the state of one particle instantly affects the state of the other, regardless of the distance between them."}`

## Configuration

### Environment Variables (Lambda)
- `OPENAI_MODEL`: gpt-3.5-turbo (default, can be overridden in template)
- `OPENAI_SECRET_NAME`: my-openai-key (reference to AWS Secrets Manager secret)
- `AWS_REGION`: ca-west-1

### GitHub Actions Secrets (Required for CI/CD)
- `AWS_REGION`: ca-west-1
- `ECR_REPOSITORY`: 274196731158.dkr.ecr.ca-west-1.amazonaws.com/langchain-lambda
- `OPENAI_SECRET_NAME`: my-openai-key

### AWS Secrets Manager
- Secret Name: `my-openai-key`
- Secret Value: OpenAI API key (raw string)
- Region: ca-west-1

## Deployment History

### Issues Resolved
1. ✅ Stack deletion timing - Implemented polling to ensure full deletion before redeployment
2. ✅ IAM permissions - Added 11+ permissions to GitHubActionsRole for CloudFormation operations
3. ✅ Lambda ECR access denied - Fixed with:
   - ECR repository resource-based policy
   - Separate IAM execution role with explicit ECR permissions
   - Added BatchCheckLayerAvailability action
4. ✅ Lambda timeout - Increased from 3s default to 30s, memory from 128MB to 512MB

### Successful Deployments
- Run ID: 21235433371 - ✅ Success (with increased memory/timeout)
- Run ID: 21197525917 - ✅ Success (with ECR repository policy)

## CloudFormation Stack
- **Stack Name**: langchain-lambda
- **Status**: CREATE_COMPLETE
- **Resources**:
  - LangChainExecutionRole (IAM::Role)
  - LangChainFunction (Lambda::Function with API Gateway integration)
  - ServerlessRestApi (API Gateway::RestApi)
  - ServerlessRestApiProdStage (API Gateway::Stage)

## Next Steps (Optional)
1. **Custom Domain**: Add a custom domain name via API Gateway
2. **Monitoring**: Set up CloudWatch alarms for Lambda errors/throttling
3. **Caching**: Enable API Gateway caching for repeated queries
4. **Scaling**: Configure Reserved Concurrency to ensure consistent performance
5. **Logging**: Archive Lambda logs to S3 for long-term analysis

## Files of Note
- `template.yaml` - SAM template with Lambda + API Gateway + IAM role
- `.github/workflows/deploy.yml` - GitHub Actions CI/CD workflow
- `handler.py` - Lambda entry point
- `chain.py` - LangChain integration
- `aws_secrets.py` - OpenAI API key retrieval from Secrets Manager
- `Dockerfile` - Container image definition

---

**Deployed**: January 21, 2026 | **Region**: ca-west-1 | **Account**: 274196731158
