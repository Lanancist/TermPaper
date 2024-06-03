# uvicorn main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import MyException
from CustomThread import *
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
    try:
        thread = CustomThread(target=Surveys.setDB)
        # Surveys.setDB()
        # list_sur = Surveys.get_list_sur()
        thread.start()
        thread.join()

        thread = CustomThread(target=Surveys.get_list_sur)

        thread.start()
        thread.join()
        list_sur = thread.local_result

        return JSONResponse(list_sur)
    except Exception:
        return {"status": 500, "data": "Ошибка базы данных"}


@app.get('/Surveys/{id}')
def get_questionnaire_name(id: int):
    thread = CustomThread(target=Surveys.create_instance_id, args=(id,))
    thread.start()
    thread.join()
    s = thread.local_result

    thread = CustomThread(target=s.formAnc)
    thread.start()
    thread.join()
    #
    # print(thread.local_result)

    # s = Surveys.create_instance_id(id)
    return JSONResponse(thread.local_result)
    # return JSONResponse(s.formAnc())
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # return {"status": 404, "data": e}


# @app.put("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     # Здесь вы можете обработать файл
#     return {"filename": file.filename}


@app.put("/answers")
def post(data=Body()):
    thread = CustomThread(target=Surveys.upDate, args=(data,))
    thread.start()
    thread.join()

    thread = CustomThread(target=Surveys.statistics1, args=(data,))
    thread.start()
    thread.join()

    # Surveys.upDate(data)

    return JSONResponse(thread.local_result)


@app.put("/statistics/{id}")
def statistics_id(id: int):
    thread = CustomThread(target=Surveys.create_instance_id, args=(id,))
    thread.start()
    thread.join()
    s = thread.local_result
    # s = Surveys.create_instance_id(id)
    thread = CustomThread(target=s.statistics)
    thread.start()
    thread.join()
    return JSONResponse(thread.local_result)


@app.post("/addSurveys")
def post(data=Body()):
    try:
        thread = CustomThread(target=Surveys.create_instance_json, args=(data,))
        thread.start()
        thread.join()

        s = thread.local_result

        thread = CustomThread(target=s.add_surveys_in_db)
        thread.start()
        thread.join()

        # s = Surveys.create_instance_json(data)
        # s.add_surveys_in_db()

        return JSONResponse({"?": True})
    except Exception:
        print("ATATATATATATATATA!!!!!!!!!!!!!!!!!!")
        return JSONResponse({"?": False})


@app.delete("/admin/Surveys/{id}")
def delete(id: int):
    thread = CustomThread(target=Surveys.del_surv, args=(id,))
    thread.start()
    thread.join()
    # Surveys.del_surv(id)
    return {}
