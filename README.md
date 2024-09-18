## usage:

$ python3 getStack.py

Enter CloudFormation Stack Name: stack-name-001

{

    "StackName": "stack-name-001",
    "StackStatus": "ROLLBACK_COMPLETE"
    
}


$ python3 getStack.py

Enter CloudFormation Stack Name: test-fail-stack

{

    "StackName": "test-fail-stack",
    "StackStatus": "ROLLBACK_FAILED"
    
}


