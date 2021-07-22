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

    def test_full_flow(self):
        """
        Register admin
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

        """
        login admin
        """
        response = self.client.post(
            url=self.base_url+'admin/login', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {self.webhook}"
            })
        admin_jwt = response.json()["keys"]
        self.assertEqual(response.status_code, 200)

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

        """
        Add beta maintainer
        """
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

        """
        set alpha maintainer password
        """
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

        """
        set beta maintainer password
        """
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

        """
        get projects from admin
        """
        response = self.client.get(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"page": 1})
        response = self.client.get(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"projectId": id, "maintainer": True, "contributor": True})
        """
        approve alpha maintainer from admin
        """
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
        """
        approve beta maintainer from admin
        """
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
        """
        approve project from admin
        """
        data = {
            "project_id": beta["project_id"],
            "project_url": "https://github.com/SRM-IST-KTR/githubsrm",
            "private": True
        }
        response = self.client.post(
            url=self.base_url+'admin/projects', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken",
                "Authorization": f"Bearer {admin_jwt}"
            }, params={"role": "project"})
        self.assertEqual(response.status_code, 200)
        """
        add contributor
        """
        data = {
            "name": "Abhishek Saxena",
            "email": "as7122000@gmail.com",
            "srm_email": "as2345@srmist.edu.in",
            "reg_number": "RA1911027010102",
            "branch": "CSE-BD",
            "github_id": "xyz",
            "interested_project": beta["project_id"],
            "poa": "HelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelp"
        }
        response = self.client.post(
            url=self.base_url+'api/contributor', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            }, params={"role": "contributor"})
        self.assertEqual(response.status_code, 201)
        """
        approve contributor from admin
        """
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
        """
        login maintainer
        """
        data = {
            "email": "rmukh561@gmail.com",
            "password": "test1234"
        }
        response = self.client.post(
            url=self.base_url+'maintainer/login', data=json.dumps(data), headers={
                "Content-type": "application/json", "X-RECAPTCHA-TOKEN": "TestToken"
            })
        maintainer_jwt = response.json()["key"]
        self.assertEqual(response.status_code, 200)
        """
        approve contributor from maintainer
        """
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.admins.delete_many({})
        cls.db.project.delete_many({})
        cls.db.maintainer.delete_many({})
        cls.db.maintainer_credentials.delete_many({})
        cls.db.contributor.delete_many({})
        cls.pymongo_client.close()
        cls.client.close()
