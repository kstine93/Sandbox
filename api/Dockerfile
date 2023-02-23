#syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /app

COPY ./requirements.txt ./deletion_app.cfg ./databaseConnection.py ./validation.py /app/

RUN pip install -r requirements.txt

COPY . .

#Port exposure
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host" , "0.0.0.0", "--port", "8080"]