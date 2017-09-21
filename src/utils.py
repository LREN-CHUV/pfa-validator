"""Utility functions to print successful ("OK") and unsuccessful ("ERROR") validation steps"""

OK = '\033[92m'
ERROR = '\033[91m'
ENDC = '\033[0m'

def print_error(message):
    """Prints a string in the terminal by prefixing it with a colored "[ ERROR ]" label"""
    print ERROR + "[ ERROR ] - " + ENDC + message

def print_ok(message):
    """Prints a string in the terminal by prefixing it with a colored "[ OK ]" label"""
    print OK + "[ OK ] - " + ENDC + message
