"""This file implements a subclass of a JSONPFAValidator that loads the PFA from a database.
It facilitates the use of the program by CI tools"""

import sys
import psycopg2
from psycopg2 import sql
from utils import print_error
from JSONPFAValidator import JSONPFAValidator

class PostgreSQLJSONPFAValidator(JSONPFAValidator):
    """A subclass of a JSONPFAValidator that loads the PFA from a database"""
    def __init__(self, db_host, db_port, db_name, db_user, db_password, db_table, db_column,
                 db_where_lvalue, db_where_rvalue):
        JSONPFAValidator.__init__(self, '')

        # Safety checks: don't do anything unless the user has provided minimal information to build
        # the query
        # Note that DB credentials are not checked, because psycopg2 will raise an exception if
        # wrong credentials were provided
        if db_table is None:
            print_error("Error: please provide the name of the table that contains the PFA file"
                        "using the DB_TABLE environment variable")
            sys.exit(1)

        if db_column is None:
            print_error("Error: please provide the name of the column that contains the PFA file"
                        "using the DB_COLUMN environment variable")
            sys.exit(1)

        if db_where_lvalue is None:
            print_error("Error: please provide an LVALUE for the WHERE clause of the query using "
                        "the DB_WHERE_LVALUE environment variable")
            sys.exit(1)

        if db_where_rvalue is None:
            print_error("Error: please provide an RVALUE for the WHERE clause of the query using "
                        "the DB_WHERE_RVALUE environment variable")
            sys.exit(1)

        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_table = db_table
        self.db_column = db_column
        self.db_where_lvalue = db_where_lvalue
        self.db_where_rvalue = db_where_rvalue


    def load_document(self):
        # We build the query using environment variables passed by the user. More specifically, the
        # table name, the column name and the WHERE clause can be passed as parameters.
        #
        # The traditional way to build such queries is to make a templated SQL string, and provide
        # the value of the templated variables at runtime.
        #
        # There is however an limitation with the psycopg2's templating system: it does allows to
        # template the right value of the *where clause*. However, it does not allow to template the
        # *column names* and *table name*.
        #
        # The reason why psycopg2 doesn't allow to provide dynamic table and column names is the
        # security concern of allowing the user to dynamically chose the column and table, which
        # would allow him to browse through any part of the database.
        #
        # In our case, we already trust the user to provide us with the database's credentials. As
        # such, he already has access to the database and the modularity we provide does not give
        # him more privileges than he already has. For this reason, we allow ourselves to bypass
        # psycopg2 limitation by using its raw SQL module.
        #
        # This leads to build a query in two steps:
        # 1. Build an SQL string that fills the *column names* and *table name* template variable
        #    using psycopg2's SQL module
        # 2. Build the rest of the string using psycopg2's standard templating mechanism

        # First templating step: fill the table and column names to the templated string
        sql_template = """
          SELECT {}
          FROM {}
          WHERE {} = %s
          LIMIT 1
        """
        prepared_statement = sql.SQL(sql_template).format(
            sql.Identifier(self.db_column),
            sql.Identifier(self.db_table),
            sql.Identifier(self.db_where_lvalue)
        )

        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            cur = conn.cursor()

            # Second templating step: fill the RVALUE of the where clause
            cur.execute(prepared_statement, (self.db_where_rvalue))
            result = cur.fetchone()
            print cur.query
            if result is None:
                print_error("The query parameters you provided did not return any result from the "
                            "database")
                sys.exit(1)

            json_string = result[0]
            if json_string is None:
                print_error("The query parameter you provided returned an empty column")
                sys.exit(1)

            self.json_string = json_string

        except psycopg2.Error as ex:
            print "Error while connecting to the database " + str(ex)
            sys.exit(1)
