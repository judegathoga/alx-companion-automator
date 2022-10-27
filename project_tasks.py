import requests
from bs4 import BeautifulSoup as bs
import creds



def login(email, password, project_num):
    signin_url = 'https://alx-intranet.hbtn.io/auth/sign_in'
    project_url = 'https://alx-intranet.hbtn.io/projects/' + str(project_num) 

    with requests.session() as s:

        # Response returned by GET request from server before login
        site = s.get(signin_url)
        site_content = bs(site.content, 'html.parser')
        
        # Each login session has a different auth token
        token = site_content.find('input', {'name': 'authenticity_token'})['value']

        # Auth Payloads
        payload = {
            'authenticity_token' : token,
            'user[email]': email,
            'user[password]': password,
            'user[remember_me]': 1,
            'commit' : 'Log in'
        }

        # Login with user credentials to the project page
        s.post(signin_url, data=payload)
    
        # Request for the appropriate project page
        response = s.get(project_url)

        # Contents of the webpage in bs4 format
        global souped_body
        souped_body = bs(response.content, 'html.parser')
        

     

login(creds.username, creds.password, 229)
