FROM python:3.11.3

RUN mkdir /news_app

WORKDIR /news_app

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000