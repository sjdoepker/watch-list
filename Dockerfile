# syntax=docker/dockerfile:1

FROM python:3.11-slim

EXPOSE 5000/tcp

WORKDIR /watchlist-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m", "flask", "--app", "flaskenv/app.py", "run" ]