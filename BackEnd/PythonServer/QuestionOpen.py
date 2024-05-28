import MyException
import Question


class QuestionOpen(Question.Question):
    __type: str = "qo"

    def __init__(self, id: int, ques: str):
        super().__init__(id, ques)

    def toDict(self):
        return {"idQues": self.id, "type": self.__type, "ques": self.ques}
