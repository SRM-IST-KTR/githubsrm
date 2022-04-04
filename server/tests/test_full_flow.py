import os
from . import Base
from dotenv import load_dotenv
import secrets
from hashlib import sha256
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

    def test_full_flow(self):
        """
        Register admin
        """
        response = entry.register_admin(self)
        self.assertEqual(response.status_code, 200)

        """
        login admin
        """
        response = entry.login_admin(self)
        admin_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)

        """
        Add alpha maintainer
        """
        response = entry.add_alpha_maintainer(self)
        self.assertEqual(response.status_code, 201)

        """
        Add beta maintainer
        """
        id = dict(self.db.maintainer.find_one({"github_id": "riju561"}))["project_id"]
        response = entry.add_beta_maintainer(self, None, id)
        self.assertEqual(response.status_code, 201)

        """
        set alpha maintainer password
        """
        entry.set_alpha_password(self)
        """
        set beta maintainer password
        """
        entry.set_beta_password(self)
        """
        get projects from admin
        """
        entry.get_projects_admin(self, id, admin_jwt)
        """
        approve alpha maintainer from admin
        """
        alpha = dict(self.db.maintainer.find_one({"github_id": "riju561"}))
        response = entry.approve_alpha_maintainer(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)
        """
        approve beta maintainer from admin
        """
        beta = dict(self.db.maintainer.find_one({"github_id": "riju"}))
        response = entry.approve_beta_maintainer(self, beta, admin_jwt)
        self.assertEqual(response.status_code, 200)
        """
        approve project from admin
        """
        response = entry.approve_project(self, alpha, admin_jwt)
        self.assertEqual(response.status_code, 200)
        """
        add contributor
        """
        response = entry.add_contributor(self, alpha)
        self.assertEqual(response.status_code, 201)
        """
        approve contributor from admin
        """
        contri = dict(self.db.contributor.find_one({"github_id": "xyz"}))
        response = entry.approve_contributor_admin(self, contri, admin_jwt)
        self.assertEqual(response.status_code, 200)
        """
        login maintainer
        """
        response = entry.login_maintainer(self)
        maintainer_jwt = response.json()["access_token"]
        self.assertEqual(response.status_code, 200)
        """
        approve contributor from maintainer
        """
        entry.approve_contributor_maintainer(self, contri, maintainer_jwt)
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.admins.delete_many({})
        cls.db.project.delete_many({})
        cls.db.maintainer.delete_many({})
        cls.db.maintainer_credentials.delete_many({})
        cls.db.contributor.delete_many({})
        cls.pymongo_client.close()
        cls.client.close()
