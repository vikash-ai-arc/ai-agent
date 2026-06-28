import boto3
from config.settings import AWS_REGION

ec2_client = boto3.client(
    "ec2",
    region_name=AWS_REGION
)

def create_ec2(
        instance_name,
        instance_type="t3.micro",
        ami_id="ami-0f918f7e67a3323f0"  # Amazon Linux 2023 (verify for region)
):
    response = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": instance_name
                    }
                ]
            }
        ]
    )

    instance_id = response["Instances"][0]["InstanceId"]

    return (
        f"EC2 Instance created successfully.\n"
        f"Instance ID: {instance_id}\n"
        f"Instance Type: {instance_type}"
    )
## List of ec2 instance
def list_ec2_instances():
    response = ec2_client.describe_instances()

    result = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            result.append({
                "instance_id": instance["InstanceId"],
                "state": instance["State"]["Name"],
                "instance_type": instance["InstanceType"],
                "public_ip": instance.get("PublicIpAddress", "N/A")
            })

    return result

# start ec2 instance 
def start_ec2_instance(instance_id: str):
    ec2_client.start_instances(
        InstanceIds=[instance_id]
    )

    return f"Started instance {instance_id}"

## Stop instance 

def stop_ec2_instance(instance_id: str):
    ec2_client.stop_instances(
        InstanceIds=[instance_id]
    )

    return f"Stopped instance {instance_id}"

## TErminate ec2 instance

def terminate_ec2_instance(instance_id: str):
    ec2_client.terminate_instances(
        InstanceIds=[instance_id]
    )

    return f"Terminated instance {instance_id}"