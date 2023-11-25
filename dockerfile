FROM python:3.11

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ADD main.py /app
COPY artefacts /app/artefacts
COPY scripts /app/scripts

VOLUME ./video

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
