
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
