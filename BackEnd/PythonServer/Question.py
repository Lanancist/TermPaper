import abc

import MyException


class Question(abc.ABC):
    _ques: str
    _id: int

    def __init__(self, id: int, ques: str):
        if ques == '':
            raise MyException.CreateQuestionException('Вопрос не может быть пустым')
        self._ques = ques
        self._id = id

    @abc.abstractmethod
    def toDict(self) -> dict:
        pass

    @abc.abstractmethod
    def add_in_db(self, SurveyID: int, QuestionNumberInSurvey: int):
        pass

    def get_id(self):
        return self.id
