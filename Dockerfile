FROM python:2

MAINTAINER ludovic.claude@chuv.ch

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

WORKDIR /usr/src/app

RUN pip install psycopg2 titus==0.8.4

COPY . .

CMD [ "python", "./src/main.py" ]

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="hbpmip/pfa-validator" \
      org.label-schema.description="Validates PFA documents" \
      org.label-schema.url="https://github.com/HBPMedical/pfa-validator" \
      org.label-schema.vcs-type="git" \
      org.label-schema.vcs-url="https://github.com/HBPMedical/pfa-validator" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version="$VERSION" \
      org.label-schema.vendor="LREN CHUV" \
      org.label-schema.license="Apache2.0" \
      org.label-schema.docker.dockerfile="Dockerfile" \
      org.label-schema.schema-version="1.0"
