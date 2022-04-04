import os
from dotenv import load_dotenv
import requests
import pymongo
import unittest
import json
from githubsrm.core.settings import DATABASE
from . import Base

entry = Base()


class TestClient(unittest.TestCase):
    """
    Integration tests
    """

    @classmethod
    def setUpClass(cls) -> None:

        load_dotenv()

        cls.client = requests.Session()
        cls.pymongo_client = pymongo.MongoClient(DATABASE["mongo_uri"])
        cls.db = cls.pymongo_client[os.getenv("TestDB")]

        cls.base_url = "http://localhost:8000/"
        cls.webhook = list(cls.db.webHook.find({}))[0]["token"]

    def test_team_data(self):
        """
        Checks valid response Status form team api
        """
        response = self.client.get(self.base_url + "api/team")
        self.assertEqual(response.status_code, 200)

    def test_add_alpha(self):
        """
        Add alpha maintainer
        """
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)
        self.clean()

    def test_add_beta(self):
        """
        Add beta maintainer
        """
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]

        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 201)
        self.clean()

    def test_add_contributor(self):
        """
        add contributor
        """
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
        self.clean()

    def test_add_maintainer_after_contributor(self):
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

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]
        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 201)

        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 400)
        self.clean()

    def test_add_maintainer_as_contributor(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))

        response = entry.add_beta_maintainer(self, alpha)
        self.assertEqual(response.status_code, 201)

        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        data = {
            **entry.beta_data,
            **{
                "poa": "HelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelp"
            },
        }
        response = entry.add_contributor(self, alpha, data)
        self.assertEqual(response.status_code, 409)
        self.clean()

    def test_same_alpha_and_beta_maintainer(self):
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]

        data = {
            "name": "Riju",
            "email": "rmukh561@gmail.com",
            "github_id": "riju561",
            "srm_email": "rm8211@srmist.edu.in",
            "reg_number": "RA1911003010056",
            "branch": "CSE",
        }
        response = entry.add_beta_maintainer(self, None, id, data)
        self.assertEqual(response.status_code, 409)
        self.clean()

    def test_add_duplicate_project(self):
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 409)
        self.clean()

    def test_add_contributor_before_accepting_project(self):
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))

        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 400)
        self.clean()

    def test_add_duplicate_beta(self):
        self.clean()
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]

        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 201)

        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 409)
        self.clean()

    def test_health_check(self):
        response = self.client.get(
            url=self.base_url + "api/healthcheck",
            headers={
                "Content-type": "application/json",
                "X-RECAPTCHA-TOKEN": "TestToken",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_contact_us(self):
        self.clean()
        response = entry.contact_us(self)
        self.assertEqual(response.status_code, 201)
        self.clean()

    def test_duplicate_contact_us(self):
        self.clean()
        response = self.client.post(
            url=self.base_url + "api/contact-us",
            data=json.dumps(entry.contact_us_data),
            headers={
                "Content-type": "application/json",
                "X-RECAPTCHA-TOKEN": "TestToken",
            },
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            url=self.base_url + "api/contact-us",
            data=json.dumps(entry.contact_us_data),
            headers={
                "Content-type": "application/json",
                "X-RECAPTCHA-TOKEN": "TestToken",
            },
        )
        self.assertEqual(response.status_code, 409)
        self.clean()

    def test_get_all_public_projects(self):
        response = self.client.get(url=self.base_url + "api/maintainer")
        self.assertEqual(response.status_code, 200)

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
