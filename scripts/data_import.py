import json
import os
from os import getcwd
from os.path import join, exists

import pandas as pd

datasets_folder = join(getcwd(), "resources", "datasets")
old_datasets_folder = join(getcwd(), "resources", "old_datasets")
fox_news_file = "fox_news.json"
hate_speech_dataset_filename = "hate_speech_dataset.json"
label_names = ["noHate", "hate"]


def read_json_csv(filename, num_labels, labels, language):
    if exists(join(datasets_folder, filename)):
        return
    print("Reading and converting fox news dataset")
    with open(join(old_datasets_folder, filename), 'r') as f:
        lines = f.readlines()
    try:
        train = []
        for line in lines:
            train_dat = {}
            line_dict = json.loads(line)
            train_dat["text"] = line_dict["text"]
            train_dat["labels"] = []
            train_dat["labels"].append(line_dict["label"])
            train.append(train_dat)
        final_dict = create_software_dict(train, num_labels, labels, language)
        with open(join(datasets_folder, filename), 'w') as f:
            json.dump(final_dict, f)
    except Exception as e:
        print(e)


def txt_files_to_json(folder, annotations_file, data_folder, filename, labels, language):
    if exists(join(datasets_folder, filename)):
        return
    try:
        old_folder = join(old_datasets_folder, folder)
        annotations_file = join(old_folder, annotations_file)
        annotations = pd.read_csv(annotations_file)
        data_folder = join(old_folder, data_folder)
        train = []
        for file in os.listdir(data_folder):
            train_dat = {}
            with open(join(data_folder, file), 'r') as f:
                lines = f.readlines()
            current_filename = file.replace(".txt", "")
            try:
                file_label = annotations[annotations["file_id"] == current_filename]["label"].values[0]
                train_dat["text"] = lines[0]
                train_dat["labels"] = []
                train_dat["labels"].append(labels.index(file_label))
                train.append(train_dat)
            except Exception as e:
                print("Label for file {} not found {}".format(file, e))
                continue
        final_dict = create_software_dict(train, len(labels), labels, language)
        with open(join(datasets_folder, filename), 'w') as f:
            json.dump(final_dict, f)
    except (FileNotFoundError, Exception):
        pass
        # logger.error(e)


def german_dataset_import(filename_import, filename_out, language):
    if exists(join(datasets_folder, filename_out)):
        return
    try:
        dataset = pd.read_csv(join(old_datasets_folder, filename_import))
        train = []
        for index, row in dataset.iterrows():
            train_dat = {"text": row["Tweet"], "labels": []}
            if row["Exp1"] == row["Exp2"]:
                if row["Exp1"].strip() == "YES":
                    train_dat["labels"].append(1)
                else:
                    train_dat["labels"].append(0)
            else:
                train_dat["labels"].append(1) if row["Rating"] >= 3 else train_dat["labels"].append(0)
            train.append(train_dat)
        final_dict = create_software_dict(train, len(label_names), label_names, language)
        with open(join(datasets_folder, filename_out), 'w') as f:
            json.dump(final_dict, f)
    except Exception as e:
        print(e)


def conan_import(filename_import, filename_out):
    with open(join(old_datasets_folder, filename_import)) as f:
        json_content = json.load(f)
    old_dataset = json_content["conan"]
    train_eng = []
    train_fr = []
    train_it = []
    for datum in old_dataset:
        train_dat_h = {"text": datum["hateSpeech"], "labels": [1]}
        train_dat_nh = {"text": datum["counterSpeech"], "labels": [0]}
        if datum["cn_id"].startswith("EN"):
            train_eng.append(train_dat_h)
            train_eng.append(train_dat_nh)
        else:
            if datum["cn_id"].startswith("FR"):
                if datum["cn_id"].endswith("T1"):
                    train_eng.append(train_dat_h)
                    train_eng.append(train_dat_nh)
                else:
                    train_fr.append(train_dat_h)
                    train_fr.append(train_dat_nh)
            elif datum["cn_id"].startswith("IT"):
                if datum["cn_id"].endswith("T1"):
                    train_eng.append(train_dat_h)
                    train_eng.append(train_dat_nh)
                else:
                    train_it.append(train_dat_h)
                    train_it.append(train_dat_nh)
    final_dict_eng = create_software_dict(train_eng, 2, label_names, "english")
    final_dict_fr = create_software_dict(train_fr, 2, label_names, "french")
    final_dict_it = create_software_dict(train_it, 2, label_names, "italian")

    output_file_eng = open(join(datasets_folder, filename_out + "_eng"), "w")
    output_file_fr = open(join(datasets_folder, filename_out + "_fr"), "w")
    output_file_it = open(join(datasets_folder, filename_out + "_it"), "w")

    output_file_eng.write(json.dumps(final_dict_eng, indent=4, sort_keys=True))
    output_file_fr.write(json.dumps(final_dict_fr, indent=4, sort_keys=True))
    output_file_it.write(json.dumps(final_dict_it, indent=4, sort_keys=True))

    output_file_eng.close()
    output_file_fr.close()
    output_file_it.close()


def create_software_dict(train, num_labels, labels, language):
    """
        Expected format in the yml config:
        name: path/to/dataset_name.json
        In the above path, define dataset json as:
        {
            data:
                train:
                     [
                         {
                            text: "this is the document text"
                            labels: [0,2,3]
                         },
                         ...
                     ],
                test: [...]
            num_labels: 10
            label_names: ['cat', 'dog', ...]
            language: english
        }
    :param train: converted training dataset
    :param num_labels: the number of the labels
    :param labels: the possible labels
    :param language: the language of the dataset
    :return: the produced dictionary containing the above data
    """
    return {"data": {"train": train}, "num_labels": num_labels, "label_names": labels,
            "language": language}
