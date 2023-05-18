import aiohttp
from fastapi import HTTPException

from db.models import Question, User, Audio
from db.db import new_session

from typing import Any, Optional
from sqlalchemy import desc

from pydub import AudioSegment

from utils import save_audio, audio_name


class QuestionLoader:
    def __init__(self, count: int):
        self.count = count


    base_url = "https://jservice.io/api/random?count="

    async def _request(self):
        url = self.base_url + str(self.count)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    return await r.json()
                else:
                    return HTTPException("api error")


    def _load(self, questions: list[dict[str, Any]]):
        with new_session() as session:
            for i in questions:
                q = Question(internal_id=i['id'], text=i['question'],\
                             answer=i['answer'])
                session.add(q)


    def questions_exist(self, questions: list[dict[str, Any]]) -> int:
        with new_session() as session:
            questions_idx = [question["id"] for question in questions]
            return session.query(Question).filter(Question.internal_id.in_(questions_idx)).count()


    async def load(self):
        while questions := await self._request():
            if self.questions_exist(questions) == 0:
                self._load(questions)
                break;
        return questions


    async def last_record(self):
        with new_session() as session:
            try:
                q = session.query(Question).order_by(desc(Question.created_at)).all()[-1]
            except Exception:
                return None
            return q.text


class UserService:
    def create_user(self, username):
        with new_session() as session:
            user = User(username=username)
            session.add(user)
            return user


    def check_credential(self, id: int, token: str) -> Optional[User]:
        with new_session() as session:
            user = session.query(User).filter_by(id=id, token=token).first()
            return user


class AudioLoader:
    path = "/usr/audio/"
    def _wav_to_mp3(self, file):
        audio = AudioSegment.from_wav(file).export(audio_name(file), format="mp3")
        return audio.name


    def get_path_by_id(self, id: str) -> Optional[Audio]:
        with new_session() as session:
            return session.query(Audio).get(id)


    def _load(self, path):
        with new_session() as session:
            audio = Audio(path=path)
            session.add(audio)
            return audio


    def load(self, file):
        audio = self._wav_to_mp3(save_audio(file))
        audio_path = self.path + audio
        return self._load(audio_path)
