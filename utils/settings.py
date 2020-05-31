KV_HEADER_LEN = 20
KV_VALUE_LEN  = 10
KV_DELIMITER  = ":"

DEFAULT_WORDS_QTY     = 5
DEFAULT_CATEGORY_LIST = ["all"]
DEFAULT_IMPROVE       = True

INDENT_STRING = "    "

# if environment variable PS3 is not set,
# otherwise, use PS3 (you must explicitly
# specify it in login source):
# export PS3="enter action number: "
DEFAULT_PROMPT = "enter action number: "

# single character (will be multiplied 10 times)
# It is used for delimiting actions in output
ACTION_DELIMITER = "-"

PRONOUNCIATION_REQUEST_STRING = "https://ssl.gstatic.com/dictionary/static/sounds/oxford/{}--_us_1.mp3"

TRANSCRIPTION_SHOW_PICTURE = False
TRANSCRIPTION_SHOW_TEXT = True
TRANSCRIPTION_REQUEST_STRING = "https://wooordhunt.ru/word/{}"
# TODO: calculate this from screen dimensions
TRANSCRIPTION_PICTURE_DIMENSIONS = [600, 100]
