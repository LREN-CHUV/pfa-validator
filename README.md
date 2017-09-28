# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct JSON
- Syntaxically correct PFA
- Semantically correct PFA

This project does not perform cross-validation on the PFA document.

## Usage

### Python usage

#### Validate a PFA file
1. [Install Titus](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python)
2. `PFA_PATH=data/example_01_valid/model.pfa python src/main.py`

#### Validate a PFA PostgreSQL column
1. [Install Titus](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python)
2. `INPUT_METHOD=POSTGRESQL DB_HOST=... DB_PORT=... DB_NAME=... DB_USER=... DB_PASSWORD=... DB_TABLE=... DB_COLUMN=... DB_WHERE_LVALUE=...DB_WHERE_RVALUE=... python src/main.py`

### Docker usage

#### Validate a PFA file
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --volume $(pwd)/data:/data --env INPUT_METHOD=POSTGRESQL DB_HOST=... DB_PORT=... DB_NAME=... DB_USER=... DB_PASSWORD=... DB_TABLE=... DB_COLUMN=... DB_WHERE_LVALUE=...DB_WHERE_RVALUE=... pfa-validator`

#### In a docker container
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --volume $(pwd)/data:/data --env PFA_PATH="/data/example_01_valid/model.pfa" pfa-validator`
