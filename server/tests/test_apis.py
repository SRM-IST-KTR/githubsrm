import time
from dotenv import load_dotenv
import secrets
from hashlib import sha256
import requests
import pymongo
import unittest
import json
from githubsrm.core.settings import DATABASE
from django.conf import settings

settings.configure(USE_DATABASE='TESTMONGO')

unittest.TestLoader.sortTestMethodsUsing = None


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

    def test_team_data(self):
        '''
        Checks valid response Status form team api
        '''
        response = self.client.get(self.base_url+'api/team')
        self.assertEqual(response.status_code, 200)

    def test_add_alpha(self):
        """
        Add alpha maintainer
        """
        data = {
            "name": "Riju",
            "email": "rmukh561@gmail.com",
            "github_id": "riju561",
            "srm_email": "rm8211@srmist.edu.in",
            "reg_number": "RA1911003010056",
            "branch": "CSE",
            "project_name": "Qwerty",
            "project_url": "",
            "tags": ["a", "b", "c", "d"],
            "description": "abc.asd.wd wdakwdaw dawdkwadaw dawldwadkaw dwadkawkdlawmd awdawodkaw"
        }
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)
        self.clean()

    def test_add_beta(self):
        """
        Add beta maintainer
        """
        data = {
            "name": "Riju",
            "email": "rmukh561@gmail.com",
            "github_id": "riju561",
            "srm_email": "rm8211@srmist.edu.in",
            "reg_number": "RA1911003010056",
            "branch": "CSE",
            "project_name": "Qwerty",
            "project_url": "",
            "tags": ["a", "b", "c", "d"],
            "description": "abc.asd.wd wdakwdaw dawdkwadaw dawldwadkaw dwadkawkdlawmd awdawodkaw"
        }
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "alpha"})
        self.assertEqual(response.status_code, 201)

        id = dict(self.db.maintainer.find_one(
            {"github_id": "riju561"}))["project_id"]
        data = {
            "name": "Riju",
            "email": "rijumukh50601@gmail.com",
            "github_id": "riju",
            "srm_email": "as1234@srmist.edu.in",
            "reg_number": "RA1911003010042",
            "branch": "CSE",
            "project_id": id
        }
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "beta"})
        self.assertEqual(response.status_code, 201)
        self.clean()

    def test_add_contributor(self):
        """
        add contributor
        """
        data = {
            "email": "rmukh561@gmail.com",
            "password": "test"
        }
        response = self.client.post(
            url=self.base_url+'admin/register', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["keys"]
        self.assertEqual(response.status_code, 200)
        data = {
            "name": "Riju",
            "email": "rmukh561@gmail.com",
            "github_id": "riju561",
            "srm_email": "rm8211@srmist.edu.in",
            "reg_number": "RA1911003010056",
            "branch": "CSE",
            "project_name": "Qwerty",
            "project_url": "",
            "tags": ["a", "b", "c", "d"],
            "description": "abc.asd.wd wdakwdaw dawdkwadaw dawldwadkaw dwadkawkdlawmd awdawodkaw"
        }
        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
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
        data = {
            "project_id": alpha["project_id"],
            "project_url": "https://github.com/SRM-IST-KTR/githubsrm",
            "private": True
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})

        self.assertEqual(response.status_code, 200)
        id = dict(self.db.maintainer.find_one(
            {"github_id": "riju561"}))["project_id"]
        data = {
            "name": "Abhishek Saxena",
            "email": "as7122000@gmail.com",
            "srm_email": "as2345@srmist.edu.in",
            "reg_number": "RA1911027010102",
            "branch": "CSE-BD",
            "github_id": "xyz",
            "interested_project": id,
            "poa": "HelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelp"
        }
        response = self.client.post(
            url=self.base_url+'api/contributor', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "contributor"})
        self.assertEqual(response.status_code, 201)
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
