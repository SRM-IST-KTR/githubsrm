
import os
from typing import Any, Dict, TypedDict
import httpx
from dotenv import load_dotenv
import boto3
import pathlib
from jinja2 import Template
from .models import Entry

open_entry = Entry()
load_dotenv()


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
        """Send notifications to admins

        Args:
            payload (SNSpayload): SNSpayload
        """
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
            print("EMAIL FAILED", e)
            return

    def get_email_content(self, role: str, data: str) -> Dict[str, Any]:
        """Gets email content as per defined role

        Args:
            role (str): alpha, beta, contributor
            data (dict): data to be sent
        Returns:
            Dict[str, Any]: [description]
        """

        if role == 'project_submission_confirmation':
            return email_template(
                subject="Project Idea Submission Confirmation | GitHub Community SRM",
                bodyText=f'Your project idea {data["project_name"]} was received and will be reviewed',
                emailHTML=emailbody(file='1.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "project_description": data["project_description"]})
            )

        elif role == 'project_submission_approval_w_password_link':
            return email_template(
                subject="Project Idea Submission Approval | GitHub Community SRM",
                bodyText=f'Your project idea {data["project_name"]} was approved',
                emailHTML=emailbody(file='2.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "reset_token": data["reset_token"], "email": data["email"], "project_id": data["project_id"]})
            )

        elif role == 'project_submission_approval':
            return email_template(
                subject="Project Idea Submission Approval | GitHub Community SRM",
                bodyText=f'Your project idea {data["project_name"]} was approved',
                emailHTML=emailbody(file='3.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "email": data["email"], "project_id": data["project_id"]})
            )

        elif role == 'maintainer_received':
            return email_template(
                subject="Maintainer Application Received | GitHub Community SRM",
                bodyText=f'Your application to apply to the project {data["project_name"]} has been received',
                emailHTML=emailbody(file='4.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"]})
            )

        elif role == 'welcome_maintainer_w_password_link':
            return email_template(
                subject="Welcome Maintainer | GitHub Community SRM",
                bodyText=f'Your application to apply to the project {data["project_name"]} has been approved',
                emailHTML=emailbody(file='5.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "reset_token": data["reset_token"], "email": data["email"]})
            )

        elif role == 'welcome_maintainer':
            return email_template(
                subject="Welcome Maintainer | GitHub Community SRM",
                bodyText=f'Your application to apply to the project {data["project_name"]} has been received',
                emailHTML=emailbody(file='6.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "email": data["email"]})
            )

        elif role == 'new_maintainer_notification':
            return email_template(
                subject="New Maintainer Notification | GitHub Community SRM",
                bodyText=f'A new maintainer has applied to your project {data["project_name"]}',
                emailHTML=emailbody(file='7.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "beta_name": data["beta_name"], "beta_email": data["beta_email"]})
            )

        elif role == 'project_approval':
            return email_template(
                subject="Project Approval | GitHub Community SRM",
                bodyText=f'Your project {data["project_name"]} has been approved',
                emailHTML=emailbody(file='8.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "project_url": data["project_url"], "project_id": data["project_id"]})
            )

        elif role == 'contributor_received':
            return email_template(
                subject="Contributor Application Received | GitHub Community SRM",
                bodyText=f'Your application to be a contributor to the project {data["project_name"]} has been received',
                emailHTML=emailbody(file='9.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "contribution": data["contribution"]})
            )

        elif role == 'contributor_approval':
            return email_template(
                subject="Contributor Application Approval | GitHub Community SRM",
                bodyText=f'Your application to be a contributor to the project {data["project_name"]} has been approved',
                emailHTML=emailbody(file='10.html', name=data['name'], role=role,
                                    project_data={"project_name": data["project_name"], "project_url": data["project_url"]})
            )

        elif role == 'forgot_password':
            return email_template(
                subject="Forgot Password | GitHub Community SRM",
                bodyText=f'Token to reset your password',
                emailHTML=emailbody(file='11.html', name=data['name'], role=role,
                                    project_data={"reset_token": data["reset_token"]})
            )


def emailbody(name: str, file: str, project_data: Dict[str, Any], role: str) -> Template:
    """Returns template with appropriate data

    Args:
        name (str): name
        file (str): template name
        project_data (Dict[str, Any]): document
        role (str): user role

    Returns:
        Template
    """

    with open(f'{pathlib.Path.cwd()}/apis/templates/{file}') as file_:
        template = Template(file_.read())
        if role == "project_submission_confirmation":
            return template.render(name=name, project_name=project_data["project_name"], project_description=project_data["project_description"])
        elif role == "project_submission_approval_w_password_link":
            return template.render(name=name, project_name=project_data["project_name"], reset_token=project_data["reset_token"], email=project_data["email"], project_id=project_data["project_id"])
        elif role == "project_submission_approval":
            return template.render(name=name, project_name=project_data["project_name"], email=project_data["email"], project_id=project_data["project_id"])
        elif role == "maintainer_received":
            return template.render(name=name, project_name=project_data["project_name"])
        elif role == "welcome_maintainer_w_password_link":
            return template.render(name=name, project_name=project_data["project_name"], reset_token=project_data["reset_token"], email=project_data["email"])
        elif role == "welcome_maintainer":
            return template.render(name=name, project_name=project_data["project_name"], email=project_data["email"])
        elif role == "new_maintainer_notification":
            return template.render(name=name, project_name=project_data["project_name"], beta_name=project_data["beta_name"], beta_email=project_data["beta_email"])
        elif role == "project_approval":
            return template.render(name=name, project_name=project_data["project_name"], project_url=project_data["project_url"], project_id=project_data["project_id"])
        elif role == "contributor_received":
            return template.render(name=name, project_name=project_data["project_name"], contribution=project_data["contribution"])
        elif role == "contributor_approval":
            return template.render(name=name, project_name=project_data["project_name"], project_url=project_data["project_url"])
        elif role == "forgot_password":
            return template.render(name=name, reset_token=project_data["reset_token"])


def email_template(subject: str, bodyText: str, emailHTML: Template) -> Dict[str, Dict[str, Any]]:
    return {
        'Simple': {
            'Subject': {
                'Data': subject,
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': bodyText,
                    'Charset': 'utf-8'
                },

                'Html': {
                    'Data': emailHTML,
                    'Charset': 'utf-8'

                }
            }
        },
    }
