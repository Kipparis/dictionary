import unittest

from utils.extracter import get_word_transcription, get_word_pronounciation
from utils.io import play_sound, display_picture

from utils.settings import *

from peewee import *
from utils.models import Category, Result


class TestExtracter(unittest.TestCase):
    def test_transcription_single(self):
        """
        Test that transcription extracter works fine with single word
        """
        word = "profile"            # test string
        transcription = get_word_transcription(word)

        self.assertIn(transcription, "ˈproʊfaɪl")

    def test_transcription_multi(self):
        """
        Test that transcription extracter works fine with multiple words
        """
        phrase = "without my leave" # test string
        transcription = get_word_transcription(phrase)

        self.assertIn(transcription, "wɪˈðaʊt maɪ liːv")

    def test_pronunciation_multi(self):
        """
        test that extracting phrase pronunciation works fine
        """
        phrase = "without my leave" # test string

        # check length in ms of each word
        # add ms of silence places
        # check that overall length is same

class TestTrainMode(unittest.TestCase):
    def setUp(self):
        """
        database setup
        """
        # from .models import Result, Category
        #
        # # Bind model classes to test db. Since we have a complete list of
        # # all models, we do not need to recursively bind dependencies.
        # test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        #
        # test_db.connect()
        # test_db.create_tables(MODELS)
        self.db = SqliteDatabase(':memory:')
        self.db.bind([Category, Result])

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        self.db.drop_tables([Category, Result])

        # Close connection to db.
        self.db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.

    def test_right_answer(self):
        """
        check that after answering only specific amount of points added
        to specific words
        """



if __name__ == '__main__':
    unittest.main()
