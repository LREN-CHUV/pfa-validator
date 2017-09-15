# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct
- Provides consistent output

This project does not perform cross-validation on the PFA document

## Usage

### In python
1. `PFA_PATH=path_to_pfa.json python main.py`

### In a docker container
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --name pfa-validator-1 -e PFA_PATH="path_to_pfa.json" pfa-validator`
