from os.path import join

from hate_speech.settings import BASE_DIR


class Feature:
    resources_folder = "resources"
    hsd_words_folder = "hsd_words"
    filename = "hsd_words.txt"


class BowFeature(Feature):

    def __init__(self):
        self.hate_words = set(self.load_hate_words())

    def load_hate_words(self):
        path_to_file = join(BASE_DIR, self.resources_folder, self.hsd_words_folder, self.filename)
        with open(path_to_file, "r") as f:
            lines = f.readlines()
            final_lines = []
            for line in lines:
                final_lines.append(line.lower())
            return final_lines
