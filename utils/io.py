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

def build_kv_line(header, value,
        header_len=KV_HEADER_LEN,
        value_len=KV_VALUE_LEN,
        delimiter=KV_DELIMITER):
    return "{0:<{2}}{1:>{3}}\n".format(
        header + delimiter,
        value,
        header_len,
        value_len
    )

def play_sound(fn):
    if fn not in "":
        os.system("play -q " + fn)
        os.remove(fn)

def display_picture(fn):
    if fn not in "":
        os.system("feh --geometry={}x{} ".format(*TRANSCRIPTION_PICTURE_DIMENSIONS) + fn)
        os.remove(fn)
