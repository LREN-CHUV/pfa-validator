import sys
import os
import json
import titus.version
from titus.genpy import PFAEngine

print "Hello, world!"
print "Titus is installed with version:"
print titus.version.__version__

pfapath = os.environ.get('PFA_PATH')

if (pfapath is None):
  print ("Program expects the file path to the PFA file to validate, that should be passed as the "
        "PFA_PATH environment variable.")
  print "* Example:"
  print "  PFA_PATH=path_to_pfa.json python main.py"
  print "* Example (if run in a docker container):"
  print "  docker run --name pfa-validator-1 -e PFA_PATH=\"path_to_pfa.json\" pfa-validator"
  sys.exit()

if not os.path.exists(pfapath):
  print "The path you provided does not exist:", os.path.abspath(pfapath)
  sys.exit()

engine, = PFAEngine.fromJson(json.load(open(pfapath)))

if not engine.config.method == "map":
  print "Please use the PFA 'map' method. Other methods are not supported in the MIP."
  sys.exit()
