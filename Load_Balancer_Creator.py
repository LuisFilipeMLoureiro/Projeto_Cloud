import boto3
from botocore.exceptions import ClientError



def LoadBalancerCreator(Security_Group,lb_name):
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

    return lb


