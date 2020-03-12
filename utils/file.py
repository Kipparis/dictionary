import re
from collections import namedtuple

Word = namedtuple('Word', ['category', 'eng_str','ru_str',
    'description', 'clarification'])

class Dict:
    __slots__ = ("file_name", "word_dict")

    def __init__(self, file_name):
        self.file_name = file_name  # store inited filename
        self.word_dict = {}         # dictionary containing words from file

        d = self.word_dict  # shortcut for faster access


def parse_dict(file_name):
    """
    Parse categories in dict and yield words
    Words are returned by namedtuple `Word`
    """
    import os, itertools
    with open(file_name, "r") as f:
        header = ""
        for line in f:
            line = line.strip()
            # for each line there are two cases:
            #       header - assign variable header to it
            #       entry  - store into yielding value
            search = re.search(r"\A\[.*\]", line) # pattern for category name
            if not search or not search.group(0):
                # rm comments
                line = re.sub(r'#.*\Z',"",line).strip()
                # if there still is line => check if it
                # contains simple translation
                if line:
                    # build info
                    word_info = [e.strip() for e in line.split("-")]
                    while len(word_info) < 4:
                        word_info.append("")
                    yield Word(header, *word_info)
            # if "header pattern" has matched
            #   store new header value
            elif search and search.group(0):
                header = search.group(0)[1:-1]
    pass

