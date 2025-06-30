from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
)
from constructs import Construct


class Ec2ProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Use default VPC
        vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)

        # Create security group
        security_group = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=vpc,
            description="Security group for web server",
            allow_all_outbound=True
        )

        # Allow SSH
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH"
        )

        # Allow HTTP
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP"
        )

        # Create EC2 instance (free tier eligible)
        instance = ec2.Instance(
            self, "WebServer",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T2, 
                ec2.InstanceSize.MICRO
            ),  # Free tier
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=security_group,
            key_name="amanu-ssh-key"  
        )

        # Output the public IP
        CfnOutput(
            self, "PublicIP",
            value=instance.instance_public_ip,
            description="Public IP of the EC2 instance"
        )

        # Output SSH command
        CfnOutput(
            self, "SSHCommand",
            value=f"ssh -i amanu-ssh-key.pem ec2-user@{instance.instance_public_ip}",
            description="SSH command to connect to the instance"
        )