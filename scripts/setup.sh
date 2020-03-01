#!/bin/bash

cp ./hate_speech/example_properties.json ./hate_speech/properties.json

RESOURCES_FOLDER="resources"
OLD_DATASETS_FOLDER="old_datasets"
DATASETS_FOLDER="datasets"
EMBEDDINGS_FOLDER="embeddings"

mkdir -p "${RESOURCES_FOLDER}"
mkdir -p "${RESOURCES_FOLDER}/${OLD_DATASETS_FOLDER}"
mkdir -p "${RESOURCES_FOLDER}/${DATASETS_FOLDER}"
mkdir -p "${RESOURCES_FOLDER}/${EMBEDDINGS_FOLDER}"
PATH_TO_OLD_DATASETS="${RESOURCES_FOLDER}/${OLD_DATASETS_FOLDER}"

# download german dataset
git clone https://github.com/UCSM-DUE/IWG_hatespeech_public.git
mv IWG_hatespeech_public/german\ hatespeech\ refugees.csv ${PATH_TO_OLD_DATASETS}/german.csv
rm -rf IWG_hatespeech_public

# download fox news dataset
git clone https://github.com/sjtuprog/fox-news-comments.git
mv fox-news-comments/fox-news-comments.json ${PATH_TO_OLD_DATASETS}/fox_news.json
rm -rf fox-news-comments

# download conan dataset
git clone https://github.com/marcoguerini/CONAN.git
mv CONAN/CONAN.json ${PATH_TO_OLD_DATASETS}/
rm -rf CONAN

# download hate-speech-dataset
mkdir -p "${PATH_TO_OLD_DATASETS}/hate-speech-dataset"

git clone https://github.com/aitor-garcia-p/hate-speech-dataset.git
mv hate-speech-dataset/all_files/ ${PATH_TO_OLD_DATASETS}/hate-speech-dataset/
mv hate-speech-dataset/annotations_metadata.csv ${PATH_TO_OLD_DATASETS}/hate-speech-dataset/
rm -rf hate-speech-dataset
