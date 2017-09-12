# pfa-validator

A small python program that validates that a PFA document is:
- Syntaxically correct
- Provides consistent output

This project does not perform cross validation the PFA document

## Usage

1. Build the image: `docker build -t pfa-validator .`
2. Run a container based on that image: `docker run --name pfa-validator-1 pfa-validator`
