#!python3

import os, sys
from utils.dtypes import StringBool
from utils.file   import *
from utils.dict import Dictionary
from utils.env    import get_env
from utils.settings import *
from utils.train import *
from utils.io import *

import argparse

# TODO: when you can't unswer maximum words, you'll be given only subset
# to train, and then you come back to normal training
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
parser.add_argument("-f", "--test_features", help="test features"
                                " available in the progam. This option might help you correct"
                                " settings file", action="store_true", default=False)
parser.add_argument("-t", "--transcription", help="get transcription for specified string",
                                type=str, metavar="phrase/word")

args = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_help()

# run test_features if user selected option
if args.test_features:
    from utils.test import visual_test
    visual_test()

if args.transcription:
    display_picture(get_word_transcription(args.transcription))

words_dict = Dictionary(words_file_name=args.words_file, database_file_name=args.db_file)

# this will create the tables with the appropriate columns, foreign key
# constaints, etc ...
# db.create_tables([Result, Category])
if args.create:
    words_dict.create()
    print("creating new table\n=================")

# to store models, you can use save() or create()

# you may wrap this into two cases: update, create
#   update - use existing structure
#   create - use db.atomic() wrapper or/and `insert_many`
# iterate over words in .dict file and uppend them
if args.update or args.create:
    words_dict.update()


def build_choices(header, dictionary, after):
    """
    prompt will be displayed on separate line above all of the choices
    then on each line will be enumerated choices
    after that `after` variable will be appended to output
    """
    out = f"{header}\n"
    for i, (key, item) in enumerate(dictionary.items(), start=1):
        out += f"{INDENT_STRING}{i}. {item}\n"
    out += after
    return out


if args.interactive:
    # build statistics from existing database
    # print statistics (maybe using external lib)
    #       last database update -- last dict file update
    #       how many words there are in database
    #       overall score between all words
    #       keybindings/help mindow on require
    #       show progress (people are training easier when see what they
    #           reached)

    # provide possobilities of training
    #       ability to choose max number of words
    #
    #       by category (you must be able to choose several)
    #       by preceding results (train words with less score)
    #
    choices_header  = "Choose action:"

    category_list = DEFAULT_CATEGORY_LIST
    # create list from simple arguments so we can pass
    # them as reference in functions
    words_qty     = [DEFAULT_WORDS_QTY]
    improve       = [DEFAULT_IMPROVE]

    def display_statistics():
        statistics_content="Info:\n\n"
        statistics_content += words_dict.build_statistics()
        print(statistics_content)
        pass

    def display_help():
        out = f"{choices_header}\n"
        for i, (key, item) in enumerate(choices_dict.items(), start=1):
            string = f"{INDENT_STRING}{i}. {item}\n"
            out += string.format(**globals())
        out += "\n\nNote:\n" + "\n".join(tooltip)
        print(out)
        pass

    def choose_word_qty(words_qty_pseudo):
        '''
        choose words qty for training
        '''
        try:
            words_qty_pseudo[0] = int(input("enter new words_qty (max"
                " {}): ".format(words_dict.word_count)))
            print(f"set words_qty to {words_qty}")
        except ValueError:
            print("Not correct number")
        pass

    def choose_category(category_list):
        '''
        choose categor(y/ies) for training
        '''
        # output list of all existing categories
        print("\n".join([category.name for category in words_dict.categories]) + "\nall")
        # assign TO the list, do not create copy
        category_list[:] = [entry.strip() for entry in
            str(input("Enter categories delimited by `;`:")).split(";")]
        pass

    def set_improve(improve_pseudo):
        '''
        enable improve mode (train what you already know but not mastered)
        '''
        answ = str(input("Improve mode enabled (Y/n): "))
        if answ in "n" or answ in "N" or answ in "no":
            improve_pseudo[0] = False
        else:
            improve_pseudo[0] = True
        print(improve_pseudo)
        pass

    def train():
        '''
        start training
        '''
        start_train(words_dict, words_qty, category_list, improve)
        pass

    def quit():
        print("\nbye :)")
        sys.exit(0)
        pass

    # to bind arguments to function

    import functools

    choices_dict = {
            display_help:       "display help",
            display_statistics: "display statistics",
            # binding function arguments allow us to call it
            # without arguments
            functools.partial(choose_word_qty, words_qty):
                "choose words qty ({words_qty[0]})",
            functools.partial(choose_category, category_list):
                "choose categories ({category_list})",
            functools.partial(set_improve, improve):
                "set improve mode ({improve[0]})",
            train:  "start training",
            quit:   "quit program"
        }

    tooltip = [
        "'all' in category list means all existing categories",
        "if you have less words then `words_qty` for now to improve,\n"
        f"{INDENT_STRING}then you will be given random wards from choosen `category` to\n"
        f"{INDENT_STRING}train",
        "find all translations - you'll be given native word, and you\n"
        f"{INDENT_STRING}must find all foreign translations",
    ]

    display_help()


    # get int from user input (assume that is N)
    # take N-th entry in `choices_dict`
    # call function (first element in dict entry)
    while True:
        try:
            list(choices_dict.keys())[int(input(build_prompt()))-1]()
        # except (IndexError, ValueError):
        #     print("Enter coorect value in range"
        #             " [1;{}]".format(len(choices_dict)))
        except (KeyboardInterrupt, EOFError):
            # have to pass instance explicitly,
            # otherwise it doesn't see it
            quit(words_dict)

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


