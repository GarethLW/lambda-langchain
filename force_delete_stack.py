#!/usr/bin/env python3
import boto3
import time
import sys

cf = boto3.client('cloudformation', region_name='ca-west-1')
stack_name = 'langchain-lambda'

try:
    # Get stack details
    response = cf.describe_stacks(StackName=stack_name)
    stack = response['Stacks'][0]
    status = stack['StackStatus']
    print(f"Current stack status: {status}")
    
    # Try to delete
    print("Attempting to delete stack...")
    cf.delete_stack(StackName=stack_name)
    
    # Wait and check
    print("Waiting for deletion...")
    for i in range(60):
        try:
            response = cf.describe_stacks(StackName=stack_name)
            current_status = response['Stacks'][0]['StackStatus']
            print(f"  [{i+1}] Status: {current_status}")
            if 'DELETE_COMPLETE' in current_status or not response.get('Stacks'):
                print("Stack deleted successfully")
                sys.exit(0)
            time.sleep(1)
        except cf.exceptions.ClientError as e:
            if 'does not exist' in str(e):
                print("Stack deleted successfully")
                sys.exit(0)
            else:
                print(f"Error: {e}")
                raise
    
    print("Timeout waiting for stack deletion")
    sys.exit(1)
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
