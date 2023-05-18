from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

import uuid

import datetime

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    internal_id = Column(Integer, unique=True)
    text = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    token = Column(UUID(as_uuid=True), default=uuid.uuid4)


class Audio(Base):
    __tablename__ = "audio"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = Column(String, nullable=False)
