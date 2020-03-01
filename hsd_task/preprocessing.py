from os.path import join
import re
import string

from hate_speech.settings import BASE_DIR, all_properties
from hate_speech_detection.models import Tweet


class Preprocessor:
    resources_folder = "resources"
    stopwords_folder = "stopwords"
    stopwords_file = "stopwords.txt"

    def __init__(self):
        self.stopwords = set(self.load_stopwords())
        self.remove_stopwords = all_properties["preprocessing"]["remove_stopwords"]
        self.punct_digit_to_space = str.maketrans(string.punctuation + string.digits,
                                                  " " * len(string.punctuation + string.digits))

    def load_stopwords(self):
        path_to_file = join(BASE_DIR, self.resources_folder, self.stopwords_folder, self.stopwords_file)
        with open(path_to_file, "r") as f:
            lines = f.readlines()
            final_lines = []
            for line in lines:
                final_lines.append(line.lower())
            return final_lines

    def preprocess(self):
        tweets = Tweet.objects.all()
        for tweet in tweets:
            if self.remove_stopwords:
                preprocessed_text = self.remove_stopwords(tweet.text)
            else:
                preprocessed_text = tweet.text
            preprocessed_text = preprocessed_text.translate(self.punct_digit_to_space).strip()
            preprocessed_text = re.sub("[ ]+", " ", preprocessed_text)
            tweet.preprocessed_text = preprocessed_text
            tweet.save()

    def remove_stopwords(self, text):
        text_words = text.split()
        text_words = [word for word in text_words if word.lower() not in self.stopwords]
        return ' '.join(text_words)
