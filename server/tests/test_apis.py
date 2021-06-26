
from unittest import TestCase
from githubsrm.apis.definitions import TeamSchema, CommonSchema


class TestSchema(TestCase):
    def setUp(self) -> None:
        self.ContributorSchema = {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "60d59693278a6b1bbe4fa9df"
        }
        self.MaintainerSchema = {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": ["Test-User"],
            "poa": "TestProject",
            "tags": ["AI", "ML", "ECE"],
            "project_name": "ProjectName"
        }

    def test_1(self):
        '''
        test 1 : No name
        '''
        del self.ContributorSchema["name"]
        del self.MaintainerSchema["name"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_2(self):
        '''
        test 2 : No email
        '''
        del self.ContributorSchema["email"]
        del self.MaintainerSchema["email"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_3(self):
        '''
        test 3 : no srm email
        '''
        del self.ContributorSchema["srm_email"]
        del self.MaintainerSchema["srm_email"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_4(self):
        '''
        test 4 : no registration number
        '''
        del self.ContributorSchema["reg_number"]
        del self.MaintainerSchema["reg_number"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_5(self):
        '''
        test 5 : no branch
        '''
        del self.ContributorSchema["branch"]
        del self.MaintainerSchema["branch"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_6(self):
        '''
        test 6 : no github id
        '''
        del self.ContributorSchema["github_id"]
        del self.MaintainerSchema["github_id"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_7(self):
        '''
        test 7 : no extra details
        '''
        del self.ContributorSchema["interested_project"]
        del self.MaintainerSchema["poa"]
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_8(self):
        '''
        test 8 : name as empty string
        '''
        self.ContributorSchema["name"] = ""
        self.MaintainerSchema["name"] = ""
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.ContributorSchema["name"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["name"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_9(self):
        '''
        test 9 : wrong email format
        '''
        self.ContributorSchema["email"] = "testuserlocalhost.com"
        self.MaintainerSchema["email"] = "testuserlocalhost.com"
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_20(self):
        '''
        test 20 : Empty email
        '''
        self.ContributorSchema["email"] = ""
        self.MaintainerSchema["email"] = ""
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.ContributorSchema["email"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["email"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_10(self):
        '''
        test 10 : wrong srm email format
        '''
        self.ContributorSchema["srm_email"] = "tu6969srmist.edu.in"
        self.MaintainerSchema["srm_email"] = "tu6969srmist.edu.in"
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_11(self):
        '''
        test 11 : Generic email in srm email
        '''
        self.ContributorSchema["srm_email"] = "tu6969@gmail.com"
        self.MaintainerSchema["srm_email"] = "tu6969@gmail.com"
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_19(self):
        '''
        test 19 : Empty email in srm email
        '''
        self.ContributorSchema["srm_email"] = ""
        self.MaintainerSchema["srm_email"] = ""
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.ContributorSchema["srm_email"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["srm_email"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_12(self):
        '''
        test 12 : Wrong registration number(Without RA)
        '''
        self.ContributorSchema["reg_number"] = "1911004010187"
        self.MaintainerSchema["reg_number"] = "1911004010187"
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_13(self):
        '''
        test 13 : Wrong registration number (Wrong length)
        '''
        self.ContributorSchema["reg_number"] = "RA19110040187"
        self.MaintainerSchema["reg_number"] = "RA19110040187"
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_18(self):
        '''
        test 18 : Wrong registration number (Empty)
        '''
        self.ContributorSchema["reg_number"] = ""
        self.MaintainerSchema["reg_number"] = ""
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.ContributorSchema["reg_number"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["reg_number"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_14(self):
        '''
        test 14 : branch as empty string
        '''
        self.ContributorSchema["branch"] = ""
        self.MaintainerSchema["branch"] = ""
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.ContributorSchema["branch"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["branch"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_15(self):
        '''
        test 15 : github_id as empty string or/and empty array
        '''
        self.ContributorSchema["github_id"] = ""
        self.MaintainerSchema["github_id"] = []
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["github_id"] = [""]
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()

        self.assertEqual(result, True)
        self.MaintainerSchema["github_id"] = [" ", " ", " "]
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_16(self):
        '''
        test 16 : extra details check(Empty strings and wrong details)
        '''
        self.ContributorSchema["interested_project"] = ""
        self.MaintainerSchema["poa"] = ""
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.ContributorSchema["interested_project"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)
        self.MaintainerSchema["poa"] = " "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_17(self):
        '''
        test case 17 : All correct
        '''
        schema = CommonSchema(data=self.ContributorSchema, headers={
            "path_info": "/apis/contributor"
        })
        result = 'error' in schema.valid()
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "/apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, False)

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

    def test_20(self):
        """
        Test missing tags
        """
        self.MaintainerSchema["tags"] = ["AI", " "]
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "apis/maintainer"
        })
        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_21(self):
        '''
        Test Project Name
        '''
        self.MaintainerSchema["project_name"] = "  "
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "apis/maintainer"
        })

        result = 'error' in schema.valid()
        self.assertEqual(result, True)

    def test_21(self):
        '''
        Test no project name
        '''

        del self.MaintainerSchema["project_name"]
        schema = CommonSchema(data=self.MaintainerSchema, headers={
            "path_info": "apis/maintainer"
        })
        result = 'error' in schema.valid()

        self.assertEqual(result, True)

    def tearDown(self) -> None:
        self.ContributorSchema = {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": "Test-User",
            "interested_project": "60d59693278a6b1bbe4fa9df"
        }
        self.MaintainerSchema = {
            "name": "Aradhya",
            "email": "testuser@localhost.com",
            "srm_email": "tu6969@srmist.edu.in",
            "reg_number": "RA1911004010187",
            "branch": "ECE",
            "github_id": ["Test-User"],
            "poa": "TestProject"
        }
