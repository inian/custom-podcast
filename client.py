import boto3
client = boto3.client('lambda')

input = open('input.json')

response = client.invoke(
    FunctionName='xx',
    InvocationType='Event',
    LogType='None',
    Payload=input
)

print response