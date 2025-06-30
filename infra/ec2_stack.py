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

        # Allow HTTPS
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow HTTPS"
        )

        # Allow FastAPI (port 8000)
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(8000),
            "Allow FastAPI"
        )

        # Allow Angular dev server (port 4200)
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(4200),
            "Allow Angular"
        )

        # User data to install all dependencies
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash",
            "yum update -y",
            
            # Install Git
            "yum install -y git",
            
            # Install Docker and Docker Compose
            "yum install -y docker",
            "systemctl start docker",
            "systemctl enable docker",
            "usermod -a -G docker ec2-user",
            
            # Install Docker Compose
            "curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
            "chmod +x /usr/local/bin/docker-compose",
            
            # Install Python 3 and pip
            "yum install -y python3 python3-pip",
            
            # Install Node.js 18
            "curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -",
            "yum install -y nodejs",
            
            # Install Angular CLI globally
            "npm install -g @angular/cli",
            
            # Install Nginx
            "yum install -y nginx",
            "systemctl enable nginx",
            
            # Create project directories
            "mkdir -p /home/ec2-user/backend",
            "mkdir -p /home/ec2-user/frontend",
            "chown -R ec2-user:ec2-user /home/ec2-user/",
            
            # Create a simple status page
            "echo 'Server is ready for FastAPI and Angular deployment!' > /var/www/html/index.html",
            "systemctl start nginx"
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
            key_name="amanu-ssh-key",
            user_data=user_data
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

        # Output server status URL
        CfnOutput(
            self, "ServerStatusURL",
            value=f"http://{instance.instance_public_ip}",
            description="Server status page"
        )