import boto3
import time

cf = boto3.client('cloudformation', region_name='ca-west-1')
stack_name = 'langchain-lambda'

try:
    response = cf.describe_stacks(StackName=stack_name)
    stack = response['Stacks'][0]
    status = stack['StackStatus']
    print(f"Stack Status: {status}")
    print(f"Stack ID: {stack['StackId']}")
    
    if 'DELETE_FAILED' in status or 'ROLLBACK_FAILED' in status:
        print(f"\nStack is in {status} state.")
        print("This usually means the stack has resources that couldn't be deleted.")
        print("Manual cleanup via AWS Console may be required.")
        
        # Try to list resources
        try:
            resources = cf.list_stack_resources(StackName=stack_name)
            print(f"\nStack resources ({len(resources.get('StackResourceSummaries', []))} total):")
            for res in resources.get('StackResourceSummaries', []):
                print(f"  - {res['LogicalResourceId']} ({res['ResourceType']}): {res['ResourceStatus']}")
        except Exception as e:
            print(f"Could not list resources: {e}")
            
except cf.exceptions.ClientError as e:
    print(f"Error: {e}")
