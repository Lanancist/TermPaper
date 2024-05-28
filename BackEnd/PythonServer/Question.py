import abc

import MyException


class Question(abc.ABC):
    ques: str
    id: int

    def __init__(self, id: int, ques: str):
        if ques == '':
            raise MyException.CreateQuestionException('Вопрос не может быть пустым')
        self.ques = ques
        self.id = id

    @abc.abstractmethod
    def toDict(self) -> dict:
        pass
