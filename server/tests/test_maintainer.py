from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import secrets
from hashlib import sha256
import jwt
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

    def test_maintainer_login(self):
        """
        login maintainer
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_approve_contributor_maintainer(self):
        """
        approve contributor from maintainer
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        entry.approve_contributor_maintainer(self, contri, maintainer_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_set_alpha_password(self):
        """
        set alpha maintainer password
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_set_beta_password(self):
        """
        set beta password
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

        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]
        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 201)

        beta = dict(self.db.maintainer.find_one({"github_id": "riju"}))
        response = entry.approve_beta_maintainer(self, beta, admin_jwt)
        self.assertEqual(response.status_code, 200)

        entry.set_beta_password(self)

        response = entry.login_beta_maintainer(self)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_all_and_single_project_pagination(self):
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 201)

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        response = entry.approve_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.approve_contributor_maintainer(self, contri, maintainer_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.get_projects_admin(self, alpha["project_id"], admin_jwt)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["contributor"]["contributor"]), 1)
        self.assertEqual(len(response.json()["maintainer"]["maintainer"]), 2)
        self.clean()

    def test_refresh_token(self):
        self.clean()
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        maintainer = list(self.db.maintainer.find({"github_id": "riju561"}))
        alpha = maintainer[0]
        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.add_another_alpha(self)
        self.assertEqual(response.status_code, 201)

        another_alpha = list(self.db.maintainer.find({"github_id": "riju561"}))[1]
        response = entry.approve_alpha_maintainer(self, another_alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.get_maintainer_projects(self, maintainer_jwt)
        self.assertEqual(response.status_code, 401)

        response = entry.refresh_maintainer_jwt(self, refresh_token)
        maintainer_jwt = response.json()["access_token"]
        response = entry.get_maintainer_projects(self, maintainer_jwt)
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_maintainer_login_with_admin_jwt(self):
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.get_maintainer_projects(self, "")
        self.assertEqual(response.status_code, 401)
        self.clean()

    def test_wrong_maintainer_credentials_login(self):
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(
            self, {"email": "rmukh561@gmail.com", "password": "testtest"}
        )
        self.assertEqual(response.status_code, 401)
        self.clean()

    def test_query_params(self):
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

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 201)

        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        response = entry.approve_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.get_maintainer_projects(self, maintainer_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.add_alpha_maintainer(
            self,
            {
                "name": "Abhishek Saxena",
                "email": "as7122000@gmail.com",
                "srm_email": "as2345@srmist.edu.in",
                "reg_number": "RA1911027010102",
                "branch": "CSE-BD",
                "github_id": "xyz",
                "project_name": "Qwertz",
                "project_url": "",
                "private": True,
                "tags": ["e", "f", "g", "h"],
                "description": "abc.asd.wddfsdfsdf wdakwdaw dawdkwadaw dawldwadkaw dwadkawkdlawmd awdawodkawdsfsdf asdfafd",
            },
        )
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one({"github_id": "xyz"}))["project_id"]
        response = entry.get_maintainer_projects(self, maintainer_jwt)
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
        response = entry.approve_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)

        entry.set_alpha_password(self)

        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        print(maintainer_jwt)
        self.assertEqual(response.status_code, 200)

        response = entry.reject_contributor_maintainer(self, contri, maintainer_jwt)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_set_password(self):
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

        encoded = jwt.encode(
            payload={
                "email": "rmukh561@gmail.com",
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            key=os.getenv("SIGNATURE"),
        )
        response = entry.reset_alpha_password(self, encoded)
        self.assertEqual(response.status_code, 200)

        response = entry.login_maintainer(
            self, {"email": "rmukh561@gmail.com", "password": "test5678"}
        )
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_set_password_again(self):
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

        encoded = jwt.encode(
            payload={
                "email": "rmukh561@gmail.com",
                "exp": datetime.utcnow() + timedelta(minutes=10),
            },
            key=os.getenv("SIGNATURE"),
        )

        response = entry.reset_alpha_password(self, encoded)
        self.assertEqual(response.status_code, 200)

        response = entry.reset_alpha_password(self, encoded)
        self.assertEqual(response.status_code, 400)
        self.clean()

    def test_reset_password(self):
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

        response = entry.alpha_password_reset_request(self)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.clean()

    def test_wrong_url(self):
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

        response = entry.alpha_password_reset_request(
            self, "admin/reset-password/reset"
        )
        self.assertEqual(response.status_code, 403)
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
