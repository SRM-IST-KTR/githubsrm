import os
from .models import Entry
from typing import Any, Dict, TypedDict
import httpx
from dotenv import load_dotenv
import boto3
import pathlib
from jinja2 import Template

load_dotenv()
email_client = boto3.client('sesv2', region_name='ap-south-1')


def conditional_render(path: str) -> str:
    """Conditional rendering

    Args:
        path (str): path sent in

    Returns:
        str: rendred file
    """
    fe_routes = [
        "projects",
        "team",
        "join-us",
        "join-us/contributor",
        "join-us/maintainer",
        "join-us/maintainer/new-project",
        "join-us/maintainer/existing-project",
        "contact-us",
        "404",
        "500",
    ]

    if path is None:
        return "index.html"

    if path.endswith('/'):
        path = path[:-1]

    for route in fe_routes:
        if path.endswith(route):
            return f"{path}.html"

    if len(path) > 0:
        return path
    else:
        return "index.html"


def check_token(token) -> bool:
    """Check ReCaptcha token

    Args:
        token

    Returns:
        bool
    """

    if os.getenv("CI"):
        return True

    url = "https://www.google.com/recaptcha/api/siteverify"
    secret_key = os.getenv('RECAPTCHA_SECRET_KEY')

    payload = {
        'secret': secret_key,
        'response': token,
    }

    with httpx.Client() as client:
        response = client.post(url, data=payload)
    return response.json()["success"] and response.json()["score"] >= 0.5


class SNSpayload(TypedDict):
    message: str
    subject: str


class BotoService:

    def sns(self, payload: SNSpayload) -> None:
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

    def wrapper_email(self, role: str, data: Dict[str, Any]) -> bool:
        """Send Emails to contributors and maintainers

        Args:
            role (str)  alpha, beta or contributor
            data (dict) essential data to send mail
        Returns:
            bool
        """
        client = boto3.client('sesv2', region_name='ap-south-1')

        try:
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
                Content=self.get_email_content(role=role, data=data)
            )
            return True

        except Exception as e:
            print(e)
            return

    def get_email_content(self, role: str, data: str) -> Dict[str, Any]:
        """Gets email content as per defined role

        Args:
            role (str): alpha, beta, contributor
            data (dict): data to be sent
        Returns:
            Dict[str, Any]: [description]
        """
        if role == 'alpha':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Submission Confirmation | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'PLEASE WAIT FOR ADMIN APPROVAL FOR THE PROJECT: {data.get("project_name")}',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'],
                                              project_name=data["project_name"], project_id=data["project_id"]),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }

        elif role == 'beta':
            entry = Entry()
            project = list(entry.db.project.find({"_id": data["project_id"]}))
            project_name = project[0]["project_name"]
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Submission Confirmation | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'You are under review for the project ID {data.get("project_id")}',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='beta_maintainer_accept.html', name=data['name'],
                                              project_name=project_name),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }

        else:
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Submission Confirmation | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Your contribution is under review for the project {data.get("interested_project")}',
                            'Charset': 'utf-8'
                        }
                    }
                }
            }


def emailbody(name, file, project_name, project_id=None):
    with open(f'{pathlib.Path.cwd()}/apis/templates/{file}') as file_:
        template = Template(file_.read())
        if project_id:
            return template.render(name=name, project_id=project_id, project_name=project_name)
        return template.render(name=name, project_name=project_name)
