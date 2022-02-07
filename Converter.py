import re


class Converter:
    def __init__(self, path_to_files):
        self.path_to_files = path_to_files

    """função que transforma os ficheiros todos para lowercase"""
    def big2small(self):
        with open(self.path_to_files + "/3_musk_en.txt", "r", encoding="utf-8") as en:
            with open("livros/3_musk_en_lower.txt", "w", encoding="utf-8") as EN:
                for line in en:
                    strip = line.rstrip("\n")
                    split = strip.split(" ")
                    new_line = ""
                    for word in split:
                        new_line += re.sub('[^A-Za-z0-9]+', '', word)
                        new_line += " "
                    EN.write(new_line.lower() + "\n")

        with open(self.path_to_files + "/3_musk_fr.txt", "r", encoding="utf-8") as fr:
            with open("livros/3_musk_fr_lower.txt", "w", encoding="utf-8") as FR:
                for line in fr:
                    strip = line.rstrip("\n")
                    split = strip.split(" ")
                    new_line = ""
                    for word in split:
                        new_line += re.sub('[^A-Za-z0-9]+', '', word)
                        new_line += " "
                    FR.write(new_line.lower() + "\n")
