from django.conf import settings

settings.configure(USE_DATABASE='TESTMONGO')
class Base:
    def __init__(self) -> None:
        self.alpha_data = {
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
        self.admin_data={
            "email": "rmukh561@gmail.com",
            "password": "test"
        }
        self.beta_data = {
            "name": "Riju",
            "email": "rijumukh50601@gmail.com",
            "github_id": "riju",
            "srm_email": "as1234@srmist.edu.in",
            "reg_number": "RA1911003010042",
            "branch": "CSE",
        }
        self.contributor_data={
            "name": "Abhishek Saxena",
            "email": "as7122000@gmail.com",
            "srm_email": "as2345@srmist.edu.in",
            "reg_number": "RA1911027010102",
            "branch": "CSE-BD",
            "github_id": "xyz",
            "poa": "HelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelpHelp"
        }
        self.maintainer_login_data={
            "email": "rmukh561@gmail.com",
            "password": "test1234"
        }
        self.beta_maintainer_login_data={
            "email": "rijumukh50601@gmail.com",
            "password": "test1234"
        }
        self.project_details = {
            "project_url": "https://github.com/SRM-IST-KTR/githubsrm",
            "private": True
        }
