import boto3



def create_postgres(Name):

    print("")
    print("====================================================================")
    print("")
    print("Inicionado criação do Postgres... \n")
    ec2_client = boto3.client("ec2", region_name="us-east-2")


    with open("postgresCLI.sh", "r") as file:
        cli_postgres = file.read()


    postgres = ec2_client.run_instances(
        ImageId="ami-020db2c14939a8efb",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="mykey",
        UserData=cli_postgres,
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

    print("Id Instância: " + postgres["Instances"][0]["InstanceId"])
    print("")
    print("====================================================================")
    print("")
    print("====================================================================")
    print("Postgres criado! \n")
    print("====================================================================")

