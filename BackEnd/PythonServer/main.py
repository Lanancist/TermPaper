# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Surveys import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все заголовки
)


@app.get("/")
async def get_list_anc():
    return JSONResponse(Surveys.get_list_sur())


@app.get('/Surveys/{id}')
async def get_questionnaire_name(id: int):
    s = Surveys.create_instance_id(id)
    return JSONResponse(s.formAnc())


# @app.put("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     # Здесь вы можете обработать файл
#     return {"filename": file.filename}


@app.put("/answers")
async def post(data=Body()):
    Surveys.upDate(data)

    return {}


@app.put("/addSurveys")
async def post(data=Body()):
    s = Surveys.create_instance_json(data)
    s.add_surveys_in_db()

    return {}
