import boto3




def delete_instance(name, region):

    session = boto3.session.Session()
    instancia = session.resource('ec2', region_name=region)
    client = session.client('ec2', region_name=region)


    running_instances = instancia.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Owner',
                    'Values': [name]
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )


    for instance in running_instances:
        instancia_id = instance.id
        print(instancia_id)
        break


    client.terminate_instances(InstanceIds=[instancia_id])

    waiter = client.get_waiter('instance_terminated')
    waiter.wait(InstanceIds=[instancia_id])
    print('encerrada {0}'.format(instancia_id))

    
    return instancia_id

