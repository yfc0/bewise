FROM python:3.11

WORKDIR /usr/src/

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip3 install --upgrade -r /usr/src/requirements.txt


COPY ./src /usr/src/

RUN mkdir /usr/audio

RUN apt-get update && apt-get install -y ffmpeg

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
