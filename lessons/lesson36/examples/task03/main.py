def web_ingress():
    return [
        {"IpProtocol": "tcp", "FromPort": port, "ToPort": port,
         "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}
        for port in (80, 443)
    ]


def provision(ec2, vpc_id):
    group = ec2.create_security_group(GroupName="web", Description="Public web", VpcId=vpc_id)
    ec2.authorize_security_group_ingress(GroupId=group["GroupId"], IpPermissions=web_ingress())
    return group["GroupId"]


def demo(work):
    rules = web_ingress()
    result = {port: any(rule["FromPort"] <= port <= rule["ToPort"] for rule in rules)
              for port in (22, 80, 443)}
    assert result == {22: False, 80: True, 443: True}
    return {"rules": rules, "allows_tcp_ipv4": result}
