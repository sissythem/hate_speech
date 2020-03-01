# Generated by Django 3.0.3 on 2020-03-01 11:18

import io
import pickle
from os import mkdir
from os.path import join, exists

import numpy as np
from django.db import migrations

from hate_speech.settings import BASE_DIR, all_properties


class AbstractFeature:
    resources_folder = "resources"
    features_folder = "features"
    path_to_features = join(BASE_DIR, resources_folder, features_folder)

    def __init__(self):
        if not exists(self.path_to_features):
            mkdir(self.path_to_features)

    @staticmethod
    def write_to_pickle(vector, path):
        with open(path, "wb") as f:
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

    def create_bow_features(self, Dataset, Tweet, Feature):
        for language in self.hate_words_files.keys():
            hate_words = self._load_hate_words(self.hate_words_files[language])
            datasets = Dataset.objects.filter(language=language)
            for dataset in datasets:
                dataset_path = join(self.path_to_bow_folder, dataset.name)
                if not exists(dataset_path):
                    mkdir(dataset_path)
                tweets = Tweet.objects.filter(dataset=dataset)
                for tweet in tweets:
                    self._create_feature_from_text(Feature=Feature, hate_words=hate_words, tweet=tweet,
                                                   folder_path=dataset_path)

    def _load_hate_words(self, filename):
        path_to_file = join(BASE_DIR, self.resources_folder, self.hsd_words_folder, filename)
        with open(path_to_file, "r") as f:
            lines = f.readlines()
            final_lines = []
            for line in lines:
                final_lines.append(line.lower())
            return set(final_lines)

    def _create_feature_from_text(self, Feature, hate_words, tweet, folder_path):
        bow_vector = np.zeros(len(hate_words))
        list_hate_words = list(hate_words)
        for idx, word in enumerate(list_hate_words):
            if word in tweet.preprocessed_text:
                bow_vector[idx] = 1
        feature = Feature()
        feature.name = self.name
        feature.tweet = tweet
        feature.folder_path = folder_path
        feature.filename = "bow_{}".format(tweet.id)
        feature.save()
        path_to_file = join(folder_path, feature.filename)
        self.write_to_pickle(bow_vector, path_to_file)


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

    def create_embedding_features(self, Dataset, Tweet, Feature):
        for language, filename in self.embeddings.items():
            word_embeddings = self._load_vectors(language=language, filename=filename)
            datasets = Dataset.objects.filter(language=language)
            for dataset in datasets:
                dataset_path = join(self.path_to_embeddings, dataset)
                tweets = Tweet.objects.filter(dataset=dataset)
                for tweet in tweets:
                    vectors = []
                    words = tweet.preprocessed_text.split(" ")
                    for word in words:
                        if word in word_embeddings.keys():
                            vectors.append(word_embeddings[word])
                    vectors = np.asarray(vectors)
                    vectors = np.mean(vectors, axis=1)
                    feature = Feature()
                    feature.name = self.name
                    feature.tweet = tweet
                    feature.folder_path = dataset_path
                    feature.filename = "embeddings_{}.pickle".format(tweet.id)
                    feature.save()
                    self.write_to_pickle(vectors, join(dataset_path, feature.filename))

    def _load_vectors(self, language, filename):
        path_to_file = join(BASE_DIR, self.resources_folder, self.embeddings_folder, language, filename)
        fin = io.open(path_to_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
        n, d = map(int, fin.readline().split())
        print("Loaded dataset has {} words and vectors with dimension {}".format(n, d))
        data = {}
        for line in fin:
            tokens = line.rstrip().split(' ')
            data[tokens[0]] = map(float, tokens[1:])
        return data


def generate_features(apps, schema_editor):
    Dataset = apps.get_model("hate_speech_detection", "Dataset")
    Tweet = apps.get_model("hate_speech_detection", "Tweet")
    Feature = apps.get_model("hate_speech_detection", "Feature")
    bow_feature = BowFeature()
    bow_feature.create_bow_features(Dataset=Dataset, Tweet=Tweet, Feature=Feature)
    embeddings_feature = WordEmbeddings()
    embeddings_feature.create_embedding_features(Dataset=Dataset, Tweet=Tweet, Feature=Feature)


class Migration(migrations.Migration):
    dependencies = [
        ("hate_speech_detection", "0003_auto_preprocess_tweets")
    ]

    operations = [
        migrations.RunPython(generate_features),
    ]
