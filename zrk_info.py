from termcolor import colored

def err_print(string):
    print(colored('ERROR: ' + string, 'red'))


def ok_print(string):
    print(colored('INFO: ' + string, 'yellow'))


def ask_print(string):
    print(colored(string, 'blue'))