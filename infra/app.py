#!/usr/bin/env python3
import os
import aws_cdk as cdk
from ec2_stack import Ec2ProjectStack

app = cdk.App()
Ec2ProjectStack(app, "MyEc2ProjectStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()