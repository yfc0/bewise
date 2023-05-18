from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from service import QuestionLoader, UserService, AudioLoader


app = FastAPI()


@app.get("/questions_num/{qty}")
async def questions(qty: int):
    r = await QuestionLoader(qty).last_record()
    await QuestionLoader(qty).load()
    return {"Предыдущий вопрос": r}


@app.post("/create_user/{username}")
async def create_user(username: str):
    user = UserService().create_user(username)
    return {"id": user.id, "token": user.token}


@app.post("/upload/{id}/{token}")
async def upload(file: UploadFile, id: int, token: str):
    user = UserService().check_credential(id, token)
    if not user:
        raise HTTPException(status_code=404, detail="have not user")
    audio = AudioLoader().load(file)
    return {"path": f"localhost:8000/download/{audio.id}"}


@app.get("/download/{id}/")
async def download(id: str):
    audio = AudioLoader().get_path_by_id(id)
    if not audio:
        raise HTTPException(status_code=404, detail="have not audio")
    return FileResponse(audio.path)
