import unittest
import os
from dotenv import load_dotenv
import requests
import pymongo
import time
import unittest
from hashlib import sha256
import secrets
import json
from githubsrm.core.settings import DATABASE
from . import Base

entry=Base()
class TestSchema(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()

        cls.client = requests.Session()
        cls.pymongo_client = pymongo.MongoClient(DATABASE['mongo_uri'])
        cls.db = cls.pymongo_client[os.getenv("TestDB")]

        cls.base_url = "http://localhost:8000/"
        cls.webhook = list(cls.db.webHook.find({}))[0]["token"]

    def test_schema_alpha(self):
        self.clean()
        for i in entry.alpha_data.keys():
            time.sleep(1)
            data = entry.alpha_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "alpha"})
            self.assertEqual(response.status_code, 400)

        for i in entry.alpha_data.keys():
            if i=="project_url":
                continue
            time.sleep(1)
            data = entry.alpha_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "alpha"})
            self.assertEqual(response.status_code, 400)

        for i in entry.alpha_data.keys():
            time.sleep(1)
            data = entry.alpha_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "alpha"})
            self.assertEqual(response.status_code, 400)
        self.clean()

    def test_schema_beta(self):
        self.clean()
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(entry.alpha_data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one(
            {"github_id": "riju561"}))["project_id"]

        for i in entry.beta_data.keys():
            time.sleep(1)
            data = entry.beta_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps({**data, **{"project_id": id}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "beta"})
            self.assertEqual(response.status_code, 400)

        for i in entry.beta_data.keys():
            time.sleep(1)
            data = entry.beta_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps({**data, **{"project_id": id}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "beta"})
            self.assertEqual(response.status_code, 400)

        for i in entry.beta_data.keys():
            time.sleep(1)
            data = entry.beta_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps({**data, **{"project_id": id}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "beta"})
            self.assertEqual(response.status_code, 400)
        self.clean()

    def test_schema_contributor(self):
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

        for i in entry.contributor_data.keys():
            time.sleep(1)
            data = entry.contributor_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'api/contributor', data=json.dumps({**data, **{"interested_project": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)

        for i in entry.contributor_data.keys():
            time.sleep(1)
            data = entry.contributor_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'api/contributor', data=json.dumps({**data, **{"interested_project": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)

        for i in entry.contributor_data.keys():
            time.sleep(1)
            data = entry.contributor_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'api/contributor', data=json.dumps({**data, **{"interested_project": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)
        self.clean()
    
    def test_project_approval_schema(self):
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
        for i in entry.project_details.keys():
            time.sleep(1)
            data = entry.project_details.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps({**data, **{"project_id": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "project"})
            self.assertEqual(response.status_code, 400)
        
        for i in entry.project_details.keys():
            time.sleep(1)
            data = entry.project_details.copy()
            data[i]=""
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps({**data, **{"project_id": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "project"})
            self.assertEqual(response.status_code, 400)
        
        for i in entry.project_details.keys():
            time.sleep(1)
            data = entry.project_details.copy()
            data[i]=" "
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps({**data, **{"project_id": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "project"})
            self.assertEqual(response.status_code, 400)
        self.clean()
    
    def test_alpha_maintainer_approval_schema(self):
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
        alpha_data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"]
        }
        for i in alpha_data.keys():
            time.sleep(1)
            data = alpha_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "maintainer"})
            self.assertEqual(response.status_code, 400)

        for i in alpha_data.keys():
            time.sleep(1)
            data = alpha_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "maintainer"})
            self.assertEqual(response.status_code, 400)

        for i in alpha_data.keys():
            time.sleep(1)
            data = alpha_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "maintainer"})
            self.assertEqual(response.status_code, 400)
        
        self.clean()

    def test_beta_maintainer_approval_schema(self):
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
        beta_data = {
            "maintainer_id": beta["_id"],
            "project_id": beta["project_id"],
            "email": beta["email"]
        }
        for i in beta_data.keys():
            time.sleep(1)
            data = beta_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "maintainer"})
            self.assertEqual(response.status_code, 400)
        
        for i in beta_data.keys():
            time.sleep(1)
            data = beta_data.copy()
            data[i]=""
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "maintainer"})
            self.assertEqual(response.status_code, 400)
        
        for i in beta_data.keys():
            time.sleep(1)
            data = beta_data.copy()
            data[i]=" "
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "maintainer"})
            self.assertEqual(response.status_code, 400)
        self.clean()

    def test_contributor_approval_admin_schema(self):
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
        contri_data = {
            "contributor_id": contri["_id"],
            "project_id": contri["interested_project"],
        }
        for i in contri_data.keys():
            time.sleep(1)
            data = contri_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)

        for i in contri_data.keys():
            time.sleep(1)
            data = contri_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)

        for i in contri_data.keys():
            time.sleep(1)
            data = contri_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {admin_jwt}"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)
        self.clean()
    
    def test_contributor_approval_maintainer_schema(self):
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

        contri_data = {
            "contributor_id": contri["_id"],
            "project_id": contri["interested_project"]
        }
        for i in contri_data.keys():
            time.sleep(1)
            data = contri_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'maintainer/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {maintainer_jwt}"
                })
            self.assertEqual(response.status_code, 400)

        for i in contri_data.keys():
            time.sleep(1)
            data = contri_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'maintainer/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {maintainer_jwt}"
                })
            self.assertEqual(response.status_code, 400)

        for i in contri_data.keys():
            time.sleep(1)
            data = contri_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'maintainer/projects', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                    "Authorization": f"Bearer {maintainer_jwt}"
                })
            self.assertEqual(response.status_code, 400)
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
