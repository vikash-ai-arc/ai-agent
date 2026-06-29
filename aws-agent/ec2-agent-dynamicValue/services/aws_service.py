import boto3
from config.settings import AWS_REGION
from botocore.exceptions import ClientError

ec2_client = boto3.client(
    "ec2",
    region_name=AWS_REGION
)

def create_ec2(
        instance_name,
        instance_type="t3.micro",
        ami_id="ami-0f918f7e67a3323f0",
        key_name=None,
        security_group_id=None,
        volume_size=8
):

    request = {
        "ImageId": ami_id,
        "InstanceType": instance_type,
        "MinCount": 1,
        "MaxCount": 1,
        "BlockDeviceMappings": [
            {
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "VolumeSize": volume_size,
                    "VolumeType": "gp3",
                    "DeleteOnTermination": True
                }
            }
        ],
        "TagSpecifications": [
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
    }

    if key_name:
        request["KeyName"] = key_name

    if security_group_id:
        request["SecurityGroupIds"] = [security_group_id]

    response = ec2_client.run_instances(**request)

    return response["Instances"][0]["InstanceId"]


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
    response = ec2_client.describe_instances(
        InstanceIds=[instance_id]
    )

    state = response["Reservations"][0]["Instances"][0]["State"]["Name"]

    if state != "stopped":
        return f"Instance {instance_id} is currently '{state}' and cannot be started."

    ec2_client.start_instances(
        InstanceIds=[instance_id]
    )

    return f"Starting instance {instance_id}"

## Stop instance 

def stop_ec2_instance(instance_id: str):
    try:
        response = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )

        state = response["Reservations"][0]["Instances"][0]["State"]["Name"]

        if state != "running":
            return f"Instance {instance_id} is in '{state}' state and cannot be stopped."

        ec2_client.stop_instances(
            InstanceIds=[instance_id]
        )

        return f"Stopping instance {instance_id}"

    except ClientError as e:
        return f"AWS Error: {str(e)}"

## TErminate ec2 instance

def terminate_ec2_instance(instance_id: str):
    ec2_client.terminate_instances(
        InstanceIds=[instance_id]
    )

    return (
        f"Termination request submitted for {instance_id}. "
        "Current state: shutting-down."
    )