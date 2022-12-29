import requests
from bs4 import BeautifulSoup as bs
import creds
import markdownify

s = requests.session() # Global User-Session variable
global project_page


def login(email, password, project_num): # Returns a bs4 object of the project webpage
    signin_url = 'https://alx-intranet.hbtn.io/auth/sign_in'
    project_url = 'https://alx-intranet.hbtn.io/projects/' + str(project_num) 

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
    souped_body = bs(response.content, 'html.parser')
    return souped_body # bs4 project-page object


# Extract repo, directory & file name for each task         
def task_properties():
    task_properties = [] # Directory and file name info for each task

    # Get all div tags with each task's Repo information
    tasks_info = project_page.find_all('div', {'class' : 'list-group-item'})
    
    for task in tasks_info:
        task_info = task.ul.find_all('li') # Info on repo name, directory & file name
        task_dict = {
            'repo_name' : task_info[0].code.text,
            'dir_name' : task_info[1].code.text,  
            'file_name' : task_info[2].code.text,
        }

        task_properties.append(task_dict)
    
    if len(task_properties) < 1:
        print('You have not yet completed your Quiz questions!')
    
    return task_properties

# Extract project description into markdown (READE.md) format
def create_readme():
    title = project_page.find('h1')
    readmes = project_page.find_all('div', {'class' : 'panel panel-default'})
    readme_sect = bs


    if(len(readmes) > 2): # There are at least 2 divs with the class 'panel panel-default'. Those with > 2 include a 'Concepts' section
        # Insert Project's Title before 'Concepts' section
        readmes[0].h3.insert_before(title)
        readmes[0].append(readmes[1])
        readme_sect = readmes[0]
    else:
        # Insert Project's Title before 'Resources' section
        readmes[0].h2.insert_before(title)
        readme_sect = readmes[0]  


    for link in readme_sect.find_all('a'):
        if str(link['href']).startswith('/'): # Exempt fully qualified URLs
            link['href'] = 'https://alx-intranet.hbtn.io' + link['href'] # Change in-page links to the right outbound links
    

    formatted_readme = markdownify.markdownify(str(readme_sect), heading_style='ATX') # Convert html to markdown format
    
    # print(formatted_readme)
    return formatted_readme
    
def questions(): # Returns the list of each project's questions
    question_list = project_page.find_all('div', {'class' : 'quiz_question_item_container'})

    for question in question_list:
       formatted_question = markdownify.markdownify(str(question), heading_style='ATX', bullets='>')
       print(formatted_question)


def submit_answer(project_num):
    submit_url = f'https://alx-intranet.hbtn.io/projects/{project_num}/submit_quiz.json'
    question_list = 

    # Answer Payloads
    payload = {
        'answers': {

        }
    }



project_page = login(creds.username, creds.password, 539)
questions()
