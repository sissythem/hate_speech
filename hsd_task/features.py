import io
from os.path import join

import numpy as np
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist, MultipleObjectsReturned

from hate_speech.settings import BASE_DIR
from hate_speech_detection.models import Feature, Dataset


class AbstractFeature:
    resources_folder = "resources"


class BowFeature(AbstractFeature):
    hsd_words_folder = "hsd_words"
    filename = "hsd_words.txt"

    def __init__(self):
        self.name = "bow"
        self.hate_words = set(self.load_hate_words())

    def load_hate_words(self):
        path_to_file = join(BASE_DIR, self.resources_folder, self.hsd_words_folder, self.filename)
        with open(path_to_file, "r") as f:
            lines = f.readlines()
            final_lines = []
            for line in lines:
                final_lines.append(line.lower())
            return final_lines

    def create_feature_from_text(self, tweet):
        bow_vector = np.zeros(len(self.hate_words))
        list_hate_words = list(self.hate_words)
        for idx, word in enumerate(list_hate_words):
            if word in tweet.text:
                bow_vector[idx] = 1
        feature = Feature()
        feature.name = self.name
        feature.tweet = tweet
        feature.save()


class WordEmbeddings(AbstractFeature):
    embeddings_folder = "embeddings"
    embedding_files = {"english": "", "french": "", "german": "", "italian": ""}

    def __init__(self):
        self.name = "embeddings"
        try:
            datasets = Dataset.objects.all()
            self.languages = []
            self.embeddings = {}
            if datasets:
                for dataset in datasets:
                    self.languages.append(dataset.language)
            self.languages = list(set(self.languages))
            for language in self.languages:
                self.embeddings[language] = self.load_vectors(language=language)
        except (EmptyResultSet, ObjectDoesNotExist, MultipleObjectsReturned, Exception):
            pass

    @staticmethod
    def load_vectors(language):
        fin = io.open(file_name, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        data = {}
        for line in fin:
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])
        return data
