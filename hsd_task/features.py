import io
import logging
import pickle
from os import mkdir
from os.path import join, exists

import numpy as np

from hate_speech.settings import BASE_DIR, all_properties
from hate_speech_detection.models import Feature, Dataset, Tweet

logger = logging.getLogger(__name__)


class AbstractFeature:
    resources_folder = "resources"
    features_folder = "features"
    path_to_features = join(BASE_DIR, resources_folder, features_folder)

    def __init__(self):
        if not exists(self.path_to_features):
            mkdir(self.path_to_features)

    @staticmethod
    def write_to_pickle(vector, path):
        with open(path, "w") as f:
            pickle.dumps(vector, f)


class BowFeature(AbstractFeature):
    hsd_words_folder = "hsd_words"
    bow_folder = "bow"

    def __init__(self):
        super().__init__()
        self.name = "bow"
        self.path_to_bow_folder = join(BASE_DIR, self.resources_folder, self.features_folder, self.bow_folder)
        if not exists(self.path_to_bow_folder):
            mkdir(self.path_to_bow_folder)
        self.hate_words_files = {}
        bow_properties = all_properties["features"]["bow"]
        for bow in bow_properties:
            self.hate_words_files[bow["language"]] = bow["file_name"]

    def load_hate_words(self, filename):
        path_to_file = join(BASE_DIR, self.resources_folder, self.hsd_words_folder, filename)
        with open(path_to_file, "r") as f:
            lines = f.readlines()
            final_lines = []
            for line in lines:
                final_lines.append(line.lower())
            return set(final_lines)

    def create_bow_features(self):
        for language in self.hate_words_files.keys():
            hate_words = self.load_hate_words(self.hate_words_files[language])
            datasets = Dataset.objects.filter(language=language)
            for dataset in datasets:
                dataset_path = join(self.path_to_bow_folder, dataset.name)
                if not exists(dataset_path):
                    mkdir(dataset_path)
                tweets = Tweet.objects.filter(dataset=dataset)
                bow_vectors = {}
                for tweet in tweets:
                    bow_vector = self.create_feature_from_text(hate_words=hate_words, tweet=tweet)
                    bow_vectors[tweet.id] = bow_vector
                feature = Feature()
                feature.name = self.name
                feature.dataset = dataset
                feature.folder_path = dataset_path
                feature.filename = "bow_{}".format(dataset.name)
                feature.save()
                path_to_file = join(dataset_path, feature.filename)
                self.write_to_pickle(bow_vectors, path_to_file)

    @staticmethod
    def create_feature_from_text(hate_words, tweet):
        bow_vector = np.zeros(len(hate_words))
        list_hate_words = list(hate_words)
        for idx, word in enumerate(list_hate_words):
            if word in tweet.preprocessed_text:
                bow_vector[idx] = 1
        return bow_vector


class WordEmbeddings(AbstractFeature):
    embeddings_folder = "embeddings"

    def __init__(self):
        super().__init__()
        self.name = "embeddings"
        self.path_to_embeddings = join(BASE_DIR, self.resources_folder, self.features_folder, self.embeddings_folder)
        embeddings_properties = all_properties["features"]["embeddings"]
        self.embeddings = {}
        for embedding in embeddings_properties:
            self.embeddings[embedding["language"]] = embedding["file_name"]

    def _load_vectors(self, language, filename):
        path_to_file = join(BASE_DIR, self.resources_folder, self.embeddings_folder, language, filename)
        fin = io.open(path_to_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        logger.debug("Loaded dataset has {} words and vectors with dimension {}".format(n, d))
        data = {}
        for line in fin:
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])
        return data

    def create_embedding_features(self):
        for language, filename in self.embeddings.items():
            word_embeddings = self._load_vectors(language=language, filename=filename)
            datasets = Dataset.objects.filter(language=language)
            for dataset in datasets:
                dataset_path = join(self.path_to_embeddings, dataset)
                tweets = Tweet.objects.filter(dataset=dataset)
                all_vectors = {}
                for tweet in tweets:
                    vectors = []
                    words = tweet.preprocessed_text.split(" ")
                    for word in words:
                        if word in word_embeddings.keys():
                            vectors.append(word_embeddings[word])
                    vectors = np.asarray(vectors)
                    vectors = np.mean(vectors, axis=1)
                    all_vectors[tweet.id] = vectors
                feature = Feature()
                feature.name = self.name
                feature.dataset = dataset
                feature.folder_path = dataset_path
                feature.filename = "embeddings_{}.pickle".format(dataset.name)
                feature.save()
                self.write_to_pickle(all_vectors, join(dataset_path, feature.filename))
