# Purpose
You want to practice foreign languages.  

# Why not just write in notebook
The program will store your results in database for long period. You may
train specific category, or train words which you stored, but never
trained (never used them).  
**_Shortly_**: you'll have more options of learning. Put yourself in a
difficult situation to learn more.  

# How many dependencies
You must have **_python_**.  
All dependencies are collected in [reqs.txt](https://github.com/Kipparis/dictionary/blob/master/reqs.txt)
file  
Most noticable list of them:  

+ database tools ([peewee](https://github.com/coleifer/peewee)).  
+ fullscreen interactive mode ([prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/index.html))  

# How to use

# TODO
## Implement

+ scoring system  
    - when it is required to anwer similar words, system should
  output list of groups which contain word  
    - score formula must contain reference to 75% correct
  words and last date  
+ fixed systax  
+ write interactive addition to .dict file  
+ offer an query string and css selecter for taking subscription
&rarr; print in in png &rarr; output using xdg open or something like
that  
+ vim-like keybindings  
+ movement, highlight current selection  
+ save user preferences  
+ hardmode. e.g. foreign description only  
+ word dict as submodule, so everyone may not 
  update main app but update dictionary  
    * script for updating either main app or dictonary or both  

### Syntax

+ pronounciation  
+ vim string in top  
    - comment  
+ implement possibility for simple list of words like:  
    - irregular words  
    - nationalities  

## Tests

+ scoring system  
+ syntax parsing  
    - database stores correctly  
    - tokens parsing correctly  

## Newcomers

+ tutorial how to add new word in .dict  
+ how to tune vim to easily navigate through file  

# Contributing
I will appreciate any advice or pull request that you make.  
Verify my signs by this <write> using GPG key.  

