import os
import re
import itertools
from collections import namedtuple

from .file import *     # file manipulations
from .settings import * # configuration
from peewee import *    # database handling

Word = namedtuple('Word', ['category', 'eng_str','ru_str',
    'description', 'clarification'])

# docs here http://docs.peewee-orm.com/en/latest/peewee/models.html

def build_statistics_line(header, value):
    return "{0:<{2}}{1:>{3}}\n".format(
        header + STATISTICS_DELIMITER,
        value,
        STATISTICS_HEADER_LEN,
        STATISTICS_VALUE_LEN
    )


class Dictionary:
    """
    shortcuts to database queries + all data related functions
    """
    __slots__ = ("words_file_name", "db_file_name", "word_dict", "db", "Category_model", "Result_model")

    def __init__(self, words_file_name="", database_file_name=""):
        self.words_file_name = words_file_name  # store inited filename
        self.db_file_name = database_file_name    # database file (e.g. .db extension)
        self.word_dict = {}         # dictionary containing words from file

        # add logger
        # import logging
        # logger = logging.getLogger('peewee')
        # logger.addHandler(logging.StreamHandler())
        # logger.setLevel(logging.DEBUG)
        self.db = SqliteDatabase(database_file_name)
        # it's good practive to explicitly open the connection
        self.db.connect()

        # about fields
        # http://docs.peewee-orm.com/en/latest/peewee/models.html#fields
        class BaseModel(Model):
            class Meta:
                database = self.db   # this model uses the args.db_file database
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

        self.Category_model = Category()
        self.Result_model   = Result()

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
            result, created = self.Result_model.get_or_create(word=entry.eng_str, category=category)
            if not created: print(f"\"{category.name}\":\"{entry.eng_str}\" - already exists")
        # explicitly call to update mod time, so we will know
        # when database syncronized with words.dict file
        update_mod_time(self.db_file_name)
        pass

    @property
    def categories(self):
        return self.Category_model.select()


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
        out += build_statistics_line("db_file", self.db_file_name)
        out += build_statistics_line(".db outdated",
                not bool(diff_m_time(self.db_file_name, self.words_file_name) > 0))
        out += build_statistics_line("words collected", str(self.word_count))
        out += build_statistics_line("general score", str(self.score))

        return out

