#!python3

import os, sys
from utils.dtypes import StringBool
from utils.file   import parse_dict
from utils.env    import get_env
from utils.settings import *
from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description="write a test, store"
        " results in db, than programm will decide what words to give"
        " you",
        epilog="If you need to delete some instance[s], you have to"
        " recreate entire table")

parser.add_argument("-d", "--db_file", type=str, default="words_res.db",
                                metavar="db_fn",
                                help="db filename for storing results")
parser.add_argument("-w", "--words_file", type=str, default="words.dict",
                                help="words file for sync with db",
                                metavar="w_fn")
parser.add_argument("-c", "--create",
                                help="create database (will drop"
                                " existing at specified path) (run only once)",
                                action="store_true", default=False)
parser.add_argument("-u", "--update", help="update words in database",
                                action="store_true", default=False)
parser.add_argument("-i", "--interactive", help="run program in"
                                " interactive mode",
                                action="store_true", default=False)

args = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_help()

# docs here http://docs.peewee-orm.com/en/latest/peewee/models.html
from peewee import *
db = SqliteDatabase(args.db_file)

# add logger
# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

# about fields
# http://docs.peewee-orm.com/en/latest/peewee/models.html#fields

class BaseModel(Model):
    class Meta:
        database = db   # this model uses the args.db_file database
        # change table name, default to name of class
        # table_name = string

class Category(BaseModel):
    '''
    list of existing caterogies
    '''
    name = CharField(default="")


class Result(BaseModel):
    '''
    table storing per-word score
    '''
    word = CharField(default="")
    score = IntegerField(default=0)
    # default - current date
    last_modified_date = DateField(default=datetime.now)
    category = ForeignKeyField(Category, backref="results")


# it's good practive to explicitly open the connection
db.connect()

# this will create the tables with the appropriate columns, foreign key
# constaints, etc ...
# db.create_tables([Result, Category])
if args.create:
    print("creating new table\n=================")
    with db:    # another way of creating tables
        db.create_tables([Result, Category])

def update_mod_time(db_file):
    import time, datetime
    mod_time = time.mktime(datetime.datetime.now().timetuple())
    os.utime(db_file, (mod_time, mod_time))

# to store models, you can use save() or create()

# you may wrap this into two cases: update, create
#   update - use existing structure
#   create - use db.atomic() wrapper or/and `insert_many`
# iterate over words in .dict file and uppend them
if args.update or args.create:
    previous_header = ""
    category = None
    for entry in parse_dict(args.words_file): # must return iterable
        print(f"GOT THIIS {entry}")
        # becouse I reassign every variable for every entry
        # it gonna to be very nice to memory (but opposite to CPU)
        # for every entry -> store in db
        if entry.category not in previous_header:   # category is new
            previous_header = entry.category        # assign category to var
            # check that category is created, if not -> create
            category, created = Category.get_or_create(name=previous_header)
            if not created: print(f"\"{category.name}\" already exists")
        # date, score applied automatically
        result, created = Result.get_or_create(word=entry.eng_str, category=category)
        if not created: print(f"\"{category.name}\":\"{entry.eng_str}\" - already exists")
    # explicitly call to update mod time, so we will know
    # that update function already ran
    update_mod_time(args.db_file)

def diff_m_time(lhf, rhf):
    return os.path.getmtime(lhf) - os.path.getmtime(rhf)

def word_count(db):
    return len(Result.select())

# call Select.iterator() when iterating.
# with python `sum` functional-style operator
def score(db):
    '''
    returns average of all scores
    '''
    ret = 0
    word_qty = word_count(db)

    return sum(result.score for result in \
            Result.select().where(Result.score > 0)) / word_qty

def build_statistics_line(header, value):
    return "{0:<{2}}{1:>{3}}\n".format(
        header + STATISTICS_DELIMITER,
        value,
        STATISTICS_HEADER_LEN,
        STATISTICS_VALUE_LEN
    )

