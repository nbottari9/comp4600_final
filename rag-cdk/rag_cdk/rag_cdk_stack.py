from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ecr as ecr
)
from constructs import Construct

RESOURCE_PREFIX = "gcp-rag-cdk-"

class RagCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        
        security_group = ec2.SecurityGroup(
            self, "rag-instance-SG",
            vpc=vpc,
            description="Allow SSH Access",
            allow_all_outbound=True
        )
            
    
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH Access")
        
        role = iam.Role(
            self, "rag-instance-sg",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        
        role.add_to_policy(
                iam.PolicyStatement(
                actions=[
                    "ecr:GetAuthorizationToken"
                ],
                resources=["*"]
            )
        )
        role.add_to_policy(
                iam.PolicyStatement(
                actions=[
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage"
                ],
                resources=["*"]
            )
        )
  
    
    
        instance = ec2.Instance(
            self, RESOURCE_PREFIX + "RAG-Instance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.generic_linux({ "us-east-1": "ami-0ecb62995f68bb549"}),
            vpc=vpc,
            security_group=security_group,
            role=role,
            key_name='Gurpreet-KP',
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(
                        volume_size=50,
                        volume_type=ec2.EbsDeviceVolumeType.GP3,
                        encrypted=True 
                    )
                )
            ] 
        )
    
        
        repo = ecr.Repository.from_repository_name(
            self,
            "GCP-imported-repo",
            repository_name="gcp-ecr-repo"
        ) 
    
        instance.add_user_data(
            "apt -y update",
            "apt install -y unzip curl",
            "curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'",
            "unzip awscliv2.zip",
            "sudo ./aws/install",
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            "source $HOME/.local/bin/env",
            "curl -fsSL https://ramalama.ai/install.sh | bash",
            f"export REPO_URI={repo.repository_uri}", 
            "git clone https://github.com/nbottari9/comp4600_final.git",
            "cd comp4600_final/rag-scripts/",
            "uv init .",
            "uv add pip-system-certs aiohttp",
            "uv run parallel_download.py && ./vectorize.sh ecr rag-data"
        )
            
