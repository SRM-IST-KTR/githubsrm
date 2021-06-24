import re
from django.test import TestCase
from githubsrm.apis.definations import TeamSchema, CommonSchema


class TestSchema(TestCase):
    def test_common_schema(self):
        schema = CommonSchema(data={
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "TestProject",

        }, headers={
            "path_info": "/apis/contributor"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, False)

        schema = CommonSchema(data={
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": 123,
            "branch": "ECE",
            "github_id": "Test-User",
        }, headers={
            "path_info": "/apis/contributor"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, True)

        schema = CommonSchema(data={
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": ["Test-User", "Test-User2"],
            "project_url": "https://github.com",
            "poa": "This is the POA"

        }, headers={
            "path_info": "/apis/maintainer"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, False)

        schema = CommonSchema(data={
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": ["Test-User"],
            "poa": "This is the poa"

        }, headers={
            "path_info": "/apis/maintainer"
        })

        schema = CommonSchema(data={
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": ["Test-User"],
            "project_url": "github.com"

        }, headers={
            "path_info": "/apis/maintainer"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_team_schema(self):
        schema = TeamSchema(data={
            "name": "Aradhya",
            "github_id": "Aradhya-Tripathi",
            "linkedin": "https://linkedin.com",
            "img_url": "https://image.com",
            "tagline": "This is the tag line"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, False)

        schema = TeamSchema(data={
            "name": "Aradhya",
            "github_id": "Aradhya-Tripathi",
            "linkedin": "incorrect Link",
            "img_url": "incorrect img",
            "tagline": "This is the tag line"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, True)
