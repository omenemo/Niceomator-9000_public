
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

@Language.factory("language_detector")
def get_lang_detector(nlp, name):
    return LanguageDetector()
         
class LanugageDetector():
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe('language_detector', last=True)
        
    def detect_language(self, text):
        doc = self.nlp(text) 
        detect_language = doc._.language
        return detect_language