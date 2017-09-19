# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct
- Provides consistent output

This project does not perform cross-validation on the PFA document

## Usage

### In python
1. `PFA_PATH=data/example_01_valid/model.pfa python main.py`

### In a docker container
1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --volume $(pwd)/data:/data --env PFA_PATH="/data/example_01_valid/model.pfa" pfa-validator`
