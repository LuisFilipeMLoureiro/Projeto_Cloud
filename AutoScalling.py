import boto3





def create_AUG(DJANGO_NAME, region, configuration_NAME, aug_NAME, AutoScalingGroupName, image_id, id_SecurityGroup):
    script_django =  """#!/bin/bash
    sudo apt update
    cd /home/ubuntu
    git clone https://github.com/LuisFilipeMLoureiro/tasks.git
    sed -i 's/node1/{0}/g' /home/ubuntu/tasks/portfolio/settings.py
    cd tasks/
    ./install.sh
    sudo ufw allow 8080/tcp
    sudo reboot"""


    

    session = boto3.session.Session()
    autoscalling = session.client('autoscaling', region_name=region)





    instancia = session.resource('ec2', region_name=region)
    client = session.client('ec2', region_name=region)


    running_instances = instancia.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Owner',
                    'Values': [DJANGO_NAME]
                },
            ]
        )


    for instance in running_instances:
        instancia_id = instance.id
        print(instancia_id)
        break
    autoscalling.create_launch_configuration(
                LaunchConfigurationName=configuration_NAME,
                ImageId=image_id,
                SecurityGroups=[id_SecurityGroup],
                InstanceType='t2.micro', 
                UserData = script_django
        )

    autoscalling.create_auto_scaling_group(
        AutoScalingGroupName=AutoScalingGroupName,
        InstanceId=instancia_id,
        MinSize=1,
        MaxSize=5,
        DesiredCapacity=1,


        Tags=[
            {
                'Key': 'Owner',
                'Value': aug_NAME
            },
            {
                'Key': 'Name',
                'Value': aug_NAME
            },
        ]
    )


