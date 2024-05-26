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
def get_list_anc():
    return JSONResponse(Surveys.get_list_sur())


@app.get('/Surveys/{id}')
def get_questionnaire_name(id: int):
    s = Surveys.create_instance(id)
    return JSONResponse(s.formAnc())


@app.put("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Здесь вы можете обработать файл
    return {"filename": file.filename}


@app.put("/put")
async def post(data=Body()):
    name = data['name']
    # Здесь вы можете обработать файл
    print(name)

    return {}

# Surveys.setBD()
