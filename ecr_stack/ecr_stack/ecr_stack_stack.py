from aws_cdk import (
    # Duration,
    Stack,
    aws_ecr as ecr,
    RemovalPolicy
    # aws_sqs as sqs,
)
from constructs import Construct

class EcrStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo = ecr.Repository(
            self,
            "OCIRepository",
            repository_name="gcp_ecr_repository",
            removal_policy=RemovalPolicy.DESTROY
        )
        
