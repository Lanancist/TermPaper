# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Questionnaire import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все заголовки
)


@app.get("/")
def get_list_anc():
    return Questionnaire.get_list_anc()


@app.get('/Questionnaire/{name}')
def get_questionnaire_name(name: str):
    return Questionnaire.load_questionnaire(name)
