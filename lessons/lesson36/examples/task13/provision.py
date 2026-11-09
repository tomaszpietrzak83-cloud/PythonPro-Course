import base64


def provision(asg, ec2, subnet_ids, image_id, security_group, target_group):
    user_data = "#!/bin/sh\nset -eu\nsystemctl enable --now lesson-web.service\n"
    template = ec2.create_launch_template(
        LaunchTemplateName="lesson-web",
        LaunchTemplateData={
            "ImageId": image_id,
            "InstanceType": "t3.micro",
            "SecurityGroupIds": [security_group],
            "UserData": base64.b64encode(user_data.encode()).decode(),
        },
    )["LaunchTemplate"]
    version = {"LaunchTemplateId": template["LaunchTemplateId"], "Version": "1"}
    asg.create_auto_scaling_group(
        AutoScalingGroupName="lesson-web", MinSize=2, MaxSize=4, DesiredCapacity=2,
        LaunchTemplate=version, VPCZoneIdentifier=",".join(subnet_ids),
        TargetGroupARNs=[target_group], HealthCheckType="ELB", HealthCheckGracePeriod=120,
    )
    return version


def deploy(asg, version):
    return asg.start_instance_refresh(
        AutoScalingGroupName="lesson-web", Strategy="Rolling",
        DesiredConfiguration={"LaunchTemplate": version},
        Preferences={"MinHealthyPercentage": 50, "InstanceWarmup": 120, "AutoRollback": True},
    )
