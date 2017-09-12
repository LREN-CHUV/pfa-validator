import sys
import os
import json
import titus.version
from titus.genpy import PFAEngine

print "Hello, world!"
print "Titus is installed with version:"
print titus.version.__version__

if (len(sys.argv) < 2):
  print "Program expects exactly one argument, that should be the path to the PFA file to validate"
  print "* Example: python main.py path_to_pfa.json"
  sys.exit()

pfapath = sys.argv[1]

if not os.path.exists(pfapath):
  print "The path you provided does not exist:", os.path.abspath(pfapath)
  sys.exit()

engine, = PFAEngine.fromJson(json.load(open(pfapath)))

if not engine.config.method == "map":
  print "Please use the PFA 'map' method. Other methods are not supported in the MIP."
  sys.exit()
