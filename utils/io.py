import os

from .settings import *
from .env import *

def terminal_deminsions():
    """
    returns: [rows, columns] of the currently running terminal
    """
    return os.popen('stty size', 'r').read().split()

def linewise_line():
    return f"{ACTION_DELIMITER}"*int(terminal_deminsions()[-1])

def prompt():
    return get_env("PS3", DEFAULT_PROMPT)

# build the prompt
def build_prompt():
    rows, columns = terminal_deminsions()
    return "\n"+linewise_line()+"\n" + prompt()
