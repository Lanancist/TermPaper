import Question
import MyException


class QuestionMultiAns(Question.Question):
    __type: str = "qma"
    __ans: list[str]

    def __init__(self, id: int, ques: str, ans: list[str] = []):
        super().__init__(id, ques)
        self.__ans = ans
        if len(self.__ans) == 0:
            raise MyException.CreateQuestionException("Колличество вопросов должно быть больше нуля")

    def toDict(self):
        return {"idQues": self.id, "type": self.__type, "ques": self.ques, "countAns": len(self.__ans),
                "ans": self.__ans}
