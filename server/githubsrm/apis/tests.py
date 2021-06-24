import re
from django.test import TestCase
from .definations import TeamSchema, CommonSchema


class TestSchema(TestCase):
    def test_valid_data(self):
        test_valid_data = TeamSchema({
            "name": "Someone",
            "github_id": "Aradhya-Tripathi",
            "linkedin": "https://samplelinkedin.com",
            "img_url": "http://sampleimage.com",
            "tagline": "Sample TagLine",
        })

        result = 'error' in test_valid_data.valid()
        self.assertEqual(result, False)

        test_valid_data = CommonSchema({
            "name": "TestUser",
            "email": "testuser@localhost.com",
            "srm_email": "at8029@srmist.edu.in",
            "reg_number": "RA6969696969696",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "Cool Project"

        })

        result = 'error' in test_valid_data.valid()
        self.assertEqual(result, False)

    def test_invalid_data(self):
        test_invalid_data = TeamSchema({
            "name": "Someone",
            "linkedin": "invalid url",
            "github_id": 123,
            "img_url": "http://sampleimage.com",
            "tagline": "Sample TagLine"
        })

        result = 'error' in test_invalid_data.valid()
        self.assertEqual(result, True)

        test_invalid_data = CommonSchema({
            "name": "TestUser",
            "email": "testuser@gmail.com",
            "srm_email": "tu6969@smrist.edu.in",
            "reg_number": "123123123",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "Cool Project" 
        })

        result = 'error' in test_invalid_data.valid()
        self.assertEqual(result, True) 