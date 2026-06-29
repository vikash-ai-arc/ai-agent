from langchain_core.tools import tool
from services.aws_service import create_ec2

from services.aws_service import (
    list_ec2_instances,
    start_ec2_instance,
    stop_ec2_instance,
    terminate_ec2_instance,
    create_ec2
)


@tool
def list_instances() -> str:
    """List all EC2 instances in AWS."""
    return list_ec2_instances()


@tool
def start_instance(instance_id: str) -> str:
    """Start an EC2 instance using the instance ID."""
    return start_ec2_instance(instance_id)


@tool
def stop_instance(instance_id: str) -> str:
    """Stop an EC2 instance using the instance ID."""
    return stop_ec2_instance(instance_id)


@tool
def terminate_instance(instance_id: str) -> str:
    """Terminate an EC2 instance using the instance ID."""
    return terminate_ec2_instance(instance_id)


@tool
def create_ec2_instance(
        instance_name: str,
        instance_type: str = "t3.micro"
        
) -> str:
    """Create a new AWS EC2 instance."""
    return create_ec2(instance_name, instance_type)