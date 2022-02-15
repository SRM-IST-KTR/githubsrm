import os
from urllib import response
from . import Base
from dotenv import load_dotenv
import requests
import pymongo
import unittest
import json
from githubsrm.core.settings import DATABASE

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

    def test_register_admin(self):
        """
        Register admin
        """
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_login_admin(self):
        """
        login admin
        """
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_get_projects(self):
        """
        get projects from admin
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

        response = entry.add_beta_maintainer(self, alpha)
        self.assertEqual(response.status_code, 201)

        beta = dict(self.db.maintainer.find_one({"github_id": "riju"}))
        response = entry.approve_beta_maintainer(self, beta, admin_jwt)
        self.assertEqual(response.status_code, 200)

        entry.get_admin_projects(self, alpha, admin_jwt)
        self.clean()

    def test_approve_alpha(self):
        """
        approve alpha maintainer from admin
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
        self.clean()

    def test_approve_beta(self):
        """
        approve beta maintainer from admin
        """
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
        response = entry.approve_beta_maintainer(self, beta, admin_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_approve_project(self):
        """
        approve project from admin
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
        self.clean()

    def test_approve_contributor_admin(self):
        """
        approve contributor from admin
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

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        response = entry.approve_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_get_accepted_projects(self):
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

        response = entry.get_accepted_projects_admin(self, admin_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_wrong_webhook(self):
        self.clean()
        response = entry.register_admin(
            self,
            "903814ir9i03i149iew9023ie2k0iqwq9i0e8q20321wdjioqi3jwip9qejqe90q3rc8hw3ndowiqqjo8jdoqdijq92dqwopd9q2jeq20=",
        )
        self.assertEqual(response.status_code, 403)
        self.clean()

    def test_approve_maintainer_w_wrong_jwt(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(
            self,
            alpha,
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6dHJ1ZSwidXNlciI6InJtdWtoNTYxQGdtYWlsLmNvbSIsImV4cCI6MTYyNzQ0NDY2NH0.CYJbJ2thNV_7HV7x2cvTGgkOVwOnIqeuYTrgQ1RIuto",
        )
        self.assertEqual(response.status_code, 401)
        self.clean()

    def test_approve_maintainer_w_wrong_jwt_none_algo(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(
            self,
            alpha,
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJhZG1pbiI6dHJ1ZSwidXNlciI6InJtdWtoNTYxQGdtYWlsLmNvbSIsImV4cCI6MTYyNzQ0NDY2NH0.",
        )
        self.assertEqual(response.status_code, 401)
        self.clean()

    def test_maintainer_rejection(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.reject_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_contributor_rejection(self):
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
        response = entry.reject_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_me_route(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.get_me_admin(self, admin_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_me_route_w_wrong_jwt(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.get_me_admin(
            self,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        )
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
