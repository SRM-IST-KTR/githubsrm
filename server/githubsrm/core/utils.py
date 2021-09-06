import os
from functools import cache
from typing import Any, Dict

from jinja2 import Template


def get_email_content(role: str, data: Dict[str, str]) -> Dict[str, Any]:
    """Gets email content as per defined role

    Args:
        role (str): alpha, beta, contributor
        data (dict): data to be sent
    Returns:
        Dict[str, Any]: [description]
    """

    if role not in email_statics:
        raise ValueError("role not found, wrong role passed")

    email_context = email_statics[role]

    # length of kw in dict should be equal to the union of data and kw, data can have extra unused args but must have the neccesary ones.
    if len(set(email_context["kw"]) & data.keys()) != len(email_context["kw"]):
        raise ValueError(
            f"inconsistent data, data should have the following keys {email_context['kw']}"
        )

    path = f"{find_templates_folder()}/{email_context['file']}.html"

    html_email = None
    with open(path) as file_:
        template = Template(file_.read())
        html_email = template.render(**data)

    if html_email is None:
        raise IOError("failed to render templates")

    body_kw = [data[i] for i in email_context["body_kw"]]

    return {
        "Simple": {
            "Subject": {"Data": email_context["subject"], "Charset": "utf-8"},
            "Body": {
                "Text": {
                    "Data": email_context["bodyText"].format(**body_kw),
                    "Charset": "utf-8",
                },
                "Html": {"Data": html_email, "Charset": "utf-8"},
            },
        },
    }


@cache
def find_templates_folder():
    for (root, dirs, _) in os.walk("."):
        if "templates" in dirs:
            return f"{root}/templates"
    raise IOError("templates folder not found")


email_statics = {
    "project_submission_confirmation": {
        "subject": "Project Idea Submission Confirmation | GitHub Community SRM",
        "bodyText": "Your project idea {} was received and will be reviewed",
        "body_kw": ["project_name"],
        "file": "1",
        "kw": ["email", "name", "project_name", "project_description"],
    },
    "project_submission_approval_w_password_link": {
        "subject": "Project Idea Submission Approval | GitHub Community SRM",
        "bodyText": "Your project idea {} was approved",
        "body_kw": ["project_name"],
        "file": "2",
        "kw": ["name", "project_name", "reset_token", "project_id"],
    },
    "project_submission_approval": {
        "subject": "Project Idea Submission Approval | GitHub Community SRM",
        "bodyText": "Project Idea Submission Approval | GitHub Community SRMProject Idea Submission Approval | GitHub Community SRMYour project idea {} was approved",
        "body_kw": ["project_name"],
        "file": "3",
        "kw": ["name", "email", "project_name", "project_id"],
    },
    "maintainer_received": {
        "subject": "Maintainer Application Received | GitHub Community SRM",
        "bodyText": "Your application to apply to the project {} has been received",
        "body_kw": ["project_name"],
        "file": "4",
        "kw": ["name", "email", "project_name"],
    },
    "contributor_application_to_maintainer": {
        "subject": "New Contributor Notification | GitHub Community SRM",
        "bodyText": "New contributor notification to {}",
        "body_kw": ["name"],
        "file": "12",
        "kw": [
            "name",
            "email",
            "project_name",
            "contributor_name",
            "contributor_email",
        ],
    },
    "welcome_maintainer_w_password_link": {
        "subject": "Welcome Maintainer | GitHub Community SRM",
        "bodyText": "Your application to apply to the project {} has been approved",
        "body_kw": ["project_name"],
        "file": "5",
        "kw": ["name", "email", "project_name", "reset_token"],
    },
    "welcome_maintainer": {
        "subject": "Welcome Maintainer | GitHub Community SRM",
        "bodyText": "Your application to apply to the project {} has been received",
        "body_kw": ["project_name"],
        "file": "6",
        "kw": [
            "name",
            "email",
            "project_name",
        ],
    },
    "new_maintainer_notification": {
        "subject": "New Maintainer Notification | GitHub Community SRM",
        "bodyText": "A new maintainer has applied to your project {}",
        "body_kw": ["project_name"],
        "file": "7",
        "kw": ["name", "email", "project_name", "beta_name", "beta_email"],
    },
    "project_approval": {
        "subject": "Project Approval | GitHub Community SRM",
        "bodyText": "Your project {} has been approved",
        "body_kw": ["project_name"],
        "file": "8",
        "kw": ["name", "email", "project_name", "project_url", "project_id"],
    },
    "contributor_received": {
        "subject": "Contributor Application Received | GitHub Community SRM",
        "bodyText": "Your application to be a contributor to the project {} has been received",
        "body_kw": ["project_name"],
        "file": "9",
        "kw": ["name", "email", "project_name", "contribution"],
    },
    "contributor_approval": {
        "subject": "Contributor Application Approval | GitHub Community SRM",
        "bodyText": "Your application to be a contributor to the project {} has been approved",
        "body_kw": ["project_name"],
        "file": "10",
        "kw": ["name", "email", "project_name", "project_url"],
    },
    "forgot_password": {
        "subject": "Forgot Password | GitHub Community SRM",
        "bodyText": "Token to reset your password",
        "body_kw": [],
        "file": "11",
        "kw": ["name", "email", "reset_token"],
    },
    "maintainer_application_rejection": {
        "subject": "Maintainer Application Rejection | GitHub Community SRM",
        "bodyText": "Maintainer Application Rejection",
        "body_kw": [],
        "file": "13",
        "kw": ["name", "email", "project_name"],
    },
    "admin_contributor_rejection": {
        "subject": "Contributor Application Rejection | GitHub Community SRM",
        "bodyText": "Sent to reject contriutor by admin",
        "body_kw": [],
        "file": "14",
        "kw": ["name", "email", "project_name"],
    },
    "maitainer_contributor_rejection": {
        "subject": "Contributor Application Rejection | GitHub Community SRM",
        "bodyText": "Sent to reject contributor by maintainer",
        "body_kw": [],
        "file": "15",
        "kw": ["name", "email", "project_name"],
    },
}
