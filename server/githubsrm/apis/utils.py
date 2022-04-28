from functools import lru_cache
import os
import requests
from dotenv import load_dotenv


load_dotenv()
session = requests.Session()


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
    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")

    payload = {
        "secret": secret_key,
        "response": token,
    }

    response = requests.post(url, data=payload)
    return response.json()["success"] and response.json()["score"] >= 0.5


@lru_cache()
def verify_github_details(verify_user=False, **kwargs):
    """Perf enhancement using the github rest API instead
    of directly hitting the github url, handles rate-limiting
    by directly hitting the url.
    """
    github_api = "https://api.github.com"
    source_route = "https://github.com"

    if verify_user:
        response = session.get(f"{github_api}/users/{kwargs['user_id']}")
        res = response.json()
        # Will send False to the frontend if server is down or User ID is not a personal id but a Organisation ID.
        if(response.status_code == 200):
            if(res['type']=="User" ):
                return True
            else:
                return False
        else:
            return False
    else:
        # Todo: move to github apis after discussion on porting
        # Used for existing projects.
        response = session.get(kwargs["url"])

        return response.status_code == 200
