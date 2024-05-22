import MyException
import Question


class QuestionOneAns(Question.Question):
    __type: str = "qoa"
    __ans: list[str]

    def __init__(self, ques: str, ans: list[str] = []):
        super().__init__(ques)
        self.__ans = ans
        if len(self.__ans) == 0:
            raise MyException.CreateQuestionException("Колличество вопросов должно быть больше нуля")

    def toDict(self):
        return {"type": self.__type, "ques": self.ques, "countAns": len(self.__ans), "ans": self.__ans}
