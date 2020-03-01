import json
from os import listdir
from os.path import join

from django.apps import AppConfig
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist, MultipleObjectsReturned

from hate_speech_detection.models import Dataset, Tweet
from hate_speech.settings import BASE_DIR


class HateSpeechDetectionConfig(AppConfig):
    name = 'hate_speech_detection'
    resources_folder = "resources"
    datasets_folder_name = "datasets"
    datasets_folder = join(BASE_DIR, resources_folder, datasets_folder_name)

    def ready(self):
        try:
            datasets = Dataset.objects.all()
            if not datasets:
                self.save_tweets()
        except (EmptyResultSet, ObjectDoesNotExist, MultipleObjectsReturned, Exception):
            self.save_tweets()

    def save_tweets(self):
        for file in listdir(self.datasets_folder):
            file_path = join(self.datasets_folder, file)
            with open(file_path, "r") as f:
                content = json.loads(f.read())
            dataset = Dataset()
            dataset.num_labels = content["num_labels"]
            dataset.language = content["language"]
            for i in range(dataset.num_labels):
                if i == 0:
                    dataset.label1 = content["label_names"][i]
                elif i == 1:
                    dataset.label2 = content["label_names"][i]
            dataset.save()
            for datum in content["data"]["train"]:
                tweet = Tweet()
                tweet.dataset = dataset
                tweet.text = datum["text"]
                tweet.label = datum["label"][0]
                tweet.save()
