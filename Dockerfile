FROM python:2

WORKDIR /usr/src/app

RUN git clone https://github.com/opendatagroup/hadrian.git
RUN cd ./hadrian/titus && python setup.py install
RUN pip install psycopg2

COPY . .

CMD [ "python", "./src/main.py" ]
