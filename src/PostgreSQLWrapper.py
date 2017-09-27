

""""This file is a DB wrapper for the main program. The wrapper connects to a PostgreSQL database
using the credentials passed as environment variables. It retrieves PFA files from the database and
passes them to the main program.

This wrapper is intended as a helper to CI tools that provide data through a PostgreSQL database"""

import os
import sys
import psycopg2
from psycopg2 import sql
from JSONPFAValidator import JSONPFAValidator

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_TABLE = os.environ.get('DB_TABLE')
DB_COLUMN = os.environ.get('DB_COLUMN')
DB_WHERE_LVALUE = os.environ.get('DB_WHERE_LVALUE')
DB_WHERE_RVALUE = os.environ.get('DB_WHERE_RVALUE')


# Safety checks: don't do anything unless the user has provided minimal information to build the
# query
# Note that DB credentials are not checked, because psycopg2 will raise an exception if wrong
# credentials were provided
if DB_TABLE is None:
    print ("Error: please provide the name of the table that contains the PFA file using the "
           "DB_TABLE environment variable")
    sys.exit(1)

if DB_COLUMN is None:
    print ("Error: please provide the name of the column that contains the PFA file using the "
           "DB_COLUMN environment variable")
    sys.exit(1)

if DB_WHERE_LVALUE is None:
    print ("Error: please provide an LVALUE for the WHERE clause of the query using the "
           "DB_WHERE_LVALUE environment variable")
    sys.exit(1)

if DB_WHERE_RVALUE is None:
    print ("Error: please provide an RVALUE for the WHERE clause of the query using the "
           "DB_WHERE_RVALUE environment variable")
    sys.exit(1)


# We build the query using environment variables passed by the user. More specifically, the table
# name, the column name and the WHERE clause can be passed as parameters.
#
# The traditional way to build such queries is to make a templated SQL string, and provide the
# value of the templated variables at runtime.
#
# There is however an limitation with the psycopg2's templating system: it does allows to template
# the right value of the *where clause*. However, it does not allow to template the *column names*
# and *table name*.
#
# The reason why psycopg2 doesn't allow to provide dynamic table and column names is the security
# concern of allowing the user to dynamically chose the column and table, which would allow him to
# browse through any part of the database.
#
# In our case, we already trust the user to provide us with the database's credentials. As such, he
# already has access to the database and the modularity we provide does not give him more privileges
# than he already has. For this reason, we allow ourselves to bypass psycopg2 limitation by using
# its raw SQL module.
#
# This leads to build a query in two steps:
# 1. Build an SQL string that fills the *column names* and *table name* template variable using
#    psycopg2's SQL module
# 2. Build the rest of the string using psycopg2's standard templating mechanism

# First templating step: fill the table and column names to the templated string
SQL_TEMPLATE = """
  SELECT {}
  FROM {}
  WHERE {} = %s
  LIMIT 1
"""
PREPARE_STATEMENT = sql.SQL(SQL_TEMPLATE).format(
    sql.Identifier(DB_COLUMN),
    sql.Identifier(DB_TABLE),
    sql.Identifier(DB_WHERE_LVALUE)
)

try:
    CONN = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    CUR = CONN.cursor()

    # Second templating step: fill the RVALUE of the where clause
    CUR.execute(PREPARE_STATEMENT, (DB_WHERE_RVALUE))
    RESULT = CUR.fetchone()
    if RESULT is None:
        print "The query parameters you provided did not return any result from the database"
        print CUR.query
        sys.exit(1)

    PFA = RESULT[0]
    if PFA is None:
        print "The query parameter you provided returned an empty column"
        sys.exit(1)

    VALIDATOR = JSONPFAValidator(PFA)
    (VALID, REASON) = VALIDATOR.validate()

    if not VALID:
        print "A PFA document was retrieved from the database but was not valid: " + REASON
        sys.exit(1)

except psycopg2.Error as ex:
    print "Error while connecting to the database " + str(ex)
    sys.exit(1)
