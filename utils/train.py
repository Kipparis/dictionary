from .dict import *
from .extracter import *
from random import random, shuffle # shaffle list of tasks

def start_train(words_dict, words_qty_pseudo, category_list, improve_pseudo):
    w_qty = words_qty_pseudo[0]
    improve = improve_pseudo[0]
    print("selected options:")
    print(build_kv_line("words_qty", w_qty)
        + build_kv_line("category_list", ",".join(category_list))
        + build_kv_line("improve mode", improve))

    # get words depending on choise
    words = words_dict.get_words_for_training(w_qty, category_list, improve)
    print("len(words): {}".format(len(words)))
    print("separate multiple entries by ';'")
    print("enter 'p' to play pronounciation")
    print("enter 't' to see transciption")
    print("\n")

    words_tuple = words.namedtuples()
    for word in words_tuple: print(word)
    print("Shuffle words")
    print(words)

    errors_exist = True
    while errors_exist:
        does_continue = input("Continue?")
        if does_continue in "yes" or does_continue in "Yes"\
                or does_continue in "":
            print(page_break())

        # words = words.order_by(fn.random())

        wrong_words = []

        # TODO: aggregate all synonims when building database
        # start asking
        for word in words:
            # get list of synonyms (so user must answer all of them)
            translations = words_dict.get_common(word)

            # output info to user
            print("Enter translations for: '{}' ({})".format(word.native, len(translations)))

            # TODO: enter or exit transcription mode and
            # pronounciation on right error or wrong error
            # take user input
            user_input = str(input())
            while user_input in "p" or user_input in "t":
                if user_input in "p":
                    play_sound(get_word_pronounciation(word.word))
                elif user_input in "t":
                    display_picture(get_word_transcription(word.word))
                user_input = str(input())

            user_transl = user_input

            # words that user answered
            answered_words = [ans.strip() for ans in user_transl.split(";")]

            # for every synonym
            for i, trans in enumerate(translations):
                # check that synonym is present in user answers
                # if not present
                if trans.word not in answered_words:
                    # build list to output wrong words
                    # when user done with training
                    wrong_words.append([trans.word, trans.native])
                    # call word_dict to update word's score
                    new_score=trans.score - 1
                    words_dict.set_score(trans, new_score)
                # if present (user answered correctly)
                else:
                    # call word_dict to update word's score
                    new_score=trans.score + 1
                    words_dict.set_score(trans, new_score)
            print("Right answer is: " +\
                    ", ".join(trans.word for trans in translations))

            print("\n")

        # after all words give list of correct answers to those been wrong
        # print("Correct words are")
        # to_print=""
        # for entry in wrong_words:
        #     to_print+=build_kv_line(entry[0], entry[-1])
        # print(to_print)
        errors_exist = len(wrong_words) > 0