def build_statistics(db):
    '''
    build statistics from database connection

    output format: "header: value"
    at the end - help message
    '''
    out = ""    # init empty string that we'll return
    # get last database modification time and substitute
    # .dict file's last modification time
    # if value positive - all okay, no update needed
    # otherwise some changes may not be migrated
    out += build_statistics_line("db_file", args.db_file)
    out += build_statistics_line(".db outdated",
            not bool(diff_m_time(args.db_file, args.words_file) > 0))
    out += build_statistics_line("words collected",
            str(word_count(db)))
    out += build_statistics_line("general score", str(score(db)))

    return out


if args.interactive:

    # TODO: incapsulate this logic
    #   there it is here because of testing
    from prompt_toolkit import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.buffer import Buffer    # editable buffer
    from prompt_toolkit.layout.containers import HSplit, VSplit, Window
    from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
    from prompt_toolkit.layout.layout import Layout
    from prompt_toolkit.application import get_app

    buffer1 = Buffer()  # editable buffer

    statistics_content="Info:\n\n"
    # build statistics from existing database
    # print statistics (maybe using external lib)
    #       last database update -- last dict file update
    #       how many words there are in database
    #       overall score between all words
    #       keybindings/help mindow on require
    #       show progress (people are training easier when see what they
    #           reached)

    statistics_content += build_statistics(db)

    # provide possobilities of training
    #       ability to choose max number of words
    #
    #       by category (you must be able to choose several)
    #       by preceding results (train words with less score)
    #
    words_qty     = DEFAULT_WORDS_QTY
    category_list = DEFAULT_CATEGORY_LIST
    improve       = DEFAULT_IMPROVE

    # TODO: next
    # dinamically build choice list from given functions
    # and link to them shortcuts as well dinamically

    choices="    Choose action:\n"
    choices_list = [
            f"choose words qty for training ({words_qty} now)",
            "choose categor(y/ies) which you'd like to train"
            f" ({category_list} now)",
            "wether you like to train what you know but not excelently"
            f" ({improve} now)",
            "find all translations (desired to improve your lexicon)",
            "train",
        ]
    choices += "\n".join(f"{i}. {text};" for i, text in
            enumerate(choices_list, start=1))

    tooltip = [
        "'all' in category list means all existing categories",
        "if you have less words then `words_qty` for now to improve,\n"
        "  then you will be given random wards from choosen `category` to\n"
        "  train",
        "find all translations - you'll be given native word, and you\n"
        "  must find all foreign translations",
    ]
    choices += "\n\nNote:\n" + "\n".join(tooltip)

    help_string="h - help page; q - quit"

    root_container = HSplit([
        Window(content=FormattedTextControl(text=statistics_content)),
        Window(content=FormattedTextControl(text=choices)),
        Window(height=1, char='-'),
        Window(height=1, content=FormattedTextControl(text=help_string))
    ])

    kb = KeyBindings()

    @kb.add('q')
    def exit_(event):
        '''
        Pressing `q` will exit the user interface

        Return value will be returned from the `Application.run()`
        '''
        event.app.exit()

    @kb.add('h')
    def help_(event):
        '''
        Pressing `h` will popup help page
        '''

    app = Application(
            layout=Layout(root_container),
            full_screen=True,
            key_bindings=kb
        )
    app.run()


# Formalities:
#
# Long term:
#   1. Console interface
#   2. Api
#   3. Git support
#   4. X support
#   5. Determine whether 256 color or not
#   6. Demostrate how application works in github
#   6.1     Usage
#   6.2     Screen demostration
#   7. Fill contributing section
#   8. Cool information how to learn efficiency (do not focus on my app)
#   8.1     Learn every day
#   8.2     Suggest timer app
#   8.3     Develop habbits
#   9. Pygmentize capability
#   10. Define custom colors
#   11. X11 capability for configs


db.close() # close connection
