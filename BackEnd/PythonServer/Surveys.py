import Question
import json
import os
import sqlite3 as sq

from QuestionMultiAns import QuestionMultiAns
from QuestionOneAns import QuestionOneAns
from QuestionOpen import QuestionOpen


class Surveys:
    id: int
    questions: list[Question]
    name: str

    # def __new__(cls, *args, **kwargs):
    #     cls.id += 1
    #     return super().__new__(cls)

    def __init__(self, id, name: str = "NoName", questions: list[Question] = []):
        self.id = id
        self.name = name
        self.questions = questions

    @classmethod
    def create_instance(cls, id: int):
        with sq.connect("Surveys.db") as con:
            cur = con.cursor()

            cur.execute(f"""SELECT Q.QuestionID, Q.QuestionType, Q.QuestionText, Q.AnswerOptionsCount, Q.SurveyID, Q.QuestionNumberInSurvey, Q.ResponseCount
                                FROM Questions AS Q
                                WHERE Q.SurveyID = {id}
                                ORDER BY Q.QuestionNumberInSurvey;""")

            list_question = []
            for ques in cur:
                print(ques)
                cur_ans = con.cursor()

                cur_ans.execute(f"""SELECT q.QuestionText, a.AnswerText, a.AnswerOrder, a.SelectedCount
                                        FROM Questions q
                                        JOIN Answers a ON q.QuestionID = a.QuestionID
                                        WHERE q.SurveyID = {id} AND q.QuestionNumberInSurvey = {ques[5]}
                                        ORDER BY q.QuestionNumberInSurvey, a.AnswerOrder;""")

                list_ans = []
                for ans in cur_ans:
                    list_ans.append(ans[1])

                if ques[1] == 0:
                    list_question.append(QuestionOpen(ques[0], ques[2]))
                elif ques[1] == 1:
                    list_question.append(QuestionOneAns(ques[0], ques[2], list_ans))
                elif ques[1] == 2:
                    list_question.append(QuestionMultiAns(ques[0], ques[2], list_ans))

            name = cur.execute(f"""SELECT SurveyTitle
                                    FROM Surveys
                                    WHERE SurveyID = {id};""").fetchone()

            return cls(id, name[0], list_question)

    @classmethod
    def get_list_sur(cls):
        with sq.connect("Surveys.db") as con:
            cur = con.cursor()

            cur.execute("""SELECT COUNT(*) FROM Surveys;""")
            d = {"countSurveys": cur.fetchone()[0]}

            cur.execute("""SELECT SurveyID, SurveyTitle, NumberOfQuestions, CompletedCount FROM Surveys;""")
            i = 0
            for sur in cur:
                d[f'Surveys{i}'] = {"id": sur[0], "name": sur[1], "countQuestions": sur[2], "CompletedCount": sur[3]}
                i += 1
        return d

    def formAnc(self):
        d = {"id": self.id, "name": self.name, "count": len(self.questions)}
        for i in range(len(self.questions)):
            d[f"ques{i}"] = self.questions[i].toDict()
        return d

    @classmethod
    def load_questionnaire(cls, name: str):  # ?????????
        directory = "./resources"
        filepath = os.path.join(directory, name + ".json")

        try:
            with open(filepath, "r") as file:
                data = json.load(file)
                # get
                return data
        except FileNotFoundError:
            print(f"Файл {name} не найден.")
            return None

    def addQuestion(self, question: Question):
        self.questions.append(question)

    def delQuestion(self, idQ: int):
        del self.questions[idQ]

    @classmethod
    def setBD(cls):
        con = sq.connect("Surveys.db")
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Surveys (
SurveyID	INTEGER NOT NULL UNIQUE,
SurveyTitle	VARCHAR(255) NOT NULL,
NumberOfQuestions	INT NOT NULL,
CompletedCount	INT NOT NULL DEFAULT 0,
PRIMARY KEY(SurveyID AUTOINCREMENT))""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Questions (QuestionID	INTEGER NOT NULL UNIQUE,
QuestionType	TINYINT NOT NULL CHECK(QuestionType IN (0, 1, 2)),
QuestionText	TEXT NOT NULL,
AnswerOptionsCount	INT,
SurveyID	INT NOT NULL,
QuestionNumberInSurvey	INT NOT NULL,
ResponseCount	INT NOT NULL DEFAULT 0,
FOREIGN KEY(SurveyID) REFERENCES Surveys(SurveyID),
PRIMARY KEY(QuestionID AUTOINCREMENT))""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Answers (
AnswerID	INTEGER NOT NULL UNIQUE,
QuestionID	INT NOT NULL,
AnswerText	TEXT NOT NULL,
AnswerOrder	INT NOT NULL,
SelectedCount	INT NOT NULL DEFAULT 0,
FOREIGN KEY(QuestionID) REFERENCES Questions(QuestionID),
PRIMARY KEY(AnswerID AUTOINCREMENT))""")

        con.close()

    @classmethod
    def addBD(cls):
        con = sq.connect("Surveys.db")
        cur = con.cursor()

        cur.execute("""INSERT INTO Surveys (SurveyTitle, NumberOfQuestions, CompletedCount)
VALUES ('start', 4, 0)""")
        SurveysID = cur.lastrowid
        cur.execute(f"""INSERT INTO Questions (QuestionType, QuestionText, AnswerOptionsCount, SurveyID, QuestionNumberInSurvey, ResponseCount)
VALUES (2, 'Сколько ты зарабатываешь?', 5, {SurveysID}, 1, 0));""")
        con.commit()
        con.close()

    @classmethod
    def appDate(cls, data: dict):
        count = data["count"]

        with sq.connect("Surveys.db") as con:
            cur = con.cursor()

            cur.execute(f"""UPDATE Surveys SET CompletedCount = CompletedCount + 1 WHERE SurveyID = {data["id"]};""")

            for i in range(count):
                ques = data[f"ques{i}"]

                cur.execute(
                    f"""UPDATE Questions SET ResponseCount = ResponseCount + 1 WHERE QuestionID IN ({ques["idQues"]});""")

                for ans in ques["ans"]:
                    if ques["type"] == 'qoa' or ques["type"] == 'qma':

                        cur.execute(
                            f"""UPDATE Answers SET SelectedCount = SelectedCount + 1 WHERE AnswerOrder IN ({ans}) AND QuestionID IN ({ques["idQues"]});""")

                    elif ques["type"] == "qo":
                        ans = ans.lower()

                        cur.execute(
                            f"""SELECT AnswerID, AnswerText, AnswerOrder, SelectedCount, QuestionID FROM Answers WHERE AnswerText = '{ans}' AND QuestionID = {ques["idQues"]};""")

                        if cur.fetchone() == None:
                            print("Создаю")
                            cur.execute(
                                f"""INSERT INTO Answers (AnswerText, AnswerOrder, SelectedCount, QuestionID) VALUES ('{ans}', 1, 1, {ques["idQues"]});""")
                        else:
                            print("Обновляю")
                            cur.execute(
                                f"""UPDATE Answers SET SelectedCount = SelectedCount + 1 WHERE AnswerText IN ('{ans}') AND QuestionID IN ({ques["idQues"]});""")

            con.commit()
