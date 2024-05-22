import Question
from functools import singledispatchmethod
import json
import os

from QuestionMultiAns import QuestionMultiAns


# from QuestionOneAns import QuestionOneAns
# from QuestionOpen import QuestionOpen


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
    def create_instance(cls, id: int):
        directory = "./resources"
        filepath = os.path.join(directory, str(id) + '.json')
        print(os.listdir(directory))
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                list_question: list[Question] = []
                for i in range(data.get('count')):
                    question = data.get(f'ques{i}')
                    question_type = question.get('type')
                    if question_type == 'qma':
                        list_question.append(
                            QuestionMultiAns(question.get('ques'), question.get('ans')))
                    elif question_type == 'qoa':
                        pass
                    elif question_type == 'qo':
                        pass
                    else:
                        raise TypeError(f'В файле с id = {id} ошибка чтения типа фопроса {i}')
                return cls(data.get('name'), list_question)
        except FileNotFoundError:
            print(f"Файл {id}.json не найден.")
            return None

    # @__init__.register(Question)
    # def __init__(self, id: int):
    #     with open(f'q{id}', 'r') as f:
    #         dat = json.load(f)
    #         print(dat)

    def formAnc(self):
        d = {'name': self.name, 'count': len(self.questions)}
        for i in range(len(self.questions)):
            d[f'ques{i}'] = self.questions[i].toDict()
        return d

    def load_and_init(self, id: int):
        directory = "./resources"
        filepath = os.path.join(directory, str(id))

        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                # get
                return data
        except FileNotFoundError:
            print(f"Файл {id} не найден.")
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
