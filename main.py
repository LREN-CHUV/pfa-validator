import sys
import os
import json
import titus.version
from titus.genpy import PFAEngine

class colors:
  OK = '\033[92m'
  ERROR = '\033[91m'
  ENDC = '\033[0m'

def printError(message):
  print colors.ERROR + "[ ERROR ] - " + colors.ENDC + message

def printOk(message):
  print colors.OK + "[ OK ] - " + colors.ENDC + message

printOk("Titus is installed with version:" + titus.version.__version__)

pfapath = os.environ.get('PFA_PATH')

if (pfapath is None):
  printError("Program expects an PFA_PATH environment variable that contains the path to "
    "PFA file to validate. Please refer to the associated README.md file for detailed usage "
    "instructions")
  sys.exit()

printOk("The PFA_PATH environment variable was provided")

if not os.path.exists(pfapath):
  printError("The path you provided does not exist:" + os.path.abspath(pfapath))
  sys.exit()

printOk("The PFA_PATH variable is a valid path")

engine, = PFAEngine.fromJson(json.load(open(pfapath)))

if not engine.config.method == "map":
  printError("The PFA method you used is not supported. Please use the PFA 'map' method")
  sys.exit()

printOk("The PFA document uses the 'map' method which is supported by the MIP")
