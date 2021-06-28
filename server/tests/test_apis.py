from dotenv import load_dotenv

import requests
import pymongo
from unittest import TestCase
import json
from githubsrm.core.settings import DATABASE
from django.conf import settings

settings.configure(USE_DATABASE='TESTMONGO')


class TestClient(TestCase):
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

    def test_team_data(self):
        '''
        Checks valid response Status form team api
        '''

        response = self.client.get(self.base_url+'api/team')
        self.assertEqual(response.status_code, 200)

    def test_maintainer_entry(self):
        '''
        Checks valid maintainer entry
        '''

        data = {
            "name": "Tesuer",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": "Test-User",
            "description": "RandomRandomRandomRandomRandomRandomRandomRandomRandomRandom",
            "tags": ["someone", "said"],
            "project_name": "Tester"
        }

        response = self.client.post(
            url=self.base_url+'api/maintainer', data=json.dumps(data), headers={
                "Content-type": "application/json", "HTTP_X_RECAPTCHA_TOKEN": "TestToken"
            }, params={"role": "alpha"})

        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.project.delete_many({})
        cls.db.maintainer.delete_many({})
        cls.pymongo_client.close()
        cls.client.close()
