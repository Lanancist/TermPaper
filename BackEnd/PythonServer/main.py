from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_hello():
    return "abo baba!"

@app.get("/listAnc")
def get_list_anc():
    return {"q": "aboba?", "ansCount": 3, "ans1":"abo", "ans2":"aboba", "ans3":"abobaba"}
