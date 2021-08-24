import os
from typing import Any, Dict, TypedDict
from .utils import get_email_content
import boto3


class SNSpayload(TypedDict):
    message: str
    subject: str


class BotoService:

    def sns(self, payload: SNSpayload) -> None:
        """Send notifications to admins

        Args:
            payload (SNSpayload): SNSpayload
        """
        if os.getenv("SENDEMAIL"):
            return True

        client = boto3.client('sns', region_name='ap-south-1')

        try:
            client.publish(
                TopicArn=os.getenv("SNS_ARN"),
                Message=payload['message'],
                Subject=payload['subject']
            )
        except Exception as e:
            print(e)
            return

    def wrapper_email(self, role: str, data: Dict[str, Any], send_all=False) -> bool:
        """Send Emails to contributors and maintainers

        Args:
            role (str)  alpha, beta or contributor
            data (dict) essential data to send mail
        Returns:
            bool
        """
        if os.getenv("SENDEMAIL"):
            return True
        client = boto3.client('sesv2', region_name='ap-south-1')

        try:
            if send_all:
                client.send_email(
                    FromEmailAddress='GitHub Community SRM <community@githubsrm.tech>',
                    Destination={
                        'ToAddresses': data.get("email"),
                    },
                    ReplyToAddresses=[
                        'community@githubsrm.tech',
                    ],
                    Content=get_email_content(role=role, data=data)
                )
            else:
                client.send_email(
                    FromEmailAddress='GitHub Community SRM <community@githubsrm.tech>',
                    Destination={
                        'ToAddresses': [
                            data.get('email'),
                        ],
                    },
                    ReplyToAddresses=[
                        'community@githubsrm.tech',
                    ],
                    Content=get_email_content(role=role, data=data)
                )

            return True

        except Exception as e:
            print("EMAIL FAILED", e)
            return
