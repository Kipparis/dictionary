#!python3

import os
from utils.dtypes import StringBool
from utils.file   import parse_dict
from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description="write a test, store "
        "results in db, than programm will decide what words to give you")
parser.add_argument("--db_file", type=str, default="words_res.db",
        help="db filename for store results")
parser.add_argument("-w", "--words_file", type=str, default="words.dict",
        help="words file for sync with db", metavar="file_name")
parser.add_argument("-c", "--create", help="create database (will drop"
        " existing at specified path) (run only once)",
        action="store_true", default=False)
parser.add_argument("-u", "--update", help="update words in database",
        action="store_true", default=False)
args = parser.parse_args()

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


# check that all categories are in table
# for category in Category.select():
#     print(category.name)



# TODO: in loop:
#   1. collect how many words from each category does he answered,
#       output statistic
#       on welcom page output this statistic
#       and percantage of overall words knowledge
#   2. ask user how many words he wants to learn (default = 7)
#   3. ask user which categories does he prefer (default = all)
#   4. run test
#
# Formalities:
#   1. Create simple usage for newcommers
#
# Long term:
#   1. Console interface
#   2. Api
#   3. Git support


db.close() # close connection
