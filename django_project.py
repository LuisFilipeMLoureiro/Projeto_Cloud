import boto3



script_django =  """#!/bin/bash
sudo apt update
cd /home/ubuntu
git clone https://github.com/LuisFilipeMLoureiro/tasks.git
sed -i 's/node1/{0}/g' /home/ubuntu/tasks/portfolio/settings.py
cd tasks/
./install.sh
sudo ufw allow 8080/tcp
sudo reboot"""


def create_django(Name, ip_postgres):

    print("")
    print("====================================================================")
    print("")
    print("Inicionado criação do Django... \n")
    ec2_client = boto3.client("ec2", region_name="us-east-1")


    django = ec2_client.run_instances(
        ImageId="ami-0279c3b3186e54acd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="mykey_virginia",
        UserData=script_django.format(ip_postgres),
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': Name
                    },
                    {
                        'Key': 'Owner',
                        'Value': Name
                    }
                ],
                
            }
        ]
    )
    id_instancia =  django["Instances"][0]["InstanceId"]
    print("Id Instância: " + django["Instances"][0]["InstanceId"])
    print("")
    print("====================================================================")
    print("")
    print("====================================================================")
    print("django criado! \n")
    print("====================================================================")


    return ec2_client, id_instancia

