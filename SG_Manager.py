import boto3
from botocore.exceptions import ClientError



def SG_Deletor_Ohio():
    print("")
    print("====================================================================")
    print("")
    print("Deletando SG Ohio... \n")
    # Create EC2 client
    ec2 = boto3.client('ec2',region_name="us-east-2")

    # Delete security group
    try:
        response = ec2.delete_security_group(GroupName='SG_Postgres')
        print("")
        print("====================================================================")
        print("")
        print("====================================================================")
        print("SG Ohio deletado! \n")
        print("====================================================================")
    except ClientError as e:
        print(e)

def SG_Deletor_NV():
    print("")
    print("====================================================================")
    print("")
    print("Deletando SG North Virginia... \n")
    # Create EC2 client
    ec2 = boto3.client('ec2',region_name="us-east-1")

    # Delete security group
    try:
        response = ec2.delete_security_group(GroupName='SG_Django')
        print("")
        print("====================================================================")
        print("")
        print("====================================================================")
        print("SG North Virginia deletado! \n")
        print("====================================================================")
    except ClientError as e:
        print(e)

def SG_Postgres(Name):

    loc_postgres = boto3.resource("ec2", region_name="us-east-2")

    SG_Postgres = loc_postgres.create_security_group(
        Description='liberando',
        GroupName=Name
    )

    SG_Postgres.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=5432,
        ToPort=5432,
        IpProtocol="tcp"
    )

    SG_Postgres.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=22,
        ToPort=22,
        IpProtocol="tcp"
    )  
    print("")
    print("====================================================================")
    print("")
    print("====================================================================")
    print("SG Ohio - Postgres criado! \n")
    print("====================================================================")
    return SG_Postgres



def SG_Django(Name):

    loc_django = boto3.resource("ec2", region_name="us-east-1")

    SG_Django = loc_django.create_security_group(
        Description='liberando',
        GroupName=Name
    )

    SG_Django.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=8080,
        ToPort=8080,
        IpProtocol="tcp"
    )

    SG_Django.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=80,
        ToPort=80,
        IpProtocol="tcp"
    )

    SG_Django.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=22,
        ToPort=22,
        IpProtocol="tcp"
    )  
    print("")
    print("====================================================================")
    print("")
    print("====================================================================")
    print("SG North Virginia - Django criado! \n")
    print("====================================================================")


    ec2 = boto3.client('ec2', region_name="us-east-1")
    response = ec2.describe_security_groups(
        Filters=[
            dict(Name='group-name', Values=[Name])
    ])


    SG_id =  response['SecurityGroups'][0]['GroupId']

    return SG_id

def SGlb(Security_LB):
    region = boto3.resource("ec2", region_name="us-east-1")
    sg = region.create_security_group(
        GroupName=Security_LB,
        Description='Security do load done'
    )

    sg.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=80,
        ToPort=80,
        IpProtocol="tcp"
    )

    ec2 = boto3.client('ec2', region_name="us-east-1")
    response = ec2.describe_security_groups(
        Filters=[
            dict(Name='group-name', Values=[Security_LB])
    ])


    res =  response['SecurityGroups'][0]['GroupId']

    return res



'''
Referências:
[1] - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_security_group
[2] - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-security-group.html
'''


