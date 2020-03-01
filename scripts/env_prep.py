import gzip
import shutil
import json
import zipfile
from os import getcwd, mkdir, remove
from os.path import join, exists, splitext

import wget

import data_import


def setup():
    resources_folder = "resources"
    path_to_resources = join(getcwd(), resources_folder)
    old_datasets_folder = "old_datasets"
    path_to_old_datasets = join(path_to_resources, old_datasets_folder)
    embeddings_folder = "embeddings"
    path_to_embeddings_folder = join(path_to_resources, embeddings_folder)
    conan_pretty_json(join(path_to_old_datasets, "CONAN.json"), path_to_old_datasets)
    create_datasets()
    properties = load_properties()
    setup_embeddings_files(properties=properties, path_to_embeddings_folder=path_to_embeddings_folder)


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


def load_properties():
    properties_file = join(getcwd(), "hate_speech", "properties.json")
    with open(properties_file, "r") as f:
        return json.loads(f.read())


def setup_embeddings_files(properties, path_to_embeddings_folder):
    embeddings_properties = properties["features"]["embeddings"]
    for embedding in embeddings_properties:
        language_folder = join(path_to_embeddings_folder, embedding["language"])
        if not exists(join(language_folder)):
            mkdir(join(language_folder))
        url = embedding["url"]
        downloaded_file = wget.download(url=url, out=language_folder)
        path_to_downloaded_file = join(language_folder, downloaded_file)
        if downloaded_file.endswith("zip"):
            with zipfile.ZipFile(path_to_downloaded_file, 'r') as zip_ref:
                zip_ref.extractall(language_folder)
            remove(path_to_downloaded_file)
        elif downloaded_file.endswith("gz"):
            filename, ext = splitext(path_to_downloaded_file)
            with gzip.open(path_to_downloaded_file, 'r') as f_in, open(filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            remove(downloaded_file)


if __name__ == '__main__':
    setup()
