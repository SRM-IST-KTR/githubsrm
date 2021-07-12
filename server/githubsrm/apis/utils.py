
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
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data["project_name"], "project_id": data.get("_id")}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }

        elif role == 'beta':
            project = open_entry.get_project_from_id(
                identifier=data["project_id"])
            project_name = project["project_name"]
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Submission Confirmation | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'You are under review for the project ID {data.get("_id")}',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='beta_maintainer_accept.html', name=data['name'], role=role,
                                              project_data={"project_name": project_name}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }
        # TODO : Change contents of email and make email templates
        elif role == 'existing_alpha_maintainer':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Maintainer Confirmation | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Maintainer Confirmation',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data.get("project_name")}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }
        elif role == 'alpha_maintainer_w_password':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Maintainer Approved | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Credentials given',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data["project_name"], "project_id": data.get("_id")}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }
        elif role == 'beta_maintainer_approval':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Maintainer Approved | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Your request to become a maintainer was approved',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data["project_name"]}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }
        elif role == 'beta_maintainer_approval_to_alpha':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Maintainer Approved | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Maintainer was approved',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data["project_name"]}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }
        elif role == 'beta_maintainer_approval_w_password':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Maintainer approved | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'',
                            'Charset': 'utf-8'
                        },

                        'Html': {
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data.get("project_name")}),
                            'Charset': 'utf-8'

                        }
                    }
                },
            }
        elif role == 'approve_project':
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
                            'Data': emailbody(file='alpha_maintainer_code.html', name=data['name'], role=role,
                                              project_data={"project_name": data["project_name"]}),
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
        if role == "alpha":
            return template.render(name=name, project_id=project_data.get("_id"), project_name=project_data.get("project_name"))
        elif role == "beta":
            return template.render(name=name, project_name=project_data.get("project_name"))
        elif role == "existing_alpha_maintainer":
            return template.render(name=name, project_name=project_data.get("project_name"))
        elif role == "alpha_maintainer_w_password":
            return template.render(name=name, project_name=project_data.get("project_name"))
        elif role == "beta_maintainer_approval":
            return template.render(name=name, project_name=project_data.get("project_name"))
        elif role == "beta_maintainer_approval_to_alpha":
            return template.render(name=name, project_name=project_data.get("project_name"))
        elif role == "beta_maintainer_approval_w_password":
            return template.render(name=name, project_name=project_data.get("project_name"))
        elif role == "approve_project":
            return template.render(name=name, project_name=project_data.get("project_name"))
