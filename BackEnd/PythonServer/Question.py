import abc

import MyException


class Question(abc.ABC):
    _ques: str
    _id: int

    def __init__(self, id: int, ques: str) -> object:
        if ques.strip() == '':
            raise MyException.CreateQuestionException('Вопрос не может быть пустым')
        self._ques = ques.strip()
        self._id = id

    @abc.abstractmethod
    def toDict(self) -> dict:
        pass

    @abc.abstractmethod
    def add_in_db(self, SurveyID: int, QuestionNumberInSurvey: int) -> None:
        pass

    def get_id(self) -> int:
        return self._id

    @abc.abstractmethod
    def create_instance(cls, data: dict) -> object:
        pass
