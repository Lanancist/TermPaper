import threading

import MyException
import Question
import sqlite3 as sq

from QuestionMultiAns import QuestionMultiAns
from QuestionOneAns import QuestionOneAns
from QuestionOpen import QuestionOpen


class Survey:
    _id: int
    _questions: list[Question]
    _name: str

    def __init__(self, id, name: str = "NoName",
                 questions: list[Question] = []) -> object:  # Конструктор из списка вопросов
        self._id = id
        self._name = name
        if len(questions) == 0:
            raise MyException.CreateSurveyException("Анкета не может быть пустой")
        self._questions = questions

    @classmethod
    def create_instance_id(cls, id: int) -> object:  # Конструктор из базы данных по id
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                cur = con.cursor()

                name = cur.execute(f"""SELECT SurveyTitle
                                            FROM Surveys
                                            WHERE SurveyID = {id};""").fetchone()

                if name == None:
                    raise MyException.CreateSurveyException(f"Анкеты c id: {id} не существует")

                cur.execute(f"""SELECT Q.QuestionID, Q.QuestionType, Q.QuestionText, Q.AnswerOptionsCount, Q.SurveyID, Q.QuestionNumberInSurvey, Q.ResponseCount
                                        FROM Questions AS Q
                                        WHERE Q.SurveyID = {id}
                                        ORDER BY Q.QuestionNumberInSurvey;""")

                list_question = []
                for ques in cur:
                    cur_ans = con.cursor()

                    cur_ans.execute(f"""SELECT q.QuestionText, a.AnswerText, a.AnswerOrder, a.SelectedCount
                                                FROM Questions q
                                                JOIN Answers a ON q.QuestionID = a.QuestionID
                                                WHERE q.SurveyID = {id} AND q.QuestionNumberInSurvey = {ques[5]}
                                                ORDER BY q.QuestionNumberInSurvey, a.AnswerOrder;""")

                    # if cur_ans.fetchall() == []:
                    #     raise MyException.CreateSurveysException("Анкета в базе не содержит ответов")
                    # print(cur_ans.fetchall())
                    list_ans = []
                    for ans in cur_ans:
                        list_ans.append(ans[1])

                    if ques[1] == 0:
                        list_question.append(QuestionOpen(ques[0], ques[2]))
                    elif ques[1] == 1:
                        list_question.append(QuestionOneAns(ques[0], ques[2], list_ans))
                    elif ques[1] == 2:
                        list_question.append(QuestionMultiAns(ques[0], ques[2], list_ans))

                return cls(id, name[0], list_question)

    @classmethod
    def create_instance_json(cls, data: dict) -> object:  # Конструктор из json файла
        list_question = []
        for i in range(data["count"]):
            if data["questions"][i]["type"] == "qo":
                list_question.append(QuestionOpen(None, data["questions"][i]["ques"]))
            elif data["questions"][i]["type"] == "qoa":
                list_question.append(QuestionOneAns(None, data["questions"][i]["ques"], data["questions"][i]["ans"]))
            elif data["questions"][i]["type"] == "qma":
                list_question.append(QuestionMultiAns(None, data["questions"][i]["ques"], data["questions"][i]["ans"]))
        return cls(None, data["name"], list_question)

    @classmethod
    def get_list_sur(cls) -> dict:  # Функция запроса в всех анкет из базы данных
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                cur = con.cursor()

                cur.execute("""SELECT COUNT(*) FROM Surveys;""")

                count = cur.fetchone()[0]

                cur.execute("""SELECT SurveyID, SurveyTitle, NumberOfQuestions, CompletedCount FROM Surveys;""")

                list_surveys = []
                for sur in cur:
                    list_surveys.append(
                        {"id": sur[0], "name": sur[1], "countQuestions": sur[2], "CompletedCount": sur[3]})

                d = {"countSurveys": count, "surveys": list_surveys}

            return d

    def formAnc(self) -> dict:  # преобразование обьекта в json
        list_ques = []
        for i in range(len(self._questions)):
            list_ques.append(self._questions[i].toDict())
        d = {"id": self._id, "name": self._name, "count": len(self._questions), "questions": list_ques}
        return d

    @classmethod
    def setDB(cls) -> None:  # инициализация базы данных
        db_lock = threading.Lock()
        with db_lock:
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

    def add_surveys_in_db(self) -> None:  # добавление экземпляра класса в базу данных
        # print("Запуск")
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                cur = con.cursor()

                cur.execute(f"""INSERT INTO Surveys (SurveyTitle, NumberOfQuestions, CompletedCount)
                                VALUES ('{self._name}', {len(self._questions)}, 0)""")

                SurveysID = cur.lastrowid

                if self._id == None:
                    self._id = SurveysID

                con.commit()

                for index, ques in enumerate(self._questions, 1):
                    ques.add_in_db(SurveysID, index)

                con.commit()

    @classmethod
    def upDate(cls, data: dict) -> None:  # Обновление базы данных, запись результатов анкетирования
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                cur = con.cursor()

                cur.execute(
                    f"""UPDATE Surveys SET CompletedCount = CompletedCount + 1 WHERE SurveyID = {data["id"]};""")

                for ques in data["questions"]:

                    if ques.get("ans") == None or ques.get("ans") == []:
                        # print('sssssssssssssss')
                        con.commit()
                        continue

                    cur.execute(
                        f"""UPDATE Questions SET ResponseCount = ResponseCount + 1 WHERE QuestionID IN ({ques["idQues"]});""")

                    for ans in ques["ans"]:
                        if ques["type"] == 'qoa':
                            cur.execute(
                                f"""UPDATE Answers SET SelectedCount = SelectedCount + 1 WHERE AnswerText IN ('{ques["ans"][-1]}') AND QuestionID IN ({ques["idQues"]});""")
                            break
                        if ques["type"] == 'qma':

                            cur.execute(
                                f"""UPDATE Answers SET SelectedCount = SelectedCount + 1 WHERE AnswerText IN ('{ans}') AND QuestionID IN ({ques["idQues"]});""")

                        elif ques["type"] == "qo":
                            ans = ans.lower()

                            cur.execute(
                                f"""SELECT AnswerID, AnswerText, AnswerOrder, SelectedCount, QuestionID FROM Answers WHERE AnswerText = '{ans}' AND QuestionID = {ques["idQues"]};""")

                            if cur.fetchone() == None:
                                # print("Создаю")
                                cur.execute(
                                    f"""INSERT INTO Answers (AnswerText, AnswerOrder, SelectedCount, QuestionID) VALUES ('{ans}', 1, 1, {ques["idQues"]});""")
                            else:
                                # print("Обновляю")
                                cur.execute(
                                    f"""UPDATE Answers SET SelectedCount = SelectedCount + 1 WHERE AnswerText IN ('{ans}') AND QuestionID IN ({ques["idQues"]});""")

                con.commit()

    @classmethod
    def del_surv(cls, id: int) -> None:  # удаление анкеты
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                cur = con.cursor()

                cur.execute(f"""SELECT COUNT(*) FROM Surveys WHERE SurveyID = {id};""")

                if cur.fetchone() == (0,):
                    # print('aboba!!!!!!!!!!!!!')
                    pass

                else:
                    cur.executescript(f"""BEGIN TRANSACTION; DELETE FROM Answers WHERE QuestionID IN (
                    SELECT QuestionID FROM Questions WHERE SurveyID ={id});DELETE FROM Questions WHERE SurveyID = {id};
                    DELETE FROM Surveys WHERE SurveyID = {id}; COMMIT;""")

    @classmethod
    def statistics_all(cls, data: dict) -> dict:  # Подсчет статистических данных из словоря
        # print("qwertyuiop")
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                d = {"id": data["id"], "name": data["name"], "count": data["count"]}
                cur = con.cursor()
                questions = []

                for ques in data["questions"]:
                    statistics_list = []

                    if ques.get("type") == "qo":
                        ques["ans"] = statistics_list
                        questions.append(ques)
                        continue

                    cur.execute(
                        f"""SELECT ResponseCount FROM Questions WHERE QuestionID = {ques["idQues"]};""")

                    ResponseCount = cur.fetchone()[0]

                    cur.execute(f"""SELECT AnswerText, SelectedCount FROM Answers 
                            WHERE QuestionID = {ques["idQues"]} ORDER BY AnswerOrder;""")

                    for ans in cur:
                        if ResponseCount == 0:
                            raise MyException.CreateQuestionException("Ошибка обработки ResponseCount")  # Ошибка
                        else:
                            statistics_list.append({f"{ans[0]}": round((ans[1] / ResponseCount) * 100, 2)})

                    ques["ans"] = statistics_list
                    questions.append(ques)

                d["questions"] = questions

            return d

    def statistics(self) -> dict:  # подсчет статистики по id
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                d = {"id": self._id, "name": self._name, "count": len(self._questions)}
                cur = con.cursor()
                questions = []

                for ques in self._questions:
                    statistics_list = []

                    cur.execute(
                        f"""SELECT ResponseCount FROM Questions WHERE QuestionID = {ques.get_id()};""")

                    ResponseCount = cur.fetchone()[0]

                    cur.execute(f"""SELECT AnswerText, SelectedCount FROM Answers 
                            WHERE QuestionID = {ques.get_id()} ORDER BY AnswerOrder;""")

                    for ans in cur:
                        if ResponseCount == 0:
                            statistics_list.append({f"{ans[0]}": round((ans[1] / 1) * 100, 2)})
                        else:
                            statistics_list.append({f"{ans[0]}": round((ans[1] / ResponseCount) * 100, 2)})

                    ques_dict = ques.toDict()
                    ques_dict["statistics"] = statistics_list
                    questions.append(ques_dict)

                d["questions"] = questions
            return d

    @classmethod
    def statistics_top(cls, top: int):  # формирование спискасамых популярных анкет
        if top <= 0:
            raise MyException.CreateSurveyException
        db_lock = threading.Lock()
        with db_lock:
            with sq.connect("Surveys.db") as con:
                d = {"count": top}
                cur = con.cursor()

                cur.execute(f"""SELECT SurveyID, SurveyTitle, NumberOfQuestions, CompletedCount
                            FROM Surveys
                            ORDER BY CompletedCount DESC
                            LIMIT {top};""")
                list_sur = []
                for sur in cur:
                    list_sur.append({"id": sur[0], "name": sur[1], "countQues": sur[2], "completedCount": sur[3]})

                d["survey"] = list_sur

                return d
