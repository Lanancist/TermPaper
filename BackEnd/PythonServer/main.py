from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import Questionnaire
import QuestionMultiAns  # DELETE!!!
import QuestionOneAns
import QuestionOpen

# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Разрешить все источники
#     allow_credentials=True,
#     allow_methods=["*"],  # Разрешить все HTTP методы
#     allow_headers=["*"],  # Разрешить все заголовки
# )
#
#
# @app.get("/mi")
# def get_hello():
#     return "abo baba!"
#
#
# @app.get("/listQuestionnaire")
# def get_list_anc():
#     return {"q": "aboba?", "ansCount": 3, "ans1": "abo", "ans2": "aboba", "ans3": "abobaba"}
#

arr = []
arr.append(
    QuestionMultiAns.QuestionMultiAns("Сколько ты зарабатываешь?", ["1-10", "10-100", "100-500", "500-1000", "<10000"]))
arr.append(QuestionOneAns.QuestionOneAns('Отвечай!', ['aboba?']))
arr.append(
    QuestionMultiAns.QuestionMultiAns("а теперь сколько ты зарабатываешь?",
                                      ["3-30", "50-500", "600-800", "900-2000", "<17654"]))
arr.append(QuestionOpen.QuestionOpen('Ты мне рааскажешь?'))

q = Questionnaire.Questionnaire("startAnc", arr)

print(q.formAnc())

q.saveQuestions()

q.saveQuestions()

q = Questionnaire.Questionnaire.create_instance(1)

print(q)
print(arr)
print(q.formAnc())
