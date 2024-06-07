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


# Метод обработки запроса на главную страницу
@app.get("/")
def get_list_anc():
    try:
        thread = CustomThread(target=Survey.setDB)  # Инициализация базы данных
        # Surveys.setDB()
        # list_sur = Surveys.get_list_sur()
        thread.start()
        thread.join()

        thread = CustomThread(target=Survey.get_list_sur)  # Запрос списка анкет

        thread.start()
        thread.join()
        list_sur = thread.get_res()

        return JSONResponse(list_sur)
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка в базе данных")


# Обработка запроса на получение анкеты с заданным id
@app.get('/Surveys/{id}')
def get_surveys_id(id: int):
    try:
        thread = CustomThread(target=Survey.create_instance_id, args=(id,))  # Создание обьекта по id
        thread.start()
        thread.join()
        s = thread.get_res()

        if s == None:
            raise MyException.CreateSurveyException(f"Анкеты c id: {id} не существует")

        thread = CustomThread(target=s.formAnc)  # формирование словаря для сериализации данных
        thread.start()
        thread.join()

        return JSONResponse(thread.get_res())

    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="Item not found")


# обработка отвеетов пользователя и возвращение статистики
@app.put("/answers")
def post(data=Body()):
    thread = CustomThread(target=Survey.upDate, args=(data,))  # запись в базу данных результата анкеты
    thread.start()
    thread.join()

    thread = CustomThread(target=Survey.statistics_all, args=(data,))  # возвращение статистики по решенной анкете
    thread.start()
    thread.join()

    return JSONResponse(thread.get_res())


# запрос статистики для анкеты с заданным id
@app.put("/statistics/{id}")
def statistics_id(id: int):
    try:
        thread = CustomThread(target=Survey.create_instance_id, args=(id,))  # Конструктор анкеты по id
        thread.start()
        thread.join()
        s = thread.get_res()

        if s == None:
            raise MyException.CreateSurveyException(f"Анкеты c id: {id} не существует")

        thread = CustomThread(target=s.statistics)  # Формирование статистики для обьекта анкета
        thread.start()
        thread.join()
        return JSONResponse(thread.get_res())

    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="Item not found")


# самые популярные анкеты
@app.post("/statistics")
def statistics_top(top: int = 5):
    try:
        thread = CustomThread(target=Survey.statistics_top, args=(top,))  # формирование списка
        thread.start()
        thread.join()

        return JSONResponse(thread.get_res())

    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="Item not found")


# Добавление новой анкеты
@app.post("/addSurveys")
def post(data=Body()):
    try:
        thread = CustomThread(target=Survey.create_instance_json,
                              args=(data,))  # конструктор класса анкета по анкете в формате json
        thread.start()
        thread.join()

        s = thread.get_res()

        if s == None:
            raise MyException.CreateSurveyException(f"Ошибка формирования анкеты")

        thread = CustomThread(target=s.add_surveys_in_db)  # Добавление обьекта анкеты в базу данных
        thread.start()
        thread.join()


    except MyException.CreateSurveyException:
        raise HTTPException(status_code=404, detail="err")


# Запрос на удаление анкеты
@app.delete("/admin/Surveys/{id}")
def delete(id: int):
    thread = CustomThread(target=Survey.del_surv, args=(id,))
    thread.start()
    thread.join()
    return {}
