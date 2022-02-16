import binascii
import hashlib
import json
import os
import secrets
from django.conf import settings

settings.configure(USE_DATABASE="TESTMONGO")


class Base:
    def __init__(self) -> None:
        self.alpha_data = {
            "name": "Riju",
            "email": "rmukh561@gmail.com",
            "github_id": "riju561",
            "srm_email": "rm8211@srmist.edu.in",
            "reg_number": "RA1911003010056",
            "branch": "CSE",
            "project_name": "Qwerty",
            "project_url": "",
            "private": True,
            "tags": ["a", "b", "c", "d"],
            "description": "abc.asd.wd wdakwdaw dawdkwadaw dawldwadkaw dwadkawkdlawmd awdawodkaw",
        }
        self.admin_data = {"email": "rmukh561@gmail.com", "password": "test"}
        self.beta_data = {
            "name": "Riju",
            "email": "rijumukh50601@gmail.com",
            "github_id": "riju",
            "srm_email": "as1234@srmist.edu.in",
            "reg_number": "RA1911003010042",
            "branch": "CSE",
        }
        self.contributor_data = {
            "name": "Abhishek Saxena",
            "email": "as7122000@gmail.com",
            "srm_email": "as2345@srmist.edu.in",
            "reg_number": "RA1911027010102",
            "branch": "CSE-BD",
            "github_id": "xyz",
            "poa": "HelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelp",
        }
        self.maintainer_login_data = {
            "email": "rmukh561@gmail.com",
            "password": "test1234",
        }
        self.beta_maintainer_login_data = {
            "email": "rijumukh50601@gmail.com",
            "password": "test1234",
        }
        self.project_details = {"year": "2021"}
        self.another_alpha = {
            "name": "Riju",
            "email": "rmukh561@gmail.com",
            "github_id": "riju561",
            "srm_email": "rm8211@srmist.edu.in",
            "reg_number": "RA1911003010056",
            "branch": "CSE",
            "project_name": "Qwertz",
            "project_url": "",
            "private": True,
            "tags": ["e", "f", "g", "h"],
            "description": "abc.asd.wd wdakwdaw dawdkwadaw dawldwadkaw dwadkawkdlawmd awdawodkawdsfsdf asdfafd",
        }
        self.contact_us_data = {
            "name": "Riju Mukherjee",
            "email": "rmukh561@gmail.com",
            "message": "Test Test Test Test Test Test Test Test Test Test Test Test Test Test Test",
            "phone_number": "9818982052",
        }
        self.base_headers = {
            "Content-type": "application/json",
            "X-RECAPTCHA-TOKEN": "TestToken",
        }

    def hash_password(self, password: str) -> str:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwd_hash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        final_hashed_pwd = (salt + pwd_hash).decode("ascii")
        return final_hashed_pwd

    def register_admin(self, instance, webhook=None):
        if not webhook:
            webhook = instance.webhook
        return instance.client.post(
            url=instance.base_url + "admin/register",
            data=json.dumps(self.admin_data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {webhook}"},
            },
        )

    def login_admin(self, instance):
        return instance.client.post(
            url=instance.base_url + "admin/login",
            data=json.dumps(self.admin_data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {instance.webhook}"},
            },
        )

    def add_alpha_maintainer(self, instance, data=None):
        if not data:
            data = self.alpha_data
        return instance.client.post(
            url=instance.base_url + "api/maintainer",
            data=json.dumps(data),
            headers=self.base_headers,
            params={"role": "alpha"},
        )

    def approve_alpha_maintainer(self, instance, alpha, admin_jwt, data=None):
        if not data:
            data = {
                "maintainer_id": alpha["_id"],
                "project_id": alpha["project_id"],
                "email": alpha["email"],
            }
        return instance.client.post(
            url=instance.base_url + "admin/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "maintainer"},
        )

    def add_beta_maintainer(self, instance, alpha=None, id=None, data=None):
        if not data:
            data = self.beta_data
        if alpha:
            return instance.client.post(
                url=instance.base_url + "api/maintainer",
                data=json.dumps({**data, **{"project_id": alpha["project_id"]}}),
                headers=self.base_headers,
                params={"role": "beta"},
            )
        else:
            return instance.client.post(
                url=instance.base_url + "api/maintainer",
                data=json.dumps({**data, **{"project_id": id}}),
                headers=self.base_headers,
                params={"role": "beta"},
            )

    def approve_beta_maintainer(self, instance, beta, admin_jwt, data=None):
        if not data:
            data = {
                "maintainer_id": beta["_id"],
                "project_id": beta["project_id"],
                "email": beta["email"],
            }
        return instance.client.post(
            url=instance.base_url + "admin/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "maintainer"},
        )

    def get_admin_projects(self, instance, alpha, admin_jwt):
        response = instance.client.get(
            url=instance.base_url + "admin/projects",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"page": 1},
        )
        print(response.json())

        response = instance.client.post(
            url=instance.base_url + "admin/projects",
            data=json.dumps(
                {**self.project_details, **{"project_id": alpha["project_id"]}}
            ),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "project"},
        )
        instance.assertEqual(response.status_code, 200)

        response = instance.client.get(
            url=instance.base_url + "admin/projects",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={
                "projectId": alpha["project_id"],
                "maintainer": True,
                "contributor": True,
            },
        )
        print(response.json())

    def approve_project(self, instance, alpha, admin_jwt, data=None):
        if not data:
            data = self.project_details
        return instance.client.post(
            url=instance.base_url + "admin/projects",
            data=json.dumps({**data, **{"project_id": alpha["project_id"]}}),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "project"},
        )

    def add_contributor(self, instance, alpha, data=None):
        if not data:
            data = self.contributor_data
        return instance.client.post(
            url=instance.base_url + "api/contributor",
            data=json.dumps(
                {
                    **data,
                    **{"interested_project": alpha["project_id"]},
                }
            ),
            headers=self.base_headers,
            params={"role": "contributor"},
        )

    def approve_contributor_admin(self, instance, contributor, admin_jwt, data=None):
        if not data:
            data = {
                "contributor_id": contributor["_id"],
                "project_id": contributor["interested_project"],
            }
        return instance.client.post(
            url=instance.base_url + "admin/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "contributor"},
        )

    def get_accepted_projects_admin(self, instance, admin_jwt):
        return instance.client.get(
            url=instance.base_url + "admin/projects/accepted",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"page": 1},
        )

    def reject_maintainer(self, instance, alpha, admin_jwt):
        data = {"maintainer_id": alpha["_id"]}
        return instance.client.delete(
            url=instance.base_url + "admin/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "maintainer"},
        )

    def reject_contributor_admin(self, instance, contributor, admin_jwt):
        data = {"contributor_id": contributor["_id"]}
        return instance.client.delete(
            url=instance.base_url + "admin/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"role": "contributor"},
        )

    def get_me_admin(self, instance, admin_jwt):
        return instance.client.get(
            url=instance.base_url + "me",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
        )

    def get_projects_admin(self, instance, id, admin_jwt):
        response = instance.client.get(
            url=instance.base_url + "admin/projects",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"page": 1},
        )
        print(response)
        response = instance.client.get(
            url=instance.base_url + "admin/projects",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {admin_jwt}"},
            },
            params={"projectId": id, "maintainer": True, "contributor": True},
        )
        print(response)
        return response

    def login_maintainer(self, instance, data=None):
        if not data:
            data = self.maintainer_login_data
        return instance.client.post(
            url=instance.base_url + "maintainer/login",
            data=json.dumps(data),
            headers=self.base_headers,
        )

    def approve_contributor_maintainer(
        self, instance, contributor, maintainer_jwt, data=None
    ):
        if not data:
            data = {
                "contributor_id": contributor["_id"],
                "project_id": contributor["interested_project"],
            }
        return instance.client.post(
            url=instance.base_url + "maintainer/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {maintainer_jwt}"},
            },
        )

    def set_alpha_password(self, instance):
        password = str(secrets.token_hex(8))
        doc = {"email": "rmukh561@gmail.com", "password": password, "reset": True}
        instance.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        instance.db.maintainer_credentials.find_one_and_update(
            {"$and": [{"email": "rmukh561@gmail.com"}, {"reset": True}]},
            update={"$set": {"password": self.hash_password(password), "reset": False}},
        )

    def set_beta_password(self, instance):
        password = str(secrets.token_hex(8))
        doc = {"email": "rijumukh50601@gmail.com", "password": password, "reset": True}
        instance.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        instance.db.maintainer_credentials.find_one_and_update(
            {"$and": [{"email": "rijumukh50601@gmail.com"}, {"reset": True}]},
            update={"$set": {"password": self.hash_password(password), "reset": False}},
        )

    def login_beta_maintainer(self, instance):
        return instance.client.post(
            url=instance.base_url + "maintainer/login",
            data=json.dumps(self.beta_maintainer_login_data),
            headers=self.base_headers,
        )

    def add_another_alpha(self, instance):
        return instance.client.post(
            url=instance.base_url + "api/maintainer",
            data=json.dumps(self.another_alpha),
            headers=self.base_headers,
            params={"role": "alpha"},
        )

    def get_maintainer_projects(self, instance, maintainer_jwt):
        return instance.client.get(
            url=instance.base_url + "maintainer/projects",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {maintainer_jwt}"},
            },
            params={"page": 1},
        )

    def refresh_maintainer_jwt(self, instance, refresh_token):
        return instance.client.post(
            url=instance.base_url + "refresh-token",
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {refresh_token}"},
            },
        )

    def reject_contributor_maintainer(self, instance, contributor, maintainer_jwt):
        data = {"contributor_id": contributor["_id"]}
        return instance.client.delete(
            url=instance.base_url + "maintainer/projects",
            data=json.dumps(data),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {maintainer_jwt}"},
            },
            params={"role": "contributor"},
        )

    def reset_alpha_password(self, instance, jwt, data=None):
        return instance.client.post(
            url=instance.base_url + "maintainer/reset-password/set",
            data=json.dumps({"password": "test5678"}),
            headers={
                **self.base_headers,
                **{"Authorization": f"Bearer {jwt}"},
            },
        )

    def alpha_password_reset_request(self, instance, url=None):
        if not url:
            url = "maintainer/reset-password/reset"
        password = str(secrets.token_hex(8))

        doc = {"email": "rmukh561@gmail.com", "password": password, "reset": True}
        instance.db.maintainer_credentials.insert_one(document=doc)

        return instance.client.post(
            url=instance.base_url + url,
            data=json.dumps({"email": "rmukh561@gmail.com"}),
            headers=self.base_headers,
        )

    def contact_us(self, instance, data=None):
        if not data:
            data = self.contact_us_data
        return instance.client.post(
            url=instance.base_url + "api/contact-us",
            data=json.dumps(data),
            headers=self.base_headers,
        )
