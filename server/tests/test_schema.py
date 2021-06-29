from unittest import TestCase, result
from githubsrm.apis.definitions import CommonSchema, ContactUsSchema


class TestSchema(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.alpha = {
            "name": "TestUser",
            "email": "testuser@localhost.com",
            "srm_email": "tu0000@srmist.edu.in",
            "reg_number": "RAXXXXXXXXXXXX",
            "branch": "ECE",
            "github_id": "Aradhya-Tripathi",
            "project_name": "TestProject",
            "project_url": "https://github.com/SRM-IST-KTR/githubsrm",
            "description": "GitHubSRM Community website xxxxxxxxxxxx",
            "tags": ["ai", "ml"]
        }

        cls.contactUs = {
            "name": "TestUser",
            "email": "TestUser@localhost.com",
            "message": "GitHubSRM Community website xxxxxxxxxxxx",
            "phone_number": ""
        }

    def test_1(self):
        """
        Test all correct
        """
        schema = CommonSchema(self.alpha, query_param='alpha')
        result = 'error' in schema.valid()

        self.assertEqual(result, False)

    def test_2(self):
        """
        Test incorrect github id
        """
        self.alpha['github_id'] = "Aradhya-Tri"

        schema = CommonSchema(self.alpha, query_param='alpha')
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_3(self):
        """
        Test incorrect repo url
        """
        self.alpha['project_url'] = "https://github.com/SRM-IST-KTR/githubsr"

        schema = CommonSchema(self.alpha, query_param='alpha')
        result = 'error' in schema.valid()

        self.assertEqual(result, True)

    def test_4(self):
        """
        Test correct contact us schema
        """
        schema = ContactUsSchema(self.contactUs)
        result = 'error' in schema.valid()

        self.assertEqual(result, False)
