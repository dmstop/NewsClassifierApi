FROM python:3.11.3

RUN mkdir /news_app

WORKDIR /news_app

COPY . .

RUN pip install -r requirements.txt

RUN curl -L -o src/predictor_model/roberta_predictor.pth "https://www.dropbox.com/scl/fi/mi68zsa4khqdyl3uc916e/roberta_predictor.pth?rlkey=8h1s4lnfxquui8ai94fvt6v4o&dl=1"

WORKDIR /news_app/src

CMD gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000