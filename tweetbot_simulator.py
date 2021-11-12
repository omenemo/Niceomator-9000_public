
# https://docs.tweepy.org/en/stable/getting_started.html#introduction
# Example: https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/twitter-data-in-python/

"""

# Create twitter account
# Potentially apply for developer/academic status

# In the command line:

pip install tweepy

"""

# Libraries

import os
import tweepy
import random
from os import listdir
from os.path import isfile, join
from memegenerator import make_meme
import text2emotion as te

potential_tweets = [
    "I don't care about your 'gender identity' shut up and suck my dick bro",
    "There are two genders. Rest are biological and genetic anomalies.\nThe are two kinds of sexuality. Rest are glorified kinks.",
    "Slavery and genocide exist right now in North Korea and China yet far left more concerned with micro-aggression, gender pronouns, and what the weather might be like in 100 years.",
    "Way to show your true colors Wolf, \nMakes sence to postpone nonlife threating surgeries,  however abortion is still a go. \n"
    "You evil ,evil , socialist globalist pig.\n Eat shit and die. You suck.\n SHUT UP AND SIT DOWN"
]

memes_folder = "meme_folder"
emotions = ["Happy", "Angry", "Surprise", "Sad", "Fear"]

# Search for tweets
search_words = 'gender identity'
matched_tweets =  [i for i in potential_tweets if search_words in i]

def get_random_meme_picture_for_emotion(emotion):
    mypath = os.path.join(memes_folder, emotion)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    random_meme_picture = random.choice(onlyfiles)
    random_meme_picture = os.path.join(mypath, random_meme_picture)
    return random_meme_picture

def split_tweet(tweet):
    words = tweet.split(" ")
    middle = int(len(words)/2)
    first_part = " ".join(words[:middle])
    second_part = " ".join(words[middle:])
    return first_part, second_part

if len(matched_tweets) > 0:
    tweet_text = matched_tweets[0]
    emotions = te.get_emotion(tweet_text)
    print(emotions)
    main_emotion = max(emotions, key=emotions.get)
    meme_picture = get_random_meme_picture_for_emotion(main_emotion)
    first_part, second_part = split_tweet(tweet_text)
    meme = make_meme(first_part, second_part, meme_picture)
    meme.save("my_meme.png")