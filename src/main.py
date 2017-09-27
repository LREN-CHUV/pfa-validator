"""
This program validates a PFA file according the MIP (Medical Informatics Platform) output
specification.

It reads configurations from environment variables:
    INPUT_METHOD: FILE (default) or POSTGRESQL

    (if the FILE input method is chosen)
    PFA_PATH: the path to the PFA file

    (if the POSTRESQL input method is chosen)
    DB_HOST: host of the PostgreSQL server, without port
    DB_PORT: port where the postgresql server is listening
    DB_NAME: name of the DB that contains the PFA file
    DB_USER: username to connect to the PostgreSQL database
    DB_PASSWORD: password to connect to the PostgreSQL database
    DB_TABLE: Table that contains the PFA file
    DB_COLUMN: Column that contains the PFA file
    DB_WHERE_LVALUE: Left part of the SQL where close to perform
    DB_WHERE_RVALUE: Right part of the SQL where close to perform
"""

import sys
import os
from FileJSONPFAValidator import FileJSONPFAValidator
from PostgreSQLJSONPFAValidator import PostgreSQLJSONPFAValidator
from utils import print_error, print_ok

# Instantiate a FileJSONPFAValidator or a PostgreSQLJSONPFAValidator depending which input method
# is requested by the user
INPUT_METHOD = os.getenv('INPUT_METHOD', 'FILE')

VALIDATOR = None

if INPUT_METHOD == 'FILE':
    PFA_PATH = os.environ.get('PFA_PATH')
    VALIDATOR = FileJSONPFAValidator(PFA_PATH)
    VALIDATOR.load_document()

elif INPUT_METHOD == 'POSTGRESQL':
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_TABLE = os.environ.get('DB_TABLE')
    DB_COLUMN = os.environ.get('DB_COLUMN')
    DB_WHERE_LVALUE = os.environ.get('DB_WHERE_LVALUE')
    DB_WHERE_RVALUE = os.environ.get('DB_WHERE_RVALUE')

    VALIDATOR = PostgreSQLJSONPFAValidator(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_TABLE, DB_COLUMN, DB_WHERE_LVALUE, DB_WHERE_RVALUE)
    VALIDATOR.load_document()

(VALID, REASON) = VALIDATOR.validate()

if not VALID:
    print_error(REASON)
    sys.exit(1)

print_ok("This is a valid PFA document!")
