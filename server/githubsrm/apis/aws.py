import os
from typing import Any, Dict, TypedDict
from .utils import get_email_content
import boto3
import json


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

    def lambda_(self, func: str, payload: Dict) -> Dict:
        """[Lambda wrapper for AWS]

        Args:
            func (str): [Func ARN or name of fucntion]
            payload (Dict): [Payload to pass to function]

        Returns:
            Dict: [fucntion json response]
        """
        client = boto3.client('lambda', region_name='ap-south-1')
        try:
            res = client.invoke(FunctionName=func, Payload=json.dumps(payload))
        except Exception as e:
            print(f"AWS failed with {e}")
            return {"error": e}

        if "Payload" in res and hasattr(res["Payload"], "read"):
            return json.loads(res["Payload"].read())
        else:
            return {"error": "Lambda response was not expected"}
