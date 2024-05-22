import abc

import MyException


class Question(abc.ABC):
    ques: str

    def __init__(self, ques: str):
        if ques == '':
            raise MyException.CreateQuestionException('Вопрос не может быть пустым')
        self.ques = ques

    @abc.abstractmethod
    def toDict(self) -> dict:
        pass
