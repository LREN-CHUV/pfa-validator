"""This file describes a subclass of JSONPFAValidator that reads the PFA document from the file
system. It facilitates the use of the program via command line."""

import sys
import os
from utils import print_error
from JSONPFAValidator import JSONPFAValidator

class FileJSONPFAValidator(JSONPFAValidator):
    """A JSONPFAValidator that loads the PFA document from the file system"""
    def __init__(self, pfa_path):
        JSONPFAValidator.__init__(self, '')
        if pfa_path is None:
            print_error("Program expects an PFA_PATH environment variable that contains the path "
                        "to PFA file to validate. Please refer to the associated README.md file "
                        "for detailed usage instructions")
            sys.exit(1)

        # Check that the pfa path passed by the user exists
        if not os.path.exists(pfa_path):
            print_error("The path you provided does not exist:" + os.path.abspath(pfa_path))
            sys.exit(1)

        self.pfa_path = pfa_path

    def load_document(self):
        json_string = None
        with open(self.pfa_path, 'r') as content_file:
            json_string = content_file.read()

        self.json_string = json_string
