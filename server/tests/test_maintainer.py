from dotenv import load_dotenv
import secrets
from hashlib import sha256
import requests
import pymongo
import unittest
import json
from githubsrm.core.settings import DATABASE
from . import Base

entry=Base()
class TestClient(unittest.TestCase):
    '''
    Integration tests
    '''
    @classmethod
    def setUpClass(cls) -> None:

        load_dotenv()

        cls.client = requests.Session()
        cls.pymongo_client = pymongo.MongoClient(DATABASE['mongo_uri'])
        cls.db = cls.pymongo_client[DATABASE['db']]

        cls.base_url = "http://localhost:8000/"
        cls.webhook = list(cls.db.webHook.find({}))[0]["token"]

    def test_maintainer_login(self):
        """
        login maintainer
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

        password = str(secrets.token_hex(8))

        doc = {"email": "rmukh561@gmail.com",
               "password": password,
               "reset": True}
        self.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": "rmukh561@gmail.com"},
                {"reset": True}
            ]
        }, update={
            "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
        })
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(entry.maintainer_login_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_approve_contributor_maintainer(self):
        """
        approve contributor from maintainer
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
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/contributor', data=json.dumps({**entry.contributor_data, **{"interested_project": alpha["project_id"] }}), headers={
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

        password = str(secrets.token_hex(8))

        doc = {"email": "rmukh561@gmail.com",
               "password": password,
               "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": "rmukh561@gmail.com"},
                {"reset": True}
            ]
        }, update={
            "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
        })
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(entry.maintainer_login_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        data = {
            "contributor_id": contri["_id"],
            "project_id": contri["interested_project"]
        }
        response = self.client.post(
            url=self.base_url+'maintainer/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {maintainer_jwt}"
            })
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_set_alpha_password(self):
        """
        set alpha maintainer password
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

        password = str(secrets.token_hex(8))

        doc = {"email": "rmukh561@gmail.com",
               "password": password,
               "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": "rmukh561@gmail.com"},
                {"reset": True}
            ]
        }, update={
            "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
        })
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(entry.maintainer_login_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_set_beta_password(self):
        """
        set beta password
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

        password = str(secrets.token_hex(8))

        doc = {"email": "rijumukh50601@gmail.com",
               "password": password,
               "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": "rijumukh50601@gmail.com"},
                {"reset": True}
            ]
        }, update={
            "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
        })
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(entry.beta_maintainer_login_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_all_and_single_project_pagination(self):
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
        password = str(secrets.token_hex(8))

        doc = {"email": "rmukh561@gmail.com",
               "password": password,
               "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": "rmukh561@gmail.com"},
                {"reset": True}
            ]
        }, update={
            "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
        })
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(entry.maintainer_login_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        maintainer_jwt=response.json()["access_token"]
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            url=self.base_url+'maintainer/projects', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {maintainer_jwt}"
            }, params={"page": 1})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'maintainer/projects', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {maintainer_jwt}"
            }, params={"projectId": alpha["project_id"], "maintainer": 1, "contributor": 1})
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_refresh_token(self):
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

        maintainer=list(self.db.maintainer.find({"github_id":"riju561"}))
        alpha = maintainer[0]
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

        password = str(secrets.token_hex(8))

        doc = {"email": "rmukh561@gmail.com",
               "password": password,
               "reset": True}

        self.db.maintainer_credentials.insert_one(document=doc)
        password = "test1234"
        self.db.maintainer_credentials.find_one_and_update({
            "$and": [
                {"email": "rmukh561@gmail.com"},
                {"reset": True}
            ]
        }, update={
            "$set": {"password": sha256(password.encode()).hexdigest(), "reset": False}
        })
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(entry.maintainer_login_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        
        maintainer_jwt = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.another_alpha), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        another_alpha=list(self.db.maintainer.find({"github_id":"riju561"}))[1]

        data = {
            "maintainer_id": another_alpha["_id"],
            "project_id": another_alpha["project_id"],
            "email": another_alpha["email"]
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "maintainer"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps({**entry.another_project_details, **{"project_id": another_alpha["project_id"]}}), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url=self.base_url+'maintainer/projects', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {maintainer_jwt}"
            },params={"page":1})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(
            url=self.base_url+'refresh-token', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {refresh_token}"
            })
        maintainer_jwt=response.json()["access_token"]
        response = self.client.get(
            url=self.base_url+'maintainer/projects', headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {maintainer_jwt}"
            }, params={"page": 1})
        self.assertEqual(response.status_code, 200)
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
