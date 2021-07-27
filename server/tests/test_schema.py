import unittest
import os
from dotenv import load_dotenv
import requests
import pymongo
import unittest
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
            data = entry.alpha_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "alpha"})
            self.assertEqual(response.status_code, 400)

        for i in entry.alpha_data.keys():
            data = entry.alpha_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "alpha"})
            self.assertEqual(response.status_code, 400)  # breaking? github_id

        for i in entry.alpha_data.keys():
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
            data = entry.beta_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps({**data, **{"project_id": id}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "beta"})
            self.assertEqual(response.status_code, 400)

        for i in entry.beta_data.keys():
            data = entry.beta_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'api/maintainer', data=json.dumps({**data, **{"project_id": id}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "beta"})
            self.assertEqual(response.status_code, 400)  # breaking? github_id

        for i in entry.beta_data.keys():
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
            data = entry.contributor_data.copy()
            del data[i]
            response = self.client.post(
                url=self.base_url+'api/contributor', data=json.dumps({**data, **{"interested_project": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)

        for i in entry.contributor_data.keys():
            data = entry.contributor_data.copy()
            data[i] = ""
            response = self.client.post(
                url=self.base_url+'api/contributor', data=json.dumps({**data, **{"interested_project": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "contributor"})
            self.assertEqual(response.status_code, 400)  # breaking? github_id

        for i in entry.contributor_data.keys():
            data = entry.contributor_data.copy()
            data[i] = " "
            response = self.client.post(
                url=self.base_url+'api/contributor', data=json.dumps({**data, **{"interested_project": alpha["project_id"]}}), headers={
                    "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
                }, params={"role": "contributor"})
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
