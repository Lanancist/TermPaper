import MyException
import Question
import sqlite3 as sq


class QuestionOpen(Question.Question):
    __type: str = "qo"

    def __init__(self, id: int, ques: str):
        super().__init__(id, ques)

    def create_instance(cls, data: dict):
        return cls(None, data["ques"])

    def toDict(self):
        return {"idQues": self._id, "type": self.__type, "ques": self._ques}

    def add_in_db(self, SurveyID: int, QuestionNumberInSurvey: int):
        with sq.connect("Surveys.db") as con:
            cur = con.cursor()

            cur.execute(f"""INSERT INTO Questions (QuestionType, QuestionText, AnswerOptionsCount, SurveyID, QuestionNumberInSurvey, ResponseCount)
            VALUES (0, '{self._ques}', NULL, {SurveyID}, {QuestionNumberInSurvey}, 0);""")

            if self._id == None:
                self._id = cur.lastrowid

            con.commit()
