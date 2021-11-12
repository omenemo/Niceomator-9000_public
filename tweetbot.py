
# https://docs.tweepy.org/en/stable/getting_started.html#introduction
# Example: https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/twitter-data-in-python/

"""

# Create twitter account
# Potentially apply for developer/academic status

# In the command line:

pip install tweepy
pip install spacy spacy_langdetect 
python3 -m spacy download en_core_web_sm
pip install torch transformers
pip install pysentimiento

"""

# Libraries

import os
import tweepy
import random
import datetime
from os import listdir
from os.path import isfile, join
from memegenerator import make_meme
import emotion_detection
from language_detection import LanugageDetector
from stance_detection import StanceDetection

################################################################################

# VARIABLES
memes_folder = "meme_folder"    # Folder with memes

language = "en"                 # Languge to search for
language_min_score = 0.1        # Minimum anger score

respond_to_ids = False        # Whether to reply to id's (cannot be true at the same time as respont_to_tags)
ids_to_reply_to = {
    
    "1456336025001897988": "climate_deniers",
    "1424365361110163467": "climate_deniers",
    "1166713131856347138": "climate_deniers",
    "1181632884056231936": "climate_deniers",
    "1124097989730025472": "climate_deniers"

}

respont_to_tags = True        # Whether to respond to tweets where niceomator was tagged (cannot be true at the same time as respond_to_ids)
respond_tweets = 5              # Amount of other tweet to which to answer if respont_to_tags == False
emotion_of_interest = "anger"   # Emotions to which to answer
search_tweets = 100             # Amount of tweets to search for
since_X_min = 10080             # Last X minutes to search tweets for
keyword = "flat_earth"          # Which keyword to search for - if None is random
reply_to_tweet = True           # Whether to reply to the tweet

bearer_token= 'xxx'
consumer_key= 'xxx' #(api key)
consumer_secret= 'xxx' #(api secret key)
access_token= 'xxx' #(access token)
access_token_secret= 'xxx' #(access token secret)

emotion_detection_method = "deep_learning_2"  # Method used for emotion detection    

reply_text = "I HAVE DETECTED SOME HATEFUL BEHAVIOUR AND TURNED YOUR TWEET INTO SOMETHING BEAUTIFUL. HAVE A SWEET DAY! #IHAVEREGRETSDOYOU"   

################################################################################

assert(not(respont_to_tags and respond_to_ids)), "Cannot do both - respond_to_tags and respond_to_ids. Execute them one after the other."

# GET EMOTION DETECTION METHOD
METHODS = {
    "text2emotion": emotion_detection.Text2Emotion,
    "deep_learning_1": emotion_detection.DeepLearningModel1,
    "deep_learning_2": emotion_detection.DeepLearningModel2,
}

emotion_of_interest = METHODS[emotion_detection_method].to_label(emotion_of_interest)
emotion_detector = METHODS[emotion_detection_method]()


# GET KEYWORDS AND QUERIES
keywords = []
with open("keywords.txt", "r") as file:
    for line in file.readlines():
        keywords.append(tuple(i.strip() for i in line.split(',', 1)))

if keyword is None:
    keyword_description, search_words = random.choice(keywords)
else:
    tmp = [i for i in keywords if i[0] == keyword]
    assert(len(tmp) == 1), "keyword was not found."
    keyword_description, search_words = tmp[0]

if respont_to_tags:
    search_words = "@niceomator"
    
# LANGUAGE DETECTOR
language_detector = LanugageDetector()


# AUTHENTICATION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# HELPER METHOD
def rep(text):
    return client.search_recent_tweets(query=text)

# CONNECTION
api = tweepy.API(auth)
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

now = datetime.datetime.now(datetime.timezone.utc)
start_time = now - datetime.timedelta(minutes = since_X_min)
tweets = client.search_recent_tweets(query=search_words,
    start_time=start_time, max_results=search_tweets)


# HELPER METHODS
def fullfills_language_requirements(text):
    detected_lang = language_detector.detect_language(text)
    if detected_lang['language'] != language:
        return False
    if detected_lang['score'] < language_min_score:
        return False
    return True

def get_random_meme_picture_for_keyword(keyword):
    mypath = os.path.join(memes_folder, keyword)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))
        and f != ".DS_Store"]
    random_meme_picture = random.choice(onlyfiles)
    random_meme_picture = os.path.join(mypath, random_meme_picture)
    return random_meme_picture

def split_tweet(tweet):
    words = tweet.split(" ")
    middle = int(len(words)/2)
    first_part = " ".join(words[:middle])
    second_part = " ".join(words[middle:])
    return first_part, second_part


# FILTER / ANALYSE / RESPOND TO TWEETS
if tweets.meta['result_count'] != 0:
    tweets = tweets[0]
    
    # Replace by id tweets if true
    if respond_to_ids:
        tweets = [(k, client.get_tweet(id)[0]) for id, k in ids_to_reply_to.items()]
    
    # No filtering on tagged tweets
    if not (respont_to_tags or respond_to_ids):
        
        # Sort out none english tweets
        tweets = [i for i in tweets if fullfills_language_requirements(i.text)]
        
        # TODO: check if include stance detection to some degree
        
        # Get emotions
        tweet_emotions = emotion_detector.predict(tweets)
        
        # Filter out emotions that are not of interest (only tweets where emotion
        # of interest has the highest score)
        tweets = [(emotions, tweet) for emotions, tweet in zip(tweet_emotions, tweets) if
            (max(emotions, key=emotions.get) == emotion_of_interest)]
        
        # Sort tweets and keep a certain number of tweets
        tweets = [(emotions[emotion_of_interest], tweet) for emotions, tweet in tweets]
        tweets.sort(key=lambda x: x[0])

        tweets = [i[1] for i in tweets[-respond_tweets:]]
    
    if len(tweets) == 0:
        print("No tweets...")
        exit(0)
    
    for ind, tweet in enumerate(tweets):
        
        if respond_to_ids:
            keyword_description = tweet[0]
            tweet = tweet[1]
        
        id = tweet.id
        text = tweet.text

        meme_picture = get_random_meme_picture_for_keyword(keyword_description)
        first_part, second_part = split_tweet(text)
        meme = make_meme(first_part, second_part, meme_picture)
        meme_path = f"generated_memes/{id}.png"
        meme.save(meme_path)
        
        # Reply
        if reply_to_tweet:
            media = api.media_upload(meme_path)
            api.update_status(status=reply_text,
                media_ids=[media.media_id], in_reply_to_status_id=id,
                auto_populate_reply_metadata=True)