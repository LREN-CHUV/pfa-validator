[![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html) [![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/LREN-CHUV/pfa-validator/blob/master/LICENSE) [![DockerHub](https://img.shields.io/badge/docker-hbpmip%2Fpfa--validator-008bb8.svg)](https://hub.docker.com/r/hbpmip/pfa-validator/) [![ImageVersion](https://images.microbadger.com/badges/version/hbpmip/pfa-validator.svg)](https://hub.docker.com/r/hbpmip/pfa-validator/tags "hbpmip/pfa-validator image tags") [![ImageLayers](https://images.microbadger.com/badges/image/hbpmip/pfa-validator.svg)](https://microbadger.com/#/images/hbpmip/pfa-validator "hbpmip/pfa-validator on microbadger") [![Codacy Badge](https://api.codacy.com/project/badge/Grade/96b3483a2345429fb9fc4918fa7d205b)](https://www.codacy.com/app/hbp-mip/pfa-validator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=HBPMedical/pfa-validator&amp;utm_campaign=Badge_Grade) [![CircleCI](https://circleci.com/gh/HBPMedical/pfa-validator.svg?style=svg)](https://circleci.com/gh/HBPMedical/pfa-validator)

# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct JSON
- Syntaxically correct PFA
- Semantically correct PFA

This project does not perform cross-validation on the PFA document.

## Usage
The program can be run as a **Python program** or as a **Docker container**.

It may fetch the PFA document to validate from the file system or from a PostgreSQL database.

* **When fetching the PFA document from the file system**, the program expects a `PFA_PATH` environment
variable that contains the path to the PFA document to validate.

* **When fetching the PFA document from a PostgreSQL database**, the program expects the following environment variables:
  * `INPUT_METHOD` that must be set to `POSTGRESQL`
  * the database's credentials: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASSWORD`
  * the parameters of the query to perform: `DB_TABLE` `DB_COLUMN`
  * the job ID (used to check the job_id column and get the right PFA document): `JOB_ID`

In addition, the program will also need the following environment variables to be set up in order to get some
validation data: `FEATURES_DB_HOST`, `FEATURES_DB_PORT`, `FEATURES_DB_NAME`, `FEATURES_DB_USER`, `FEATURES_DB_PASSWORD`
and `FEATURES_DB_TABLE`

### Examples

#### Validate a PFA file
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image:

```sh
    docker run --volume $(pwd)/data:/data \
    --env PFA_PATH="/data/example_01_valid/model.pfa" \
    --env FEATURES_DB_HOST=db \
    --env FEATURES_DB_PORT=5432 \
    --env FEATURES_DB_NAME=sample \
    --env FEATURES_DB_USER=sample \
    --env FEATURES_DB_PASSWORD=... \
    --env FEATURES_DB_TABLE=features \
    hbpmip/pfa-validator:0.10.1-1
```

#### Validate a PFA PostgreSQL column
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image:

```sh
  docker run \
    --env INPUT_METHOD=POSTGRESQL \
    --env JOB_ID=1
    --env DB_HOST=172.20.0.2 \
    --env DB_PORT=5432 \
    --env DB_NAME=woken \
    --env DB_USER=woken \
    --env DB_PASSWORD=... \
    --env DB_TABLE=job_result \
    --env DB_COLUMN=data \
    --env FEATURES_DB_HOST=db \
    --env FEATURES_DB_PORT=5432 \
    --env FEATURES_DB_NAME=sample \
    --env FEATURES_DB_USER=sample \
    --env FEATURES_DB_PASSWORD=... \
    --env FEATURES_DB_TABLE=features \
    hbpmip/pfa-validator:0.10.1-1
```

NOTE: If you don't want to use Docker, you can install the dependencies with: `pip install -r requirements.txt`
and run this program using Python2. The environment variables still have to be set up.

## TODO

* Allow validation of YAML formatted PFA document

# Acknowledgements

This work has been funded by the European Union Seventh Framework Program (FP7/2007­2013) under grant agreement no. 604102 (HBP)

This work is part of SP8 of the Human Brain Project (SGA1).

