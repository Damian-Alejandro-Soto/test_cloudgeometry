import os
import json
import boto3
from botocore.exceptions import ClientError

def get_stack_status(stack_name):
    # Create a boto3 CloudFormation client
    cloudformation = boto3.client('cloudformation')
    
    try:
        # Get stack details
        response = cloudformation.describe_stacks(StackName=stack_name)
        stack = response['Stacks'][0]
        stack_status = stack['StackStatus']
        
        # Prepare the result dictionary
        result = {
            "StackName": stack_name,
            "StackStatus": stack_status
        }
        
        # If the stack is in a rollback state, check for failure reasons
        if 'ROLLBACK' in stack_status:
            events = cloudformation.describe_stack_events(StackName=stack_name)['StackEvents']
            for event in events:
                if event['ResourceStatus'] in ['CREATE_FAILED', 'UPDATE_FAILED', 'DELETE_FAILED'] and 'ROLLBACK' in event['ResourceStatusReason']:
                    resource_name = event['LogicalResourceId']
                    error_message = event.get('ResourceStatusReason', 'No error message provided.')
                    
                    result['RollbackTriggeredBy'] = {
                        "ResourceName": resource_name,
                        "ErrorMessage": error_message
                    }
                    
                    # Check if the resource is a nested stack
                    if event['ResourceType'] == 'AWS::CloudFormation::Stack':
                        nested_stack_name = event['PhysicalResourceId']
                        nested_result = get_stack_status(nested_stack_name)
                        result['NestedStackError'] = nested_result
                    
                    break
        
        # Output the result as JSON
        print(json.dumps(result, indent=4))
    
    except ClientError as e:
        print(json.dumps({"Error": str(e)}, indent=4))

if __name__ == '__main__':
    # Stack name passed as an input
    stack_name = input("Enter CloudFormation Stack Name: ")
    
    # Get stack status
    get_stack_status(stack_name)



