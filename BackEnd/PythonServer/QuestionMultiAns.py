import Question
import MyException
import sqlite3 as sq


class QuestionMultiAns(Question.Question):
    __type: str = "qma"
    __ans: list[str]

    def __init__(self, id: int, ques: str, ans: list[str] = []) -> object:
        super().__init__(id, ques)
        self.__ans = ans
        if len(self.__ans) == 0:
            raise MyException.CreateQuestionException("Колличество ответов должно быть больше нуля")

    @classmethod
    def create_instance(cls, data: dict) -> object:
        return cls(None, data["ques"], data["ans"])

    def toDict(self) -> dict:
        return {"idQues": self._id, "type": self.__type, "ques": self._ques, "countAns": len(self.__ans),
                "ans": self.__ans}

    def add_in_db(self, SurveyID: int, QuestionNumberInSurvey: int) -> None:
        with sq.connect("Surveys.db") as con:
            cur = con.cursor()

            cur.execute(f"""INSERT INTO Questions (QuestionType, QuestionText, AnswerOptionsCount, SurveyID, QuestionNumberInSurvey, ResponseCount)
            VALUES (2, '{self._ques}', {len(self.__ans)}, {SurveyID}, {QuestionNumberInSurvey}, 0);""")

            if self._id == None:
                self._id = cur.lastrowid

            for i, ans in enumerate(self.__ans, 1):
                cur.execute(f"""INSERT INTO Answers (AnswerText, AnswerOrder, SelectedCount, QuestionID)
                VALUES ('{ans}', {i}, 0, {self._id});""")

            con.commit()
