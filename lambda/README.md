# [AWS Lambda](https://aws.amazon.com/pm/lambda/)

My biggest issue here was how can I make this lambda to fail (at work I have something that fails sometimes).
It took me a while to find the documentation for
[Lambda invoke](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html) where I found that it returns 200
for pretty much all the time.

Biggest lesson learned was to go to the UI to test the lambda to see that it fails when it should.

## Create Lambda

You need to get access to AWS cli. I used access key because it worked for me.
This adds this part: `--profile mydemouser` to aws commands.
If you use other methods some changes might be needed.

```
~ $ aws lambda list-functions

Unable to locate credentials. You can configure credentials by running "aws configure".
~ $ aws configure --profile mydemouser
AWS Access Key ID [None]: <check_this_from_aws>
AWS Secret Access Key [None]: <check_this_from_aws>
Default region name [None]: us-east-1
Default output format [None]:
~ $ aws --profile mydemouser lambda list-functions
{
    "Functions": []
}
~ $
```

This example deploys a python container running lambda to uppercase the input. It fails 50% of the time.

I used [these instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions)
to develop and deploy the container.

```
~/Work/aws-playground/lambda [main] $ docker build --platform linux/amd64 -t lambda-docker-image:test .
...
~/Work/aws-playground/lambda [main] $ docker run -dp 127.0.0.1:3000:8080 lambda-docker-image:test
<hash_removed>
~/Work/aws-playground/lambda [main] $ curl "http://localhost:3000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
{"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS", "content-type": "application/json"}, "body": [{"payload": "HELLO WORLD!"}]}~/Work/aws-playground/lambda [main] $ 
```

login to docker (check value for the <id_removed> in the UI)

```
~/Work/aws-playground/lambda [main] $ aws ecr get-login-password --profile mydemouser --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
Login Succeeded
~/Work/aws-playground/lambda [main] $
```

create the repository

```
~/Work/aws-playground/lambda [main] $ aws ecr --profile mydemouser create-repository --repository-name hello-world --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:<account>:repository/hello-world",
        "registryId": "<id_removed>",
        "repositoryName": "hello-world",
        "repositoryUri": "<id_removed>.dkr.ecr.us-east-1.amazonaws.com/hello-world",
        "createdAt": "2024-02-15T17:06:51.305000+02:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
~/Work/aws-playground/lambda [main] $
```

push the image to ECR

```
~/Work/aws-playground/lambda [main] $ docker tag lambda-docker-image:test <repositoryUri_from_command_above>:latest
~/Work/aws-playground/lambda [main] $ docker push <account>.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest
~/Work/aws-playground/lambda [main] $ aws --profile mydemouser ecr list-images --repository-name hello-world
{
    "imageIds": [
        {
            "imageDigest": "sha256:<hash_removed>",
            "imageTag": "latest"
        }
    ]
}
~/Work/aws-playground/lambda [main] $
```

create role

```
~/Work/aws-playground/lambda [main] $ aws --profile mydemouser iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

{
    "Role": {
        "Path": "/",
        "RoleName": "lambda-ex",
        "RoleId": "<id_removed>",
        "Arn": "arn:aws:iam::<account>:role/lambda-ex",
        "CreateDate": "2024-02-15T15:25:18+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
}
~/Work/aws-playground/lambda [main] $
```

create the lambda

```
~/Work/aws-playground/lambda [main] $ aws --profile mydemouser lambda create-function --function-name hello-world --package-type Image --code ImageUri=<account>.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest --role arn:aws:iam::<account>:role/lambda-ex
{
    "FunctionName": "hello-world",
    "FunctionArn": "arn:aws:lambda:us-east-1:<account>:function:hello-world",
    "Role": "arn:aws:iam::<account>:role/lambda-ex",
    "CodeSize": 0,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2024-02-15T15:26:22.890+0000",
    "CodeSha256": "<hash_removed>",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "<id_removed>",
    "State": "Pending",
    "StateReason": "The function is being created.",
    "StateReasonCode": "Creating",
    "PackageType": "Image",
    "Architectures": [
        "x86_64"
    ],
    "EphemeralStorage": {
        "Size": 512
    },
    "SnapStart": {
        "ApplyOn": "None",
        "OptimizationStatus": "Off"
    },
    "LoggingConfig": {
        "LogFormat": "Text",
        "LogGroup": "/aws/lambda/hello-world"
    }
}
~/Work/aws-playground/lambda [main] $
```

test the lambda

```
~/Work/aws-playground/lambda [main] $ aws --profile mydemouser lambda invoke --function-name hello-world response.json
{
"StatusCode": 200,
"ExecutedVersion": "$LATEST"
}
~/Work/aws-playground/lambda [main] $ cat response.json | jq
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "content-type": "application/json"
  },
  "body": [
    {
      "payload": ""
    }
  ]
}
~/Work/aws-playground/lambda [main] $
```

## Update the Lambda

create new tag

```
~/Work/aws-playground/lambda [main] $ docker build --platform linux/amd64 -t lambda-docker-image:test .
...
~/Work/aws-playground/lambda [main] $ docker tag lambda-docker-image:test <account>.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest
```

push the tag to docker to update the hello-world:latest

```
~/Work/aws-playground/lambda [main] $ docker push <account>.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest
The push refers to repository [<account>.dkr.ecr.us-east-1.amazonaws.com/hello-world]
b57213f68876: Layer already exists
cb50e1611d4c: Layer already exists
0d83a183a2ca: Layer already exists
b2fbcdbc3abe: Layer already exists
01237e4b624b: Layer already exists
7393ae547845: Layer already exists
08352d8f528a: Layer already exists
4ad08681a382: Layer already exists
8a302ef602af: Layer already exists
latest: digest: sha256:<hash_removed> size: 2203
~/Work/aws-playground/lambda [main] $ aws --profile mydemouser ecr list-images --repository-name hello-world
{
    "imageIds": [
        {
            "imageDigest": "sha256:<hash_removed>"
        },
        {
            "imageDigest": "sha256:<hash_removed>",
            "imageTag": "latest"
        }
    ]
}
~/Work/aws-playground/lambda [main] $
```

update the lambda to use the new image

```
aws --profile mydemouser lambda update-function-code --image-uri <account>.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest --function-name hello-world
```