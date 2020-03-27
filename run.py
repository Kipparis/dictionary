#!python3

import os, sys
from utils.dtypes import StringBool
from utils.file   import parse_dict
from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description="write a test, store "
        "results in db, than programm will decide what words to give you")

parser.add_argument("--db_file", type=str, default="words_res.db",
                                help="db filename for store results")
parser.add_argument("-w", "--words_file", type=str, default="words.dict",
                                help="words file for sync with db",
                                metavar="fn")
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
    sys.exit(1)

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

# to store models, you can use save() or create()

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


if args.interactive:
    # print statistics (maybe using external lib)
    #       last database update -- last dict file update
    #       how many words there are in database
    #       overall score between all words
    #       keybindings/help mindow on require

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

    statistics_content="    Info:\nEmpty for a while\nEnd than here appears something"
    help_string="h - help page; q - quit"
    choices="    Choose action:\n1. give me a respect;\n2. learn words with me"
    choices_list = [
            "give me a respect",
            "learn words with me"
        ]
    choices = "\n".join(f"{i}. {text};" for i, text in
            enumerate(choices_list, start=1))

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
        # TODO: procedurely generate help page from function docstrings

    app = Application(
            layout=Layout(root_container),
            full_screen=True,
            key_bindings=kb
        )
    app.run()

    # provide possobilities of training
    #       ability to choose max number of words
    #
    #       by category (you must be able to choose several)
    #       by preceding results (train words with less score)
    #

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


db.close() # close connection
