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

def SG_Postgres():

    loc_postgres = boto3.resource("ec2", region_name="us-east-2")

    SG_Postgres = loc_postgres.create_security_group(
        Description='liberando',
        GroupName='SG_Postgres'
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



def SG_Django():

    loc_django = boto3.resource("ec2", region_name="us-east-1")

    SG_Django = loc_django.create_security_group(
        Description='liberando',
        GroupName='SG_Django'
    )

    SG_Django.authorize_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=8080,
        ToPort=8080,
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
    return SG_Django

'''
Referências:
[1] - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_security_group
[2] - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ec2-example-security-group.html
'''


