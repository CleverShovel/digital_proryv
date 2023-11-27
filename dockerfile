FROM python:3.11

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get -y install libgl1 &&\
    pip install --no-cache-dir -r requirements.txt

ADD main.py /app
COPY artefacts /artefacts
COPY scripts /app/scripts

VOLUME  /app/data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
