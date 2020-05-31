from .io import display_picture, play_sound
from .extracter import get_word_transcription, get_word_pronounciation

def visual_test():
    """
    test elements those can be displayed to user
    """

    word = "profile"    # just test for now, should use more complecated word
    issue = 0           # if issue occured => show issue url

    # test picture displaying
    # TRANSCRIPTION_SHOW_TEXT = False
    # TRANSCRIPTION_SHOW_PICTURE = True
    display_picture(get_word_transcription(word, False, True))
    ans = input("Does picture displayed correctly? (y/n)")
    if ans not in "y":
        print("You should set TRANSCRIPTION_SHOW_PICTURE to false or make an issue")
        issue |= 1
    # test transcription in terminal
    # TRANSCRIPTION_SHOW_TEXT = True
    # TRANSCRIPTION_SHOW_PICTURE = False
    display_picture(get_word_transcription(word, True, False))
    ans = input("Does text displayed correctly?")
    if ans not in "y":
        print("You should set TRANSCRIPTION_SHOW_TEXT to false or make an issue")
        issue |= 1
    # test sound playing
    play_sound(get_word_pronounciation(word))
    ans = input("Does sound being played correctly?")
    if ans not in "y":
        print("You should make an issue")
        issue |= 1

    if issue:
        print("You can create issue here: <github url here>")
