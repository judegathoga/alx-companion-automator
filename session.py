# Handles all the logic for logging in, maintaining session and user information
import requests
from bs4 import BeautifulSoup as bs
import consts

class Session:      
    s = requests.session() # Global User-Session variable

    def login(self, email, password) -> None:
        # Response returned by GET request from server before login
        site = self.s.get(consts.signin_url)
        site_content = bs(site.content, 'html.parser')

        # Each login session has a different auth token
        # Fetch token for this particular session
        token = site_content.find('input', {'name': 'authenticity_token'})['value']

        # Construct the Auth Payloads
        payload = {
            'authenticity_token' : token,
            'user[email]': email,
            'user[password]': password,
            'user[remember_me]': 1,
            'commit' : 'Log in'
        }

        # Login with user credentials to the project page
        self.s.post(consts.signin_url, data=payload)

    # Returns a bs object of the project page
    # Returns a None if a captain log or evaluation has not been completed
    def project_page(self, proj_num):
        proj_url = consts.projects_url + str(proj_num) 
     
        # Request for the appropriate project page
        proj_page = self.s.get(proj_url)

        # Contents of the webpage in bs4 format
        proj_bs = bs(proj_page.content, 'html.parser')

        return proj_bs # bs4 project-page object