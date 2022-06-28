from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from ner import get_entity
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# home


@app.get("/home")
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/submit")
async def submit(article: str = Form(...)):
    entity_list = get_entity(article)
    entity_dict = dict()
    entity_dict["record"] = []
    for i in range(len(entity_list)):
        temp_dict = {}
        temp_dict["sentence"] = entity_list[i][0]
        temp_dict["entitys"] = []
        for j in range(len(entity_list[i][1])):
            temp_dict2 = dict()
            temp_dict2["tag"] = entity_list[i][1][j][0]
            temp_dict2["entity"] = entity_list[i][1][j][1]
            temp_dict["entitys"].append(temp_dict2)
        entity_dict["record"].append(temp_dict)
    return entity_dict


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, host="127.0.0.1")
