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
            pickle.dump(vector, f)


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

    def create_bow_features(self, Dataset, Tweet, Feature):
        for language in self.hate_words_files.keys():
            if language != "english":
                continue
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


def generate_features(apps, schema_editor):
    Dataset = apps.get_model("hate_speech_detection", "Dataset")
    Tweet = apps.get_model("hate_speech_detection", "Tweet")
    Feature = apps.get_model("hate_speech_detection", "Feature")
    bow_feature = BowFeature()
    bow_feature.create_bow_features(Dataset=Dataset, Tweet=Tweet, Feature=Feature)


class Migration(migrations.Migration):
    dependencies = [
        ("hate_speech_detection", "0003_auto_preprocess_tweets")
    ]

    operations = [
        migrations.RunPython(generate_features),
    ]
