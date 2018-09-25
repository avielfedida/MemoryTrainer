# MemoryTrainer
Simple to use, windows only, CMD application to help you remember stuff

## Basic idea
Basically it's a self adjustable key value pairs trainer.
Simply put, it shows you terms you want to remember, if tell the software if you remembered it or not,if you remembered, the software will adjust itself to show this term less and less, if you failed to remember, this term will be prioritize and be shown more often until you report that you remember it.

So a simple case might be that you want to learn some technical terms such as network, grapics card and algorithm, you insert these terms, giving each a `category`, a `name`(the term) and an `answer`, after that you will go over to the study option, you will be shown one of these words, because they just inserted they have equal chance to appear, but let's say you got network, wasn't able to remember the `answer` for this term you stated you don't remember, you now get to see the `answer` so you can learn, then decide if you want to get another word, now because you didn't remembered the term network, it has more chance of showing then grapics card or algorithm terms.

With that said, it's a simple use-case for this application, there are plenty more options...

## Technicals
 - Sql3 as a database

## Required packages
- matplotlib

## Features
- 2 Study modes
  - Self pace:
    1. shown a word
    2. shown a Y/N(remembered or not)
    3. answer is shown
    4. finish or next word
  - Speed
    1. shown a word, one after the other, no answer is shown.
    2. if decide to stop or a limit you configure reaches
    3. you see all the answers for all the terms you didn't remembered
 - Statistics: every time you exit the software it record you current learning state, choosing the statistics options you can see a simple 2D graph of you learning progress, it accumulates all you statistics updates per day, as days goes by you can see if you get better or maybe you add more terms then you study them.
 - Categories and Modes switching: when you hit study you get terms under certain category you decide, as a default, the category with most terms is choosed when the application starts, you can switch category, and you can switch mode.


### Tests
It tested manually on a 64 bit windows 10 Pro

### Supported languages
English only

### License
MIT
