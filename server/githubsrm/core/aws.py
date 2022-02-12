import json
import os
from typing import Any, Dict, List, TypedDict

import boto3

from .log_utils.log import get_logger
from .settings import TRIGGER_AWS
from .utils import get_email_content

# Set logging level to critical since breaking aws service breaks everything :).
logger = get_logger(
    "aws.service.errors",
    filename="AWSError.log",
    level=30,
)


class SNSpayload(TypedDict):
    message: str
    subject: str


class BotoService:
    def sns(self, payload: SNSpayload) -> None:
        """Send notifications to admins

        Args:
            payload (SNSpayload): SNSpayload
        """
        if not TRIGGER_AWS:
            return True

        client = boto3.client("sns", region_name="ap-south-1")

        try:
            client.publish(
                TopicArn=os.getenv("SNS_ARN"),
                Message=payload["message"],
                Subject=payload["subject"],
            )
        except Exception as e:
            logger.critical("SNS Failed!")
            logger.exception(e)

    def wrapper_email(self, role: str, data: Dict[str, Any], send_all=False) -> bool:
        """Send Emails to contributors and maintainers

        Args:
            role (str)  alpha, beta or contributor
            data (dict) essential data to send mail
        Returns:
            bool
        """
        if not TRIGGER_AWS:
            return True
        client = boto3.client("sesv2", region_name="ap-south-1")

        email_addresses = []
        data_email = data.get("email")
        if isinstance(data_email, List):
            email_addresses.extend(data_email)
        else:
            email_addresses.append(data_email)

        try:
            client.send_email(
                FromEmailAddress="GitHub Community SRM <community@githubsrm.tech>",
                Destination={"ToAddresses": email_addresses},
                ReplyToAddresses=[
                    "community@githubsrm.tech",
                ],
                Content=get_email_content(role, data),
            )
            return True

        except Exception as e:
            logger.critical("Email Failed!")
            logger.exception(e)

    def lambda_(self, func: str, payload: Dict) -> Dict:
        """[Lambda wrapper for AWS]

        Args:
            func (str): [Func ARN or name of function]
            payload (Dict): [Payload to pass to function]

        Returns:
            Dict: [function json response]
        """
        if not TRIGGER_AWS:
            # Test return!
            return {
                "success": True,
                "team-slug": "team-slug-123",
                "private": True,
                "repo-link": "https://github.com/SRM-IST-KTR/githubsrm",
            }
        client = boto3.client("lambda", region_name="ap-south-1")
        try:
            res = client.invoke(FunctionName=func, Payload=json.dumps(payload))
        except Exception as e:
            logger.critical("lambda failed during invocation!")
            logger.exception(e)

        if "Payload" in res and hasattr(res["Payload"], "read"):
            return json.loads(res["Payload"].read())
        else:
            logger.critical(
                f"lambda returned without payload!\n Returned Value: {response}"
            )
            return {"error": "lambda failed!"}


service = BotoService()
