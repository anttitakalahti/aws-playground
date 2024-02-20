# aws-playground

This project is mainly for me to learn how the basic building blocks work. 

I'll try to use the [AWS always free tier](https://aws.amazon.com/free/) to do these.

All of this is written in Feb 2024.

I wanted to explore how to build a decoupled [serverless system](https://aws.amazon.com/serverless/).
The main selling point for me would be to allow changing of parts without touching other systems.
SQS example is a login service which allows you to log in without knowing if the credentials are in
active directory or in database or wherever.

Other idea would be to do [event driven system](https://aws.amazon.com/event-driven-architecture/)
using [EventBridge](https://aws.amazon.com/eventbridge/).

```
~ $ which aws
/usr/local/bin/aws
~ $ aws --version
aws-cli/2.15.18 Python/3.11.6 Darwin/23.2.0 exe/x86_64 prompt/off
~ $
```

## Lambda

lambda folder has everything needed to deploy the lambda

## Simple Queue Service

simple_queue_service part is in progress.


