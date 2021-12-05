import json
import os
from functools import lru_cache
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

    templates_folder = find_templates_folder()

    with open(f"{templates_folder}/email_statics.json", "r") as fp:
        email_statics = json.load(fp)

    if role not in email_statics:
        raise ValueError("role not found, wrong role passed")

    email_context = email_statics[role]

    # length of kw in dict should be equal to the union of data and kw, data can have extra unused args but must have the neccesary ones.
    if len(set(email_context["kw"]) & data.keys()) != len(email_context["kw"]):
        raise ValueError(
            f"inconsistent data, data should have the following keys {email_context['kw']}"
        )

    path = f"{templates_folder}/{email_context['file']}.html"

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
                    "Data": email_context["bodyText"].format(*body_kw),
                    "Charset": "utf-8",
                },
                "Html": {"Data": html_email, "Charset": "utf-8"},
            },
        },
    }


@lru_cache
def find_templates_folder():
    for (root, dirs, _) in os.walk("."):
        if "templates" in dirs:
            return f"{root}/templates"
    raise IOError("templates folder not found")
