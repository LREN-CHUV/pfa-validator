# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct JSON
- Syntaxically correct PFA
- Semantically correct PFA

This project does not perform cross-validation on the PFA document.

## Usage
The program can be run as a **Python program** or as a **Docker container**.

It may fetch the PFA document to validate from the file system or from a PostgreSQL database.

- **When fetching the PFA document from the file system**, the program expects a `PFA_PATH` environment
variable that contains the path to the PFA document to validate.

- **When fetching the PFA document from a PostgreSQL database**, the program expects the following environment variables:
  * `INPUT_METHOD` that must be set to `POSTGRESQL`
  * the database's credentials: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASSWORD`
  * the parameters of the query to perform: `DB_TABLE` `DB_COLUMN` `DB_WHERE_LVALUE` `DB_WHERE_RVALUE`

### Python examples

#### Validate a PFA file
1. [Install Titus](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python)
2. `PFA_PATH=data/example_01_valid/model.pfa python src/main.py`

#### Validate a PFA PostgreSQL column
1. [Install Titus](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python)
2. `INPUT_METHOD=POSTGRESQL DB_HOST=172.20.0.2 DB_PORT=5432 DB_NAME=woken DB_USER=... DB_PASSWORD=... DB_TABLE=job_result DB_COLUMN=data DB_WHERE_LVALUE=job_id DB_WHERE_RVALUE=1 python src/main.py`

### Docker examples

#### Validate a PFA file
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --volume $(pwd)/data:/data --env PFA_PATH="/data/example_01_valid/model.pfa" pfa-validator`

#### Validate a PFA PostgreSQL column
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --volume $(pwd)/data:/data --env INPUT_METHOD=POSTGRESQL --env DB_HOST=172.20.0.2 --env DB_PORT=5432 --env DB_NAME=woken --env DB_USER=... --env DB_PASSWORD=... --env DB_TABLE=job_result --env DB_COLUMN=data --env DB_WHERE_LVALUE=job_id --env DB_WHERE_RVALUE=1 pfa-validator`
