FROM python:2

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./main.py" ]