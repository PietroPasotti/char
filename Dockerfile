# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN ["chmod", "661", "./main.sh"]
CMD ["./main.sh"]

# docker run --env ENEMIES=127.0.0.1:8001 --env UVICORN_PORT=8000 --env NAME=ork -p 8000:8000 --expose 8000 --rm -d char
# docker run --env ENEMIES=127.0.0.1:8000 --env UVICORN_PORT=8001 --env NAME=elf -p 8001:8001 --expose 8001 --rm -d char
# stop&delete all:
#   docker stop $(docker ps -a -q); docker rm $(docker ps -a -q)
