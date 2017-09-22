# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct JSON
- Syntaxically correct PFA
- Semantically correct PFA

This project does not perform cross-validation on the PFA document.

## Usage
[Install Titus](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python),
Define a `PFA_PATH` environment variable that contains the path to the file to validate and run
the `src/main.py` python script.

## Examples
### In python
1. [Install Titus](https://github.com/opendatagroup/hadrian/wiki/Installation#case-4-you-want-to-install-titus-in-python)
2. `PFA_PATH=data/example_01_valid/model.pfa python src/main.py`

### In a docker container
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --volume $(pwd)/data:/data --env PFA_PATH="/data/example_01_valid/model.pfa" pfa-validator`
