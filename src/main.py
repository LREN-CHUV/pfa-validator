"""Program entrypoint when used as command line tool. Dynamic usage should directly import the
JSONPFAValidator file"""

import sys
import os
from utils import print_ok, print_error
from JSONPFAValidator import JSONPFAValidator


# Check that a PFA_PATH variable was set
PFA_PATH = os.environ.get('PFA_PATH')

if PFA_PATH is None:
    print_error("Program expects an PFA_PATH environment variable that contains the path to "
                "PFA file to validate. Please refer to the associated README.md file for "
                "detailed usage instructions")
    sys.exit(1)

# Check that the pfa path passed by the user exists
if not os.path.exists(PFA_PATH):
    print_error("The path you provided does not exist:" + os.path.abspath(PFA_PATH))
    sys.exit(1)

PFA_STRING = None
with open(PFA_PATH, 'r') as content_file:
    PFA_STRING = content_file.read()

VALIDATOR = JSONPFAValidator(PFA_STRING)
(VALID, REASON) = VALIDATOR.validate()

if not VALID:
    print_error(REASON)
    sys.exit(1)

print_ok("This is a valid PFA file!")
