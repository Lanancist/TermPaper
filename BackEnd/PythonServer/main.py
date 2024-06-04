# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from CustomThread import *
from Survey import *

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
    try:
        thread = CustomThread(target=Survey.setDB)
        # Surveys.setDB()
        # list_sur = Surveys.get_list_sur()
        thread.start()
        thread.join()

        thread = CustomThread(target=Survey.get_list_sur)

        thread.start()
        thread.join()
        list_sur = thread.local_result

        return JSONResponse(list_sur)
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка в базе данных")


@app.get('/Surveys/{id}')
def get_surveys_id(id: int):
    try:
        thread = CustomThread(target=Survey.create_instance_id, args=(id,))
        thread.start()
        thread.join()
        s = thread.local_result

        if s == None:
            raise MyException.CreateSurveyException(f"Анкеты c id: {id} не существует")

        thread = CustomThread(target=s.formAnc)
        thread.start()
        thread.join()

        return JSONResponse(thread.local_result)

    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="Item not found")


# @app.put("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     # Здесь вы можете обработать файл
#     return {"filename": file.filename}


@app.put("/answers")
def post(data=Body()):
    thread = CustomThread(target=Survey.upDate, args=(data,))
    thread.start()
    thread.join()

    thread = CustomThread(target=Survey.statistics_all, args=(data,))
    thread.start()
    thread.join()

    return JSONResponse(thread.local_result)


@app.post("/statistics/{id}")
def statistics_id(id: int):
    try:
        thread = CustomThread(target=Survey.create_instance_id, args=(id,))
        thread.start()
        thread.join()
        s = thread.local_result

        if s == None:
            raise MyException.CreateSurveyException(f"Анкеты c id: {id} не существует")

        thread = CustomThread(target=s.statistics)
        thread.start()
        thread.join()
        return JSONResponse(thread.local_result)

    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/statistics")
def statistics_top(top: int = 5):
    try:
        thread = CustomThread(target=Survey.statistics_top, args=(top,))
        thread.start()
        thread.join()

        return JSONResponse(thread.local_result)

    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/addSurveys")
def post(data=Body()):
    try:
        thread = CustomThread(target=Survey.create_instance_json, args=(data,))
        thread.start()
        thread.join()

        s = thread.local_result

        if s == None:
            raise MyException.CreateSurveyException(f"Ошибка формирования анкеты")

        thread = CustomThread(target=s.add_surveys_in_db)
        thread.start()
        thread.join()


    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="err")


@app.delete("/admin/Surveys/{id}")
def delete(id: int):
    thread = CustomThread(target=Survey.del_surv, args=(id,))
    thread.start()
    thread.join()
    return {}
