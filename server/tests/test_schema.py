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

entry = Base()


class TestSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        load_dotenv()

        cls.client = requests.Session()
        cls.pymongo_client = pymongo.MongoClient(DATABASE["mongo_uri"])
        cls.db = cls.pymongo_client[os.getenv("TestDB")]

        cls.base_url = "http://localhost:8000/"
        cls.webhook = list(cls.db.webHook.find({}))[0]["token"]

    def test_schema_alpha(self):
        self.clean()
        for j in [0, "", " ", None]:
            for i in entry.alpha_data.keys():
                time.sleep(1)
                if i == "project_url" and j == "":
                    continue
                data = entry.alpha_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.add_alpha_maintainer(self, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_schema_beta(self):
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]

        for j in [0, "", " ", None]:
            for i in entry.beta_data.keys():
                time.sleep(1)
                data = entry.beta_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.add_beta_maintainer(self, None, id, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_schema_contributor(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        for j in [0, "", " ", None]:
            for i in entry.contributor_data.keys():
                time.sleep(1)
                data = entry.contributor_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.add_contributor(self, alpha, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_project_approval_schema(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        for j in [0, "", " ", None]:
            for i in entry.project_details.keys():
                time.sleep(1)
                data = entry.project_details.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.approve_project(self, alpha, admin_jwt, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_alpha_maintainer_approval_schema(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        alpha_data = {
            "maintainer_id": alpha["_id"],
            "project_id": alpha["project_id"],
            "email": alpha["email"],
        }

        for j in [0, "", " ", None]:
            for i in alpha_data.keys():
                time.sleep(1)
                data = alpha_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.approve_alpha_maintainer(self, alpha, admin_jwt, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_beta_maintainer_approval_schema(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]

        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 201)

        beta = dict(self.db.maintainer.find_one({"github_id": "riju"}))
        beta_data = {
            "maintainer_id": beta["_id"],
            "project_id": beta["project_id"],
            "email": beta["email"],
        }

        for j in [0, "", " ", None]:
            for i in beta_data.keys():
                time.sleep(1)
                data = beta_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.approve_beta_maintainer(self, beta, admin_jwt, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_contributor_approval_admin_schema(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 201)

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        contri_data = {
            "contributor_id": contri["_id"],
            "project_id": contri["interested_project"],
        }

        for j in [0, "", " ", None]:
            for i in contri_data.keys():
                time.sleep(1)
                data = contri_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.approve_contributor_admin(
                    self, contri, admin_jwt, data
                )
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_contributor_approval_maintainer_schema(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 201)

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        response = entry.approve_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        contri_data = {
            "contributor_id": contri["_id"],
            "project_id": contri["interested_project"],
        }

        for j in [0, "", " ", None]:
            for i in contri_data.keys():
                time.sleep(1)
                data = contri_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.approve_contributor_maintainer(
                    self, contri, maintainer_jwt, data
                )
                self.assertEqual(response.status_code, 400)
        self.clean()

    def test_contact_us_schema(self):
        self.clean()

        for j in [0, "", " ", None]:
            for i in entry.contact_us_data.keys():
                time.sleep(1)
                if i == "phone_number" and j == "":
                    continue
                data = entry.contact_us_data.copy()
                if j == 0:
                    del data[i]
                else:
                    data[i] = j
                response = entry.contact_us(self, data)
                self.assertEqual(response.status_code, 400)
        self.clean()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.admins.delete_many({})
        cls.db.project.delete_many({})
        cls.db.maintainer.delete_many({})
        cls.db.maintainer_credentials.delete_many({})
        cls.db.contributor.delete_many({})
        cls.db.contactUs.delete_many({})
        cls.pymongo_client.close()
        cls.client.close()

    def clean(self):
        self.db.admins.delete_many({})
        self.db.project.delete_many({})
        self.db.maintainer.delete_many({})
        self.db.maintainer_credentials.delete_many({})
        self.db.contributor.delete_many({})
        self.db.contactUs.delete_many({})
