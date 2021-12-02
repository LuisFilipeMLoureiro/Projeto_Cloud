import boto3
import os
from postgres_project import create_postgres
from django_project import create_django
from SG_Manager import SG_Deletor_Ohio,SG_Deletor_NV,SG_Postgres,SG_Django



#[Powershell]
# ssh -i aws_ec2_key_virginia.pem ubuntu@18.212.171.88
#[Prompt]
#telnet 3.14.8.159 5432
#Variaveis Globais
POSTGRES_NAME = "POSTGRES_USER"
POSTGRES_REGION = "us-east-2"



def create_key_pair_ohio():
    ec2_client = boto3.client("ec2", region_name="us-east-2")
    key_pair = ec2_client.create_key_pair(KeyName="mykey")

    private_key = key_pair["KeyMaterial"]

    # write private key to file with 400 permissions
    with os.fdopen(os.open("tmp/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)

    print("====================================")
    print("")
    print("key para instâncias de Ohio criadas... \n")
    return key_pair


def create_key_pair_virginia():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    key_pair = ec2_client.create_key_pair(KeyName="mykey_virginia")

    private_key = key_pair["KeyMaterial"]

    # write private key to file with 400 permissions
    with os.fdopen(os.open("tmp/aws_ec2_key_virginia.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)
    print("====================================")
    print("")
    print("key para instâncias de North Virginia criadas... \n")
    return key_pair

def create_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    instances = ec2_client.run_instances(
        ImageId="ami-0279c3b3186e54acd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="mykey_virginia",
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'user_project'
                    },
                    {
                        'Key': 'Owner',
                        'Value': 'user_project'
                    },
                ]
            }
        ]
    )
    print("")
    print("====================================")
    print("")
    print("====================================")
    print("Instância criada... \n")
    print("Id: " + instances["Instances"][0]["InstanceId"])
 

def stop_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-west-2")
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    print(response)

def get_public_ip(tag_instance, region):
    ec2_client = boto3.client("ec2", region_name=region)
    reservations = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [tag_instance]}])
    #print(reservations)
    
    return reservations['Reservations'][0]['Instances'][0]['PublicIpAddress']



def playbook():
    #create_key_pair_ohio()
    #create_key_pair_virginia()
    SG_Postgres()
    create_postgres()
    SG_Django()
    create_django(get_public_ip(POSTGRES_NAME, POSTGRES_REGION))

#play
#playbook()
create_postgres()

'''
Referências:
[1] - https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
[2] -https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

'''