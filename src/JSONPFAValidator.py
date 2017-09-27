"""This file describes the implementation of the JSONPFAValidator class, which contains the main
logic of the program"""

import json
import titus
from titus.genpy import PFAEngine

class JSONPFAValidator(object):
    """The JSONPFAValidator contains the main logic of the program. It provides a function
    `validate` that validates a JSON PFA file, by checking its JSON syntax, its PFA syntax, its PFA
    semantics and that it uses the PFA `map` method, which is required by the MIP"""

    def __init__(self, json_string):
        self.json_string = json_string
        self.engine = None

    def get_engine(self):
        """Creates a PFA engine based on the json_string provided as constructor class. If an
        engine was already created, this method does nothing"""
        if not self.engine:
            self.engine = PFAEngine.fromJson(json.loads(self.json_string))

        return self.engine

    def validate(self):
        """A function that validates a PFA described as a string
        Returns a 2-uple. The first element is boolean that is True or False if JSON string
        represents a valid PFA file. The second is a string explaining the reason if the PFA file is
        not valid"""

        # Check that a PFA engine can be correctly instantiated
        valid_json = True
        valid_pfa_syntax = True
        valid_pfa_semantic = True
        valid_scoring_engine = True
        no_other_exception = True

        reason = None
        engine = None

        try:
            # pylint: disable=unbalanced-tuple-unpacking
            engine, = self.get_engine()
        except ValueError as ex:
            valid_json = False
            reason = str(ex)
        except titus.errors.PFASyntaxException as ex:
            valid_pfa_syntax = False
            reason = str(ex)
        except titus.errors.PFASemanticException as ex:
            valid_pfa_semantic = False
            reason = str(ex)
        except titus.errors.PFAInitializationException as ex:
            valid_scoring_engine = False
            reason = str(ex)
        except Exception as ex:
            no_other_exception = False
            reason = str(ex)

        if not valid_json:
            return (False, "The file provided does not contain a valid JSON document: "  + reason)

        if not valid_pfa_syntax:
            return (False, "The file provided does not contain a valid PFA compliant document: "
                    + reason)

        if not valid_pfa_semantic:
            return (False, "The file provided contains inconsistent PFA semantics: " + reason)

        if not valid_scoring_engine:
            return (False, "it wasn't possible to build a valid scoring engine from the PFA "
                           "document: " + reason)

        if not no_other_exception:
            return (False, "An unknown exception occurred: " + reason)

        # Check that the PFA file uses the "map" method. Other methods are not supported
        # (because irrelevant) by the MIP
        if not engine.config.method == "map":
            return (False, "The PFA method you used is not supported. Please use the PFA 'map' "
                           "method")

        return (True, None)
