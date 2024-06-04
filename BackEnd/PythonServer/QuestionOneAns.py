import MyException
import Question
import sqlite3 as sq


class QuestionOneAns(Question.Question):
    __type: str = "qoa"
    __ans: list[str]

    def __init__(self, id: int, ques: str, ans: list[str] = []):
        super().__init__(id, ques)
        self.__ans = ans
        if len(self.__ans) == 0:
            raise MyException.CreateQuestionException("Колличество ответов должно быть больше нуля")

    def create_instance(cls, data: dict):
        return cls(None, data["ques"], data["ans"])

    def toDict(self):
        return {"idQues": self._id, "type": self.__type, "ques": self._ques, "countAns": len(self.__ans),
                "ans": self.__ans}

    def add_in_db(self, SurveyID: int, QuestionNumberInSurvey: int):
        with sq.connect("Surveys.db") as con:
            cur = con.cursor()

            cur.execute(f"""INSERT INTO Questions (QuestionType, QuestionText, AnswerOptionsCount, SurveyID, QuestionNumberInSurvey, ResponseCount)
            VALUES (1, '{self.ques}', {len(self.__ans)}, {SurveyID}, {QuestionNumberInSurvey}, 0);""")

            if self.id == None:
                self.id = cur.lastrowid

            for i, ans in enumerate(self.__ans, 1):
                cur.execute(f"""INSERT INTO Answers (AnswerText, AnswerOrder, SelectedCount, QuestionID)
                VALUES ('{ans}', {i}, 0, {self.id});""")

            con.commit()
