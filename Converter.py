import re


class Converter:
    def __init__(self):
        self.ver_en = "livros/3_musk_en.txt"
        self.ver_fr = "livros/3_musk_fr.txt"

    """função que transforma os ficheiros todos para lowercase"""
    def big2small(self):
        with open(self.ver_en, "r", encoding="utf-8") as en:
            with open("livros/3_musk_en_lower.txt", "w", encoding="utf-8") as EN:
                for line in en:
                    strip = line.rstrip("\n")
                    split = strip.split(" ")
                    new_line = ""
                    for word in split:
                        new_line += re.sub('[^A-Za-z0-9]+', '', word)
                        new_line += " "
                    EN.write(new_line.lower() + "\n")

        with open(self.ver_fr, "r", encoding="utf-8") as fr:
            with open("livros/3_musk_fr_lower.txt", "w", encoding="utf-8") as FR:
                for line in fr:
                    strip = line.rstrip("\n")
                    split = strip.split(" ")
                    new_line = ""
                    for word in split:
                        new_line += re.sub('[^A-Za-z0-9]+', '', word)
                        new_line += " "
                    FR.write(new_line.lower() + "\n")
