# Handles all the logic for displaying project questions, answering, submitting, and returning 
# correctness feedback
from bs4 import BeautifulSoup as bs
import markdownify
import consts

class Questions:    
    # Raises an AttributeError if the project has no questions
    def __init__(self, proj_body) -> None:
        # # A list of all the questions
        self.questions = proj_body.find_all('div', {'class' : 'quiz_question_item_container'})

        # A list of each Question object
        self.question_objs = []

        if not self.__check_questions:
            raise AttributeError('This Question Object (Project page), has no questions attached to it')
        self.__populate_question_ids()

    # Check if the project has questions
    @property
    def __check_questions(self) -> bool:
        return len(self.questions) > 0
            
    
    # Populates the question_ids dictionary with each question's id and answer-choice ids
    def __populate_question_ids(self):
        for question in self.questions:
            quest = Question(question)
            self.question_objs.append(quest)
    

    def submit(self):
        submit_url = consts.projects_url + str(consts.proj_num) + '/submit_quiz.json'
        answers = {}

        for quest in self.question_objs:
            print(quest)
    
        

class Question:
    def __init__(self, question_body: bs) -> None:
        self.question_bs = question_body # Question plus answers
        self.question = {} # Question_ID : Question
        self.answers = [] # Answers and their ids
        self.is_multiple_choice = False # Checkbox or Radio button?
        self.__populate_fields()

    def __populate_fields(self):
        html_cont =  bs(self.question_bs.decode(), 'html.parser')

        # Question details
        dash = '-----------------------------------------------------\n'
        question = html_cont.p.prettify().strip() + ((dash + html_cont.pre.prettify().strip() + dash) if html_cont.pre is not None else '') # Append the question's code section if it exists
        formatted_quest = markdownify.markdownify(str(question), heading_style='ATX').strip()
        print(formatted_quest)
        
        # Question ID
        question_id = html_cont.find('ul', {'class': 'quiz_question_answers'})['data-question-id'] 
        self.question[question_id] = formatted_quest
        
        # All answer ids for this particular question
        # answers = html_cont.ul.contents
        # print(answers)



        
        # # Check if the answers allow multiple selection or not
        # self.is_multiple_choice = "checkbox" in self.question_body.decode()

    def __str__(self) -> str:
        quest_str = '===================================================================================\n'
        quest_str += f'Question:\n{self.display()}\n\nQuestion_id: {self.question_id}\nAnswer IDs: {self.answer_ids}\nAnswers: {"Multi-choice" if self.is_multiple_choice else "Single-Choice"} \n'
        quest_str += '===================================================================================\n\n'
        return quest_str
    
    # Displays the  question
    def display(self) -> str: 
        # Format the question in README fashion
        question = markdownify.markdownify(str(self.question_bs), heading_style='ATX', bullets="\u25a2")
        lines = question.split('\n')

        formatted_question = '\n'.join(lines[3:])
        return formatted_question.strip()         
        
        