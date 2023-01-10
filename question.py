# Handles all the logic for displaying project questions, answering, submitting, and returning 
# correctness feedback
from bs4 import BeautifulSoup as bs
import markdownify

class Questions:    
    # Raises an AttributeError if the project has no questions
    def __init__(self, proj_body) -> None:
        # # A list of all the questions
        self.question_list = proj_body.find_all('div', {'class' : 'quiz_question_item_container'})

        # A list of each Question object
        self.question_objs = []

        if not self.__check_questions:
            raise AttributeError('This Question Object (Project page), has no questions attached to it')
        self.__populate_question_ids()

    # Check if the project has questions
    @property
    def __check_questions(self) -> bool:
        return len(self.question_list) > 0
            
    
    @classmethod
    # Displays the particular question
    def display(cls, question) -> str: 
        # Format the question in README fashion
        question = markdownify.markdownify(str(question), heading_style='ATX', bullets="\u25a2")
        lines = question.split('\n')

        formatted_question = '\n'.join(lines[3:])
        return formatted_question.strip()
    
    # Populates the question_ids dictionary with each question's id and answer-choice ids
    def __populate_question_ids(self):
        for question in self.question_list:
            quest = Question(question)
            self.question_objs.append(quest)
    
    def answer(self):
        for question in self.question_objs:
            print(question)
        


class Question:
    def __init__(self, question_body: bs) -> None:
        self.question = question_body
        self.question_id = None
        self.answer_ids = None
        self.is_multiple_choice = False
        self.__populate_fields()

    def __populate_fields(self):
        html_cont =  bs(self.question.decode(), 'html.parser')
        # Question ID
        self.question_id = html_cont.find('ul', {'class': 'quiz_question_answers'})['data-question-id'] 
        
        # All answer ids for this particular question
        self.answer_ids = [ans_id['data-quiz-answer-id'] for ans_id in html_cont.find_all('input', {'name' : self.question_id})] 
        
        # Check if the answers allow multiple selection or not
        self.is_multiple_choice = "checkbox" in self.question.decode()

    def __str__(self) -> str:
        quest_str = '===================================================================================\n'
        quest_str += f'Question:\n{Questions.display(self.question)}\n\nQuestion_id: {self.question_id}\nAnswer IDs: {self.answer_ids}\nAnswers: {"Multi-choice" if self.is_multiple_choice else "Single-Choice"} \n'
        quest_str += '===================================================================================\n\n'
        return quest_str

        
        