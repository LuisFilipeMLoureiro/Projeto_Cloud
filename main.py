import boto3
import os
from postgres_project import create_postgres
from django_project import create_django
from SG_Manager import SG_Deletor_Ohio,SG_Deletor_NV,SG_Postgres,SG_Django, SGlb
from Load_Balancer_Creator import LoadBalancerCreator
from Delete_Instance import delete_instance
from AutoScalling import create_AUG
import time
import logging

logging.basicConfig(filename='LOG_File.txt', filemode='w',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
#Variaveis Globais
POSTGRES_REGION = "us-east-2"
DJANGO_REGION = "us-east-1"


POSTGRES_NAME = "POSTGRES_26"
SG_POSTGRES = "SG_POSTGRES_26"

DJANGO_NAME = "DJANGO_26"
SG_DJANGO = "SG_DJANGO_26"
LB_NAME = "LB26"
NAME_AMI = "AMI26"

configuration_NAME = 'config26'
aug_NAME = 'testeaUG16'
AutoScalingGroupName = "GNAME26"
Name_TG = "TG12"
Security_LB = "SG_LB10"

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

def delete_ami(region, id_image):
    connection =  boto3.client("ec2", region_name=region)
    images = connection.describe_images(ImageIds=[id_image])
    images[0].deregister()

def create_django_ami(Name, ec2_django, id_django):

    imagem_djnago = ec2_django.create_image(InstanceId=id_django, Name=Name, NoReboot=True)
    print(imagem_djnago['ImageId'])
    return imagem_djnago['ImageId']


def attached(TARGET_GROUP, Arn,AutoScalingGroupName):
    load_balancer = boto3.client('elbv2', region_name='us-east-1')
    session = boto3.session.Session()
    ec2AutoScalling = session.client('autoscaling', region_name='us-east-1')

    ec2AutoScalling.attach_load_balancer_target_groups(
        TargetGroupARNs=[TARGET_GROUP],
        AutoScalingGroupName=AutoScalingGroupName
    )

    load_balancer.create_listener(
        LoadBalancerArn=Arn,
        DefaultActions=[{ 'Type': 'forward', 'TargetGroupArn': TARGET_GROUP}],
        Protocol='HTTP',
        Port=80  
    )

def playbook():
    
    logging.info("Iniciando Programa...")
    #create_key_pair_ohio()
    #create_key_pair_virginia()
    SG_Postgres(SG_POSTGRES)
    logging.info("SG PostGres criado...")
    create_postgres(POSTGRES_NAME)
    logging.info("PostGres criado...")
    SG_ID = SG_Django(SG_DJANGO)
    logging.info("SG Djanfo criado...")
    time.sleep(65)
    ec2_django, id_django = create_django(DJANGO_NAME, get_public_ip(POSTGRES_NAME, POSTGRES_REGION))
    logging.info("Djanfo criado...")
    time.sleep(65)
    DJANGO_AMI = create_django_ami(NAME_AMI,ec2_django, id_django)
    logging.info("AMI Djanfo criado...")
    print("criação da img concluída")
    SGlb(Security_LB )
    logging.info("SG do Load Balancer criado...")
    time.sleep(5)
    Arn, TARGET_GROUP = LoadBalancerCreator(Security_LB, LB_NAME, Name_TG)
    logging.info("Load Balancer criado...")
    print("Load Balancer criado")
    create_AUG(DJANGO_NAME, DJANGO_REGION, configuration_NAME, aug_NAME, AutoScalingGroupName, DJANGO_AMI, SG_ID)
    logging.info("AUG criado...")
    print("group scalling criado")
    attached(TARGET_GROUP, Arn,AutoScalingGroupName)
    logging.info("Listeners criados...")
    print("attached")
    delete_instance(DJANGO_NAME, DJANGO_REGION)
    logging.info("Instancia Djando apagada...")
    print("instancia django deletada")
    logging.info("Fim do programa...")

# -- play
playbook()


'''
Referências:
[1] - https://www.learnaws.org/2020/12/16/aws-ec2-boto3-ultimate-guide/
[2] - https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

'''