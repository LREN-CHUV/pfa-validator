FROM python:2

MAINTAINER mirco.nasuti@chuv.ch

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENV JOB_ID=1
ENV DB_HOST=db \
    DB_PORT=5432 \
    DB_NAME=woken \
    DB_USER=woken \
    DB_PASSWORD=... \
    DB_TABLE=job_result

CMD [ "python", "./insert_fake_data.py" ]
