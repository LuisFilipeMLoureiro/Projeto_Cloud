import boto3
from botocore.exceptions import ClientError
import time


def LoadBalancerCreator(Security_Group,lb_name, Name_TG):
    lista_subnets = []
    django = boto3.client('ec2', region_name='us-east-1')
    load_balancer = boto3.client('elbv2', region_name='us-east-1')


    subnet = django.describe_subnets()
    for s in subnet['Subnets']:
        lista_subnets.append(s['SubnetId'])

    

    idSecurityGroup = django.describe_security_groups(GroupNames=[Security_Group])["SecurityGroups"][0]["GroupId"]

    lb = load_balancer.create_load_balancer(
        Scheme='internet-facing',
        Name=lb_name,
        SecurityGroups=[
                idSecurityGroup,
                ],
                Tags=[
                    {
                        'Key': 'Owner',
                        'Value': lb_name
                    },
                    {
                        'Key': 'Name',
                        'Value': lb_name
                    },
                ],

                Subnets= lista_subnets
            )


    describe = django.describe_vpcs()
    res = describe["Vpcs"][0]["VpcId"] 

    target_group = load_balancer.create_target_group(
            Name=Name_TG,
            Protocol="HTTP",
            Port=8080,
            HealthCheckEnabled=True,
            HealthCheckProtocol='HTTP',
            HealthCheckPort='8080',
            HealthCheckPath='/admin/',
            TargetType="instance",
            VpcId=res,
            Matcher={
            'HttpCode': '200,302,301,404,403',
            }
        )
    

    TARGET_GROUP = target_group["TargetGroups"][0]["TargetGroupArn"]

    time.sleep(30)

    load_balancers = load_balancer.describe_load_balancers()
    for i in lb['LoadBalancers']:
        if i['LoadBalancerName'] == lb_name:
            Arn = i['LoadBalancerArn']





    return Arn, TARGET_GROUP






