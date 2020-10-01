import os
import re
import itertools
from collections import namedtuple

from .file import *     # file manipulations
from .settings import * # configuration
from .io import *       # easy input/output
from peewee import *    # database handling
from .models import Category, Result

Word = namedtuple('Word', ['category', 'eng_str','ru_str',
    'description', 'example'])

# docs here http://docs.peewee-orm.com/en/latest/peewee/models.html

class Dictionary:
    """
    shortcuts to database queries + all data related functions
    """
    __slots__ = (
            "words_file_name",
            "db_file_name",
            "word_dict",
            "db",
            "Category_model",
            "Result_model"
        )

    def __init__(self, words_file_name="", database_file_name=""):
        self.words_file_name = words_file_name      # store inited filename
        self.db_file_name = database_file_name      # database file (e.g. .db extension)
        self.word_dict = {}         # dictionary containing words from file

        # add logger
        # import logging
        # logger = logging.getLogger('peewee')
        # logger.addHandler(logging.StreamHandler())
        # logger.setLevel(logging.DEBUG)
        self.db = SqliteDatabase(database_file_name)
        self.db.connect()
        # it's good practive to explicitly open the connection
        self.db.bind([Category, Result])
        # TODO: after each init check for last modified date
        # and decrease score

        self.Category_model = Category
        self.Result_model   = Result

    def __str__(self):
        return "hola"

    def __del__(self):
        self.db.close() # close connection

    # return iterator for entries in file
    def entries_from_file(self):
        """
        Parse categories in dict and yield words
        Words are returned by namedtuple `Word`
        """
        with open(self.words_file_name, "r") as f:
            header = ""
            for line in f:
                # strip and rm comments
                line = re.sub(r'#.*',"",line).strip()
                # for each line there are two cases:
                #       header - assign variable header to it
                #       entry  - store into yielding value
                if not line: continue   # if line empty we have nothing to do with it
                search = re.search(r"\A\[.*\]", line) # pattern for category name
                if not search or not search.group(0):
                    # TODO: sometimes i can pass something like this
                    # tie, necktie - галстук
                    word_info = [e.strip() for e in line.split("-")]
                    while len(word_info) < 4:
                        word_info.append("")
                    # return structure Word
                    yield Word(header, *word_info)
                # if "header pattern" has matched
                #   store new header value
                elif search and search.group(0):
                    header = search.group(0)[1:-1]
        pass

    def create(self):
        with self.db:    # another way of creating tables
            self.db.create_tables([self.Result_model, self.Category_model])
        pass

    def update(self):
        previous_header = ""
        category = None
        for entry in self.entries_from_file(): # must return iterable
            print(f"GOT THIIS {entry}")
            # becouse I reassign every variable for every entry
            # it gonna to be very nice to memory (but opposite to CPU)
            # for every entry -> store in db
            if entry.category not in previous_header:   # category is new
                previous_header = entry.category        # assign category to var
                # check that category is created, if not -> create
                category, created = self.Category_model.get_or_create(name=previous_header)
                if not created: print(f"\"{category.name}\" already exists")
            # date, score fields applied automatically
            result, created = self.Result_model.get_or_create(
                    word=entry.eng_str,
                    native=entry.ru_str,
                    description=entry.description,
                    example=entry.example,
                    category=category)
            if not created: print(f"\"{category.name}\":\"{entry.eng_str}\" - already exists")
        # explicitly call to update mod time, so we will know
        # when database syncronized with words.dict file
        update_mod_time(self.db_file_name)
        pass

    @property
    def categories(self):
        return self.Category_model.select()

    @property
    def words(self):
        """
        fetch all words
        """
        return self.Result_model.select()

    def words_by_category(self, category):
        """
        fetch words by category
        """
        # query = Tweet.select().join(User).where(User.username == 'huey')
        return(self.Result_model.select().join(self.Category_model).where(self.Category_model.name == category))


    @property
    def word_count(self):
        return len(self.Result_model.select())

    # call Select.iterator() when iterating.
    # with python `sum` functional-style operator
    @property
    def score(self):
        '''
        returns average of all scores for each of words in database
        '''
        ret = 0
        word_qty = self.word_count

        return sum(result.score for result in \
                self.Result_model.select().where(self.Result_model.score > 0)) / word_qty

    def get_common(self, word):
        """
        return word list each having same `native` translation as passed argument
        """
        return(self.Result_model
                .select()
                .where(self.Result_model.native == word.native))
        pass


    def build_statistics(self):
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
        out += build_kv_line("db_file", self.db_file_name)
        out += build_kv_line(".db outdated",
                not bool(diff_m_time(self.db_file_name, self.words_file_name) > 0))
        out += build_kv_line("words collected", str(self.word_count))
        out += build_kv_line("general score", str(self.score))

        return out

    def set_score(self, word_entry, new_score):
        res = (self.Result_model
                .update(score=new_score)
                .where(self.Result_model.word == word_entry.word)
                .execute())

    def get_words_for_training(self, w_qty, category_list, improve):
        words = []
        # first get query for categories
        if "all" in category_list:
            words = self.words
        else:
            words=(self.Result_model.select()
                .join(self.Category_model)
                .where(self.Category_model.name.in_(category_list)))

        # then choose words depending on improve rules
        if improve:
            # get less unswered words
            words = words.order_by(self.Result_model.score)
        print("(get_words_for_training) Words len: {}".format(len(words)))
        # then slice word qty
        # words = words.limit(w_qty).namedtuples()
        words = words.limit(w_qty)
        return words
