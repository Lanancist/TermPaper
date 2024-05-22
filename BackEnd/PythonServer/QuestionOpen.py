import MyException
import Question


class QuestionOpen(Question.Question):
    __type: str = "qo"

    def __init__(self, ques: str):
        super().__init__(ques)

    def toDict(self):
        return {"type": self.__type, "ques": self.ques}
