import Question
from functools import singledispatchmethod
import json
import os

from QuestionMultiAns import QuestionMultiAns
from QuestionOneAns import QuestionOneAns
from QuestionOpen import QuestionOpen


class Questionnaire:
    # id: int = 0
    questions: list[Question]
    name: str
    change: bool = False

    # def __new__(cls, *args, **kwargs):
    #     cls.id += 1
    #     return super().__new__(cls)

    @singledispatchmethod
    def __init__(self, name: str = 'NoName', questions: list[Question] = []):
        self.name = name
        self.questions = questions
        self.change = True

    @classmethod
    def create_instance(cls, file_name: str):
        directory = "./resources"
        file_path = os.path.join(directory, file_name + '.json')
        print(os.listdir(directory))
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                list_question: list[Question] = []
                for i in range(data.get('count')):
                    question = data.get(f'ques{i}')
                    question_type = question.get('type')
                    if question_type == 'qma':
                        list_question.append(
                            QuestionMultiAns(question.get('ques'), question.get('ans')))
                    elif question_type == 'qoa':
                        list_question.append(
                            QuestionOneAns(question.get('ques'), question.get('ans')))
                    elif question_type == 'qo':
                        QuestionOpen(question.get('ques'))
                    else:
                        raise TypeError(f'В файле {file_name} ошибка чтения типа фопроса {i}')
                return cls(data.get('name'), list_question)
        except FileNotFoundError:
            print(f"Файл {file_name}.json не найден.")
            return None

    @classmethod
    def get_list_anc(cls):
        directory = "./resources"
        list_dir = os.listdir(directory)
        d = {"countQuestionnaire": len(list_dir)}
        i = 0
        for dir in list_dir:
            filepath = os.path.join(directory, dir)
            with open(filepath, 'r') as file:
                data = json.load(file)
                d[f'Questionnaire{i}'] = {'name': data.get('name'), 'countQuestions': data.get('count')}
                i += 1
        return d

    def formAnc(self):
        d = {'name': self.name, 'count': len(self.questions)}
        for i in range(len(self.questions)):
            d[f'ques{i}'] = self.questions[i].toDict()
        return d

    @classmethod
    def load_questionnaire(cls, name: str):  # ?????????
        directory = "./resources"
        filepath = os.path.join(directory, name + '.json')

        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                # get
                return data
        except FileNotFoundError:
            print(f"Файл {name} не найден.")
            return None

    def addQuestion(self, question: Question):
        self.questions.append(question)
        self.change = True

    def delQuestion(self, idQ: int):
        del self.questions[idQ]
        self.change = True

    def saveQuestions(self):
        directory = "./"
        filename = self.name

        if filename[-5:] != '.json':
            filename += '.json'

        # Полное имя файла
        full_filename = os.path.join(directory, filename)

        # Проверяем, существует ли файл
        if (not (os.path.exists(full_filename))) or self.change:
            with open(full_filename, 'w') as f:
                json.dump(self.formAnc(), f)
                print(f"Data saved to: {full_filename}")
