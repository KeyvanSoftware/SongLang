from langdetect import detect
from collections import defaultdict

songs_by_language = defaultdict(list) 

def detect_language(text):
    try:
        return detect(text)
    except:
        return None


def group_by_language(language, uri):
    if language != 'en':
        songs_by_language[language].append(uri)
