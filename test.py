#!python3

import os
from utils.dtypes import StringBool
from utils.file   import parse_dict
from datetime import datetime

import argparse

parser = argparse.ArgumentParser(description="write a test, store "
        "results in db, than programm will decide what words to give you")
parser.add_argument("--db_file", type=str, default="words_res.db"
        help="db filename for store results")
parser.add_argument("-c", "--create", help="create new db",
        action="store_true")
parser.add_argument("-w", "--words_file", type=str, default="words.dict",
        help="words file for sync with db", metavar="file_name")
parser.add_argument("-u", "--update", help="update words in database",
        action="store_true", default=True)
args = parser.parse_args()

# docs here http://docs.peewee-orm.com/en/latest/peewee/models.html
from peewee import *
db = SqliteDatabase(args.db_file)
# about fields
# http://docs.peewee-orm.com/en/latest/peewee/models.html#fields
class Result(Model):
    '''
    table storing per-word score
    '''
    word = CharField()
    score = IntegerField(default=0)
    # default - current date
    last_modified_date = DateField(default=datetime.now)
    category_link = ForeignKeyField(Category, backref="results")

    class Meta:
        database = db   # this model uses the args.db_file database
        # change table name, default to name of class
        # table_name = string

class Category(Model):
    '''
    list of existing caterogies
    '''
    name = CharField()

    class Meta:
        database = db

if args.create:
    # create tables
    db_cursor.execute('''CREATE TABLE categories
            (ID int NOT NULL PRIMARY KEY,
            category_name text
            )''')
    db_cursor.execute('''CREATE TABLE results
            (ID int NOT NULL PRIMARY KEY,
            word text,
            score int,
            date_added date,
            category int DEFAULT -1
                REFERENCES categories(ID)
                ON UPDATE CASCADE
                ON DELETE SET DEFAULT
            )''')
    # iterate over words in .dict file and uppend them
    for entry in parse_dict(args.words_file): # must return iterable
        print(f"GOT THIIS {entry}")
        # becouse I reassign every variable for every entry
        # it gonna to be very nice to memory (but opposite to CPU)
        # for every entry -> store in db


# if args.update:



# TODO: in loop:
#   1. ask user how many words he wants to learn (default = 7)
#   2. ask user which categories does he prefer (default = all)
#   3. run test
#   4. collect how many words from each category does he answered,
#       output statistic
#       on welcom page output this statistic
#       and percantage of overall words knowledge
# Formalities:
#   1. Create simple usage for newcommers


db_conn.close() # close connection
