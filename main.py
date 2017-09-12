import sys
import titus.version

print "Hello, world!"
print "Titus is installed with version:"
print titus.version.__version__

if (len(sys.argv) < 2):
  print "Program expects exactly one argument, that should be the path to the PFA file to validate"
  print "* Example: python main.py path_to_pfa.json"
  sys.exit()

print "You called the program with argument", sys.argv[1]
