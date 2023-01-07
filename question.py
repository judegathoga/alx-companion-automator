# Handles all the logic for displaying project questions, answering, submitting, and returning 
# correctness feedback
from bs4 import BeautifulSoup as bs
import markdownify

class Questions:    
    # Raises an AttributeError if the project has no questions
    def __init__(self, project_page) -> None:
        # A list of all the questions
        self.question_list = project_page.find_all('div', {'class' : 'quiz_question_item_container'})

        # A list of each question id and their respective answer-ids
        self.question_ids = []

        if not self.__check_questions:
            raise AttributeError('This Question Object (Project page), has no questions attached to it')
        self.__populate_question_ids()

    # Check if the project has questions
    @property
    def __check_questions(self) -> bool:
        return len(self.question_list) > 0
            

    # Displays the particular question
    def __display(self, question) -> str: 
        # Format the question in README fashion
        question = markdownify.markdownify(str(question), heading_style='ATX', bullets="\u25a2")
        lines = question.split('\n')

        formatted_question = '\n'.join(lines[3:])
        return formatted_question.strip()
    
    # Populates the question_ids dictionary with each question's id and answer-choice ids
    def __populate_question_ids(self):
        for question in self.question_list:
            html_cont = bs(question.decode(), 'html.parser')
            quest_id = html_cont.find('ul', {'class': 'quiz_question_answers'})['data-question-id'] # Question id
            # All answer ids for this particular question
            answer_ids = [ans_id['data-quiz-answer-id'] for ans_id in html_cont.find_all('input', {'name' : quest_id})] 
            
            quest_ans_id = {quest_id : answer_ids} # Question : Answers id dict
            self.question_ids.append(quest_ans_id)
        


    # Receives the user's responses
    def answer(self):
        for question in self.question_list:
            print(self.__display(question))
            responses = input('Type your answer(s) in form of letters (A B C). Seperate by spaces for multiple-choice questions')


