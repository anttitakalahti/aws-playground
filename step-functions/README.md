# Amazon Step Functions

My preferred solution for microservice orchestration is step functions.

## Callback pattern example

https://docs.aws.amazon.com/step-functions/latest/dg/callback-task-sample-sqs.html

## Prerequisites

This step functions uses the lambda from lambda folder. I also created another lambda in the UI to reverse payload.

```
~/Work/aws-playground [main] $ aws --profile mydemouser lambda \
  list-functions \
  --query Functions[].[FunctionName,FunctionArn]
[
    [
        "hello-world",
        "arn:aws:lambda:us-east-1:<account>:function:hello-world"
    ],
    [
        "reverse",
        "arn:aws:lambda:us-east-1:<account>:function:reverse"
    ]
]
~/Work/aws-playground [main] $
```

## Create step function

I designed the step function in the GUI. 

I then ran it in the GUI, and it failed like this:
```
User: arn:aws:sts::<account>:assumed-role/StepFunctions-MyStateMachine-<hash_maybe>
is not authorized to perform: lambda:InvokeFunction on resource: 
arn:aws:lambda:us-east-1:<account>:function:hello-world:$LATEST because no identity-based policy allows the 
lambda:InvokeFunction action (Service: AWSLambda; Status Code: 403; Error Code: AccessDeniedException; Request ID: 
<id>; Proxy: null)
```

```
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser stepfunctions list-state-machines
{
    "stateMachines": [
        {
            "stateMachineArn": "arn:aws:states:us-east-1:<account>:stateMachine:<id>",
            "name": "<name>",
            "type": "STANDARD",
            "creationDate": "2024-02-27T11:37:46.683000+02:00"
        }
    ]
}
~/Work/aws-playground/step-functions [main] $
```
run

```
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser stepfunctions \
>   start-execution \
>   --state-machine-arn arn:aws:states:us-east-1:<account>:stateMachine:MyStateMachine-dpumksw4h \
>   --input "{\"payload\": \"hi mom\"}"
{
    "executionArn": "arn:aws:states:us-east-1:<account>:execution:MyStateMachine-dpumksw4h:<hash>",
    "startDate": "2024-02-27T14:07:45.109000+02:00"
}
~/Work/aws-playground/step-functions [main] $
```

This will also fail for the same reason

```
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser iam list-roles --query Roles[].[RoleName,Arn]
[
    ...
    [
        "StepFunctions-MyStateMachine-<name-role-hash>",
        "arn:aws:iam::<account>:role/service-role/StepFunctions-MyStateMachine-<name-role-hash>"
    ]
]
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser iam attach-role-policy \
  --role-name StepFunctions-MyStateMachine-<name-role-hash> \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole
~/Work/aws-playground/step-functions [main] $
```
https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html



https://awscli.amazonaws.com/v2/documentation/api/latest/reference/stepfunctions/create-state-machine.html