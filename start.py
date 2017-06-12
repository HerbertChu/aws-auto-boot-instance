import boto3
import time

# Enter the region your instances are in, e.g. 'us-east-1'

region = ''

# Enter your instances here which need to bootup
# ex. ['X-XXXXXXXX', 'X-XXXXXXXX']

instances = []

# Enter your web-instances which access by public 
# ex. ['X-XXXXXXXX', 'X-XXXXXXXX']

web_instance = ''

# Enter your vpc id here which may connect to any private network
vpc_id = ''

# Enter the security group which apply to vpc

vpc_security_group_id = ['']

# Enter your elastic ip here which access by public area
elastic_ip = ''
 

def lambda_handler(event, context):

    ec2 = boto3.client('ec2', region_name=region)

    response = ec2.start_instances(InstanceIds=instances)

    print 'FINISH started instances: ' + str(response)
    
    print '=========================================='
    
    status = '0'
    
    # wait for the vm running state in case the following cmd fail
    # the vpc attachment and the elastic ip associate require the vm running state
    
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
