# Amazon Simple Queue Service

[Amazon Simple Queue Service](https://aws.amazon.com/sqs/) (SQS) is a 
[message queue](https://en.wikipedia.org/wiki/Message_queue) in AWS. 

The goal here is to show how to build systems where tasks are put into the queue and handled by Lambda at some point.
The main benefit here is to split the app into smaller parts that can be more independent.
You can update the lambda and the message queue will retry the task if your lambda is down.

> Amazon SQS guarantees at-least-once delivery. 
> Messages are stored on multiple servers for redundancy and to ensure availability. 
> If a message is delivered while a server is not available, 
> it may not be removed from that server's queue and may be resent.

Another key consideration is that Amazon SQS is a distributed system. This means that the message is in the queue
until the consumer deletes it. This means that more than one consumer can process the same message.
The mechanism to control this is 
[visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html).

> Amazon SQS sets a visibility timeout, a period of time during which Amazon SQS prevents all consumers 
> from receiving and processing the message. The default visibility timeout for a message is 30 seconds. 
> The minimum is 0 seconds. The maximum is 12 hours.


## Prerequisites

I did the Lambda first and I am using the access key because it works for me. 
This adds this part: `--profile mydemouser` to aws commands.

## More about SQS with lambda

https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html

## How to create your queue

```
create-queue --queue-name MySuperDuperQueue 
```
