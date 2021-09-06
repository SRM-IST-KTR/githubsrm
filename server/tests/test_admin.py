import os
from . import Base
from dotenv import load_dotenv
import requests
import pymongo
import unittest
import json
from githubsrm.core.settings import DATABASE

entry = Base()


class TestClient(unittest.TestCase):
    '''
    Integration tests
    '''
    @classmethod
    def setUpClass(cls) -> None:

        load_dotenv()

        cls.client = requests.Session()
        cls.pymongo_client = pymongo.MongoClient(DATABASE['mongo_uri'])
        cls.db = cls.pymongo_client[os.getenv("TestDB")]

        cls.base_url = "http://localhost:8000/"
        cls.webhook = list(cls.db.webHook.find({}))[0]["token"]

    def test_register_admin(self):
        """
        Register admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_login_admin(self):
        """
        login admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_get_projects(self):
        """
        get projects from admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps({**entry.beta_data, **{"project_id": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "beta"})
        self.assertEqual(response.status_code, 201)
        beta = dict(self.db.maintainer.find_one({"github_id": "riju"}))
        data = {
            "maintainer_id": beta["_id"],
            "project_id": beta["project_id"],
            "email": beta["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'admin/projects', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"page": 1})

        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps({**entry.project_details, **{"project_id": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'admin/projects', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"projectId": alpha["project_id"], "maintainer": True, "contributor": True})
        self.clean()

    def test_approve_alpha(self):
        """
        approve alpha maintainer from admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_approve_beta(self):
        """
        approve beta maintainer from admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        id = dict(self.db.maintainer.find_one(
            {"github_id": "riju561"}))["project_id"]

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps({**entry.beta_data, **{"project_id": id}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "beta"})
        self.assertEqual(response.status_code, 201)

        beta = dict(self.db.maintainer.find_one({"github_id": "riju"}))
        data = {
            "maintainer_id": beta["_id"],
            "project_id": beta["project_id"],
            "email": beta["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_approve_project(self):
        """
        approve project from admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps({**entry.project_details, **{"project_id": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_approve_contributor_admin(self):
        """
        approve contributor from admin
        """
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps({**entry.project_details, **{"project_id": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        print(response.json())
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/contributor', data=json.dumps({**entry.contributor_data, **{"interested_project": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "contributor"})
        self.assertEqual(response.status_code, 201)

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        data = {
            "contributor_id": contri["_id"],
            "project_id": contri["interested_project"],
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "contributor"})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_get_accepted_projects(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps({**entry.project_details, **{"project_id": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'admin/projects/accepted', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"page": 1})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_wrong_webhook(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer 903814ir9i03i149iew9023ie2k0iqwq9i0e8q20321wdjioqi3jwip9qejqe90q3rc8hw3ndowiqqjo8jdoqdijq92dqwopd9q2jeq20="
            })
        self.assertEqual(response.status_code, 403)
        self.clean()

    def test_approve_maintainer_w_wrong_jwt(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6dHJ1ZSwidXNlciI6InJtdWtoNTYxQGdtYWlsLmNvbSIsImV4cCI6MTYyNzQ0NDY2NH0.CYJbJ2thNV_7HV7x2cvTGgkOVwOnIqeuYTrgQ1RIuto"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 401)
        self.clean()

    def test_approve_maintainer_w_wrong_jwt_none_algo(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhZG1pbiI6dHJ1ZSwidXNlciI6InJtdWtoNTYxQGdtYWlsLmNvbSIsImV4cCI6MTYyNzQ0NDY2NH0."
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 401)
        self.clean()

    def test_maintainer_rejection(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"]
        }
        response = self.client.delete(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_contributor_rejection(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps({**entry.project_details, **{"project_id": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/contributor', data=json.dumps({**entry.contributor_data, **{"interested_project": alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "contributor"})
        self.assertEqual(response.status_code, 201)

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        data = {
            "contributor_id": contri["_id"]
        }
        response = self.client.delete(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "contributor"})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_me_route(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'me', headers={
                "Content-type": "application/json", "Authorization": f"Bearer {admin_jwt}"
            })
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_me_route_w_wrong_jwt(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(entry.admin_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'me', headers={
                "Content-type": "application/json", "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 401)
        self.clean()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.admins.delete_many({})
        cls.db.project.delete_many({})
        cls.db.maintainer.delete_many({})
        cls.db.maintainer_credentials.delete_many({})
        cls.db.contributor.delete_many({})
        cls.pymongo_client.close()
        cls.client.close()

    def clean(self):
        self.db.admins.delete_many({})
        self.db.project.delete_many({})
        self.db.maintainer.delete_many({})
        self.db.maintainer_credentials.delete_many({})
        self.db.contributor.delete_many({})
