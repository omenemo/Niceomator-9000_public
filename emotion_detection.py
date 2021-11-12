import text2emotion as te
from pysentimiento import EmotionAnalyzer
from transformers import pipeline
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request


class EmotionDetector():
    
    def __init__(self):
        raise NotImplementedError
    
    def predict(self):
        """ Input list of tweets - returns list of predictions. """
        raise NotImplementedError

    @staticmethod
    def to_label(emotion):
        raise NotImplementedError
    
class Text2Emotion(EmotionDetector):
    
    emotions = ["Happy", "Angry", "Surprise", "Sad", "Fear"]
    
    def __init__(self):
        pass
    
    def predict(self, tweets):
        """ Input list of tweets - returns list of predictions. """
        return [te.get_emotion(tweet.text) for tweet in tweets]

    @staticmethod
    def to_label(emotion):
        if emotion == "anger":
            return "Anger"
        else:
            raise NotImplementedError
        
class DeepLearningModel1(EmotionDetector):
    
    emotions = ["sadness", "anger", "love", "joy", "fear", "surprise"]
    
    def __init__(self):
        self.classifier = pipeline("text-classification",
            model='bhadresh-savani/distilbert-base-uncased-emotion',
            return_all_scores=True)

    
    def predict(self, tweets):
        """ Input list of tweets - returns list of predictions. """
        emotions = self.classifier([tweet.text for tweet in tweets])
        emotions = [{i['label']: i['score'] for i in scores} for scores in emotions]
        return emotions
    
    @staticmethod
    def to_label(emotion):
        if emotion == "anger":
            return "anger"
        else:
            raise NotImplementedError

class DeepLearningModel2(EmotionDetector):
    
    emotions = ["others", "disgust", "anger", "sadness", "joy", "fear", "surprise"]
    
    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzer(lang="en")

    
    def predict(self, tweets):
        """ Input list of tweets - returns list of predictions. """
        return [self.emotion_analyzer.predict(tweet.text).probas for tweet in tweets]

    @staticmethod
    def to_label(emotion):
        if emotion == "anger":
            return "anger"
        else:
            raise NotImplementedError

