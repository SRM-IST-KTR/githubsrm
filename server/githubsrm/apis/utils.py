
import os
import requests
from dotenv import load_dotenv
from jinja2 import Template
from typing import Dict, Any

import pathlib
from .models import Entry

open_entry = Entry()
load_dotenv()


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

    response = requests.post(url, data=payload)
    return response.json()["success"] and response.json()["score"] >= 0.5


def get_email_content(role: str, data: str) -> Dict[str, Any]:
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

    elif role == "contributor_application_to_maintainer":
        return email_template(
            subject="New Contributor Notification | GitHub Community SRM",
            bodyText=f"New contributor notification to {data['name']}",
            emailHTML=emailbody(file='12.html', name=data['name'], role=role,
                                project_data={"project_name": data["project_name"],
                                              "contributor_name": data["contributor_name"],
                                              "contributor_email": data["contributor_email"]})

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

    elif role == 'maintainer_application_rejection':
        return email_template(
            subject="Maintainer Application Rejection | GitHub Community SRM",
            bodyText="Maintainer Application Rejection",
            emailHTML=emailbody(file="13.html", name=data['name'], role=role, project_data={
                                "project_name": data["project_name"]})
        )
    elif role == 'admin_contributor_rejection':
        return email_template(
            subject="Contributor Application Rejection | GitHub Community SRM",
            bodyText="Sent to reject contriutor by admin",
            emailHTML=emailbody(file="14.html", name=data['name'], role=role, project_data={
                                "project_name": data["project_name"]})
        )
    elif role == 'maitainer_contributor_rejection':
        return email_template(
            subject="Contributor Application Rejection | GitHub Community SRM",
            bodyText="Sent to reject contributor by maintainer",
            emailHTML=emailbody(file="15.html", name=data['name'], role=role, project_data={
                                "project_name": data["project_name"]})
        )


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

    path = ""
    for (root, dirs, _) in os.walk("."):
        if "templates" in dirs:
            path = f"{root}/templates/{file}"

    if not path:
        raise IOError("templates folder not found")

    with open(path) as file_:
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
        elif role == "contributor_application_to_maintainer":
            return template.render(name=name, project_name=project_data["project_name"],
                                   contributor_name=project_data["contributor_name"],
                                   contributor_email=project_data["contributor_email"])
        elif role == "maintainer_application_rejection":
            return template.render(name=name, project_name=project_data["project_name"])
        elif role == "admin_contributor_rejection":
            return template.render(name=name, project_name=project_data["project_name"])
        elif role == "maitainer_contributor_rejection":
            return template.render(name=name, project_name=project_data["project_name"])
