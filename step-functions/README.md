# Amazon Step Functions

Step functions allow you to orchestrate complex workflows.

I removed my accounts from the files so be sure to replace all the `<account>` parts with your account id.

This step function calls two lambdas and maps the outputs to inputs in between.

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

First you need to create a role for the step function.

```
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser iam create-role \
>   --role-name StepFunctions-MyFirstStateMachine-role \
>   --assume-role-policy-document "$(<iam_role_definition.json)"
{
    "Role": {
        "Path": "/",
        "RoleName": "StepFunctions-MyFirstStateMachine-role",
        "RoleId": "AROAVDTUAHFNZM5R22B7D",
        "Arn": "arn:aws:iam::<account>:role/StepFunctions-MyFirstStateMachine-role",
        "CreateDate": "2024-02-28T07:47:12+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": [
                            "states.amazonaws.com"
                        ]
                    },
                    "Action": "sts:AssumeRole",
                    "Condition": {
                        "ArnLike": {
                            "aws:SourceArn": "arn:aws:states:us-east-1:<account>:stateMachine:*"
                        },
                        "StringEquals": {
                            "aws:SourceAccount": "<account>"
                        }
                    }
                }
            ]
        }
    }
}
~/Work/aws-playground/step-functions [main] $
```

Then you can create the state machine

```
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser stepfunctions \
>    create-state-machine \
>    --name MyFirstStateMachine \
>    --definition "$(<stepfunction_definition.json)" \
>    --role-arn arn:aws:iam::<account>:role/StepFunctions-MyFirstStateMachine-role
{
    "stateMachineArn": "arn:aws:states:us-east-1:<account>:stateMachine:MyFirstStateMachine",
    "creationDate": "2024-02-28T09:52:18.799000+02:00"
}
~/Work/aws-playground/step-functions [main] $
```

and run the function

```
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser stepfunctions \
>    start-execution \
>    --state-machine-arn arn:aws:states:us-east-1:<account>:stateMachine:MyFirstStateMachine \
>    --input '{"payload": "hi mom"}'
{
    "executionArn": "arn:aws:states:us-east-1:<account>:execution:MyFirstStateMachine:<hash>",
    "startDate": "2024-02-28T09:59:50.092000+02:00"
}
~/Work/aws-playground/step-functions [main] $ aws --profile mydemouser stepfunctions \
>     describe-execution \
>     --execution-arn arn:aws:states:us-east-1:<account>:execution:MyFirstStateMachine:<hash>
{
    "executionArn": "arn:aws:states:us-east-1:<account>:execution:MyFirstStateMachine:<hash>",
    "stateMachineArn": "arn:aws:states:us-east-1:<account>:stateMachine:MyFirstStateMachine",
    "name": "<hash>",
    "status": "SUCCEEDED",
    "startDate": "2024-02-28T12:11:53.809000+02:00",
    "stopDate": "2024-02-28T12:11:55.169000+02:00",
    "input": "{\"payload\": \"hi mom\"}",
    "inputDetails": {
        "included": true
    },
    "output": "{\"statusCode\":200,\"headers\":{\"Access-Control-Allow-Origin\":\"*\",\"Access-Control-Allow-Methods\":\"GET, POST, PUT, DELETE, OPTIONS\",\"content-type\":\"application/json\"},\"body\":{\"payload\":\"MOM IH\"}}",
    "outputDetails": {
        "included": true
    },
    "redriveCount": 0,
    "redriveStatus": "NOT_REDRIVABLE",
    "redriveStatusReason": "Execution is SUCCEEDED and cannot be redriven"
}
~/Work/aws-playground/step-functions [main] $
```
