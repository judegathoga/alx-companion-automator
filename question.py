# Handles all the logic for displaying project questions, answering, submitting, and returning 
# correctness feedback
from bs4 import BeautifulSoup as bs
import markdownify

class Question:
    project_body = bs
    
    def __init__(self, project) -> None:
        self.project_body = project


    # Displays the particular question
    def __display(self, question) -> str: 
        # Format the question in README fashion
        question = markdownify.markdownify(str(question), heading_style='ATX', bullets="\u25a2")
        lines = question.split('\n')

        formatted_question = '\n'.join(lines[3:])
        return formatted_question.strip()

    # Receives the user's responses
    def answer(self):
        # A list of all the questions
        question_list = self.project_body.find_all('div', {'class' : 'quiz_question_item_container'})

        for question in question_list:
            print(self.__display(question))
            responses = input('Type your answer(s) in form of letters (A, B, C). Seperate by commas for multiple-choice questions')
            

