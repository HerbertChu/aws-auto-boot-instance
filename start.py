import boto3
import time

# Enter the region your instances are in, e.g. 'us-east-1'

region = 'ap-southeast-1'

# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']

instances = ['i-9b2367cd','i-0bbab165eac50b50c']

web_instance = 'i-9b2367cd'

vpc_id = 'vpc-57a0bc32'

vpc_security_group_id = ['sg-3526a852']

elastic_ip = '54.251.37.241'
 

def lambda_handler(event, context):

    ec2 = boto3.client('ec2', region_name=region)

    response = ec2.start_instances(InstanceIds=instances)

    print 'FINISH started instances: ' + str(response)
    
    print '=========================================='
    
    status = '0'
    
    while status != '16' :
        print 'Wait for running state ...'
        time.sleep(2)
        response = ec2.describe_instance_status(InstanceIds=instances)
        print 'Response : '+str(response)
        if len(response['InstanceStatuses']):
            status = str(response['InstanceStatuses'][0]['InstanceState']['Code'])
            print 'Status : ' + str(response['InstanceStatuses'][0]['InstanceState']['Code'])
    
    print '=========================================='
    
    response = ec2.associate_address(
        InstanceId=web_instance,
        PublicIp=elastic_ip
    )
    
    print 'FINISH associate elastic ip: ' + str(response)
    
    print '=========================================='

    
    response = ec2.attach_classic_link_vpc(
        InstanceId=web_instance,
        VpcId=vpc_id,
        Groups=vpc_security_group_id
    )
    
    print 'FINISH attach class link: ' + str(response)
