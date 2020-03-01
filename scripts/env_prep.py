import json
from os import getcwd
from os.path import join

import data_import


def setup():
    resources_folder = "resources"
    path_to_resources = join(getcwd(), resources_folder)
    old_datasets_folder = "old_datasets"
    path_to_old_datasets = join(path_to_resources, old_datasets_folder)
    conan_pretty_json(join(path_to_old_datasets, "CONAN.json"), path_to_old_datasets)
    create_datasets()


def conan_pretty_json(conan_file, old_datasets):
    with open(conan_file, "r") as f:
        conan_content = json.loads(f.read())
    conan_file_new = "conan.json"
    output_file = open(join(old_datasets, conan_file_new), "w")
    output_file.write(json.dumps(conan_content, indent=4, sort_keys=True))
    output_file.close()


def create_datasets():
    data_import.read_json_csv(data_import.fox_news_file, 2, data_import.label_names, "english")
    data_import.txt_files_to_json("hate-speech-dataset", "annotations_metadata.csv", "all_files",
                                  data_import.hate_speech_dataset_filename, data_import.label_names, "english")
    data_import.german_dataset_import("german.csv", "german.json", "german")
    data_import.conan_import("conan.json", "conan.json")


if __name__ == '__main__':
    setup()
