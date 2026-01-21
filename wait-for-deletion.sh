#!/bin/bash
STACK_NAME="langchain-lambda"
REGION="ca-west-1"
MAX_ATTEMPTS=60
ATTEMPT=0

echo "Starting deletion check for stack: $STACK_NAME"

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  RESPONSE=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --region $REGION 2>&1)
  
  if echo "$RESPONSE" | grep -q "does not exist"; then
    echo "✓ Stack successfully deleted"
    exit 0
  fi
  
  STATUS=$(echo "$RESPONSE" | grep "StackStatus" | grep -o '"[^"]*"$' | tr -d '"')
  echo "[$ATTEMPT/$MAX_ATTEMPTS] Stack status: $STATUS"
  
  if [ "$STATUS" = "DELETE_COMPLETE" ]; then
    echo "✓ Stack DELETE_COMPLETE"
    exit 0
  fi
  
  if [[ "$STATUS" =~ "DELETE_FAILED" ]]; then
    echo "✗ Stack in DELETE_FAILED state"
    exit 1
  fi
  
  ATTEMPT=$((ATTEMPT + 1))
  sleep 5
done

echo "✗ Timeout waiting for stack deletion"
exit 1
