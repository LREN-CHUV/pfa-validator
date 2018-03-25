"""This file describes the implementation of the JSONPFAValidator class, which contains the main
logic of the program"""

import json
from psycopg2 import connect
from psycopg2 import sql
from pandas import read_sql
from titus.genpy import PFAEngine
from titus.datatype import AvroRecord
from titus.errors import *


class JSONPFAValidator(object):
    """The JSONPFAValidator contains the main logic of the program. It provides a function
    `validate` that validates a JSON PFA file, by checking its JSON syntax, its PFA syntax, its PFA
    semantics and that it uses the PFA `map` method, which is required by the MIP"""

    def __init__(self, json_string=''):
        self.json_string = json_string
        self.engine = None

    def load_document(self):
        """Load the document. This method does nothing when a JSONPFAValidator object is
        instantiated, but may be extended by subclasses so it should always be called before
        validate()"""
        pass

    def get_engine(self):
        """Creates a PFA engine based on the json_string provided as constructor class. If an
        engine was already created, this method does nothing"""
        if not self.engine:
            # pylint: disable=unbalanced-tuple-unpacking
            engine, = PFAEngine.fromJson(json.loads(self.json_string))
            self.engine = engine

        return self.engine

    def validate(self):
        """A function that validates a PFA described as a string
        Returns a 2-uple. The first element is boolean that is True or False if JSON string
        represents a valid PFA file. The second is a string explaining the reason if the PFA file is
        not valid"""

        # Check that a PFA engine can be correctly instantiated
        try:
            engine = self.get_engine()
        except ValueError as ex:
            # JSON validation
            return False, "The file provided does not contain a valid JSON document: " + str(ex)
        except PFASyntaxException as ex:
            # Syntax validation
            return False, "The file provided does not contain a valid PFA compliant document: " + str(ex)
        except PFASemanticException as ex:
            # PFA semantic check
            return False, "The file provided contains inconsistent PFA semantics: " + str(ex)
        except PFAInitializationException as ex:
            # Scoring engine check
            return False, "It wasn't possible to build a valid scoring engine from the PFA document: " + str(ex)
        except Exception as ex:
            # Other exceptions
            return False, "An unknown exception occurred: " + str(ex)

        # Check that the PFA file uses the "map" method. Other methods are not supported
        # (because irrelevant) by the MIP
        if not engine.config.method == "map":
            return False, "The PFA method you used is not supported. Please use the PFA 'map' method"

        # Check that the PFA file uses a "record" type as input
        if not isinstance(engine.config.input, AvroRecord):
            return False, "The PFA document must take a record as input parameter. " \
                          "Each field of the record must describe a variable"

        # Check that the PFA file has a least one input field
        if not engine.config.input.fields:
            return False, "The PFA document must describe an input record with at least one field"

        return True, None

    def validate_io(self, features_db_host, features_db_port, features_db_name, features_db_user,
                    features_db_password, features_db_table):
        """Extracts the variables from the PFA document, connects to a PostgreSQL database,
        retrieves values for said variables, try to input them to the PFA and see if it outputs
        consistent data"""

        # Get PFAEngine
        try:
            engine = self.get_engine()
        except (ValueError, PFASyntaxException, PFASemanticException, PFAInitializationException, Exception):
            return False, "Cannot instanciate PFAEngine ! Please use validate() method for more details."

        # Get input variables list
        pfa = json.loads(self.json_string)
        pfa_variables = [v['name'] for v in pfa['input']['fields']]

        # Get data from DB
        sql_template = """SELECT {} FROM {}"""
        prepared_statement = sql.SQL(sql_template).format(
            sql.SQL(',').join([sql.Identifier(i) for i in pfa_variables]),
            sql.Identifier(features_db_table))
        conn = connect(
            host=features_db_host,
            port=features_db_port,
            dbname=features_db_name,
            user=features_db_user,
            password=features_db_password
        )
        print "Select data..."
        print (prepared_statement)
        data = read_sql(prepared_statement, conn).to_dict('records')
        conn.close()

        try:
            print "Executing PFA..."
            for d in data:
                print "Input data: %s" % str(d)
                print "Result: %s" % str(engine.action(d))
        except PFARuntimeException as ex:
            return False, "A PFA library function encountered an exceptional case: " + str(ex)
        except PFAUserException as ex:
            return False, "The PFA has an explicit error directive: " + str(ex)
        except PFATimeoutException as ex:
            return False, "The PFA has a timeout setup and the calculation takes too long: " + str(ex)

        return True, None
