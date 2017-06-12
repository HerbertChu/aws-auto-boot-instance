import boto3

# Enter the region your instances are in, e.g. 'us-east-1'

region = ''

# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']

instances = []


def lambda_handler(event, context):

    ec2 = boto3.client('ec2', region_name=region)
    #ec2 = boto3.client('ec2')
    response = ec2.stop_instances(InstanceIds=instances)
    print 'response: ' + str(response)
    print 'stopped your instances: ' + str(instances)
