from .dict import *
from .extracter import *

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

    wrong_words = []

    # start asking
    for word in words:
        # get list of synonyms (so user must answer all of them)
        translations = words_dict.get_common(word)

        # output info to user
        print("Enter translations for: '{}' ({})".format(word.native, len(translations)))

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

        print("\n")

    # after all words give list of correct answers to those been wrong
    print("Correct words are")
    to_print=""
    for entry in wrong_words:
        to_print+=build_kv_line(entry[0], entry[-1])
    print(to_print)


