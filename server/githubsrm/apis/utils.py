import os
from typing import Any, Dict
import httpx
from dotenv import load_dotenv
import boto3

load_dotenv()
email_client = boto3.client('sesv2', region_name='ap-south-1')


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


class BotoService:

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
                            'Data': f'Here is your Project ID {data.get("project_id")}',
                            'Charset': 'utf-8'
                        }
                    }
                }
            }

        elif role == 'beta':
            return {
                'Simple': {
                    'Subject': {
                        'Data': 'Submission Confirmation | GitHub Community SRM',
                        'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'You have been added as a maintainer to the project with the id {data.get("project_id")}',
                            'Charset': 'utf-8'
                        }
                    }
                }
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


def send_mail(project_id: str, email: str) -> bool:
    """Send emails

    Args:
        project_id (str)
        email (str)

    Returns:
        bool
    """
    try:
        email_client.send_email(
            FromEmailAddress='GitHub Community SRM <community@githubsrm.tech>',
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            ReplyToAddresses=[
                'community@githubsrm.tech',
            ],


        )
        return True

    except Exception as e:
        print(e)
        return


'''
Content={
                'Simple': {
                    'Subject': {
                        'Data': 'Submission Confirmation | GitHub Community SRM',
                                'Charset': 'utf-8'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Your Project ID is {project_id}',
                                    'Charset': 'utf-8'
                        },

                        # 'Html': {
                        #     'Data': emailbody(file='confirm_email.html', name=request.data['fields']['name'], otp=None),
                        #     'Charset': 'utf-8'

                        # }
                    }
                },
            }

'''
