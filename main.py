import argparse
import sys

import openpyxl as openpyxl

from Converter import Converter
from count_min_sketch import CountMinSketch

"""
Nome: Miguel Filipe Rodrigues ALmeida de MAtos fazenda
Nmec: 110877
Curso: Mestrado em Engenharia Informática
Tp3: Most Frequent Words with Count-Min Sketch
"""


# funções de auxílio
def create_cms(path):
    args = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            strip = line.rstrip("\n")
            split = strip.split(" ")
            args[split[0]] = split[1]

    m = int(args["m"])
    d = int(args["d"])
    delta = float(args["delta"])
    epsilon = float(args["epsilon"])

    if m > 0 and d > 0:
        return CountMinSketch(m=m, d=d)
    else:
        return CountMinSketch(delta=delta, epsilon=epsilon)


# funções de contagem
def count_en(exact, cms):
    with open("./livros/3_musk_en_lower.txt", "r", encoding="utf-8") as file:
        for line in file:
            strip = line.rstrip("\n")
            words = strip.split(" ")
            for word in words:
                if word in exact:
                    exact[word] += 1
                else:
                    exact[word] = 1

                cms.update(word, 1)


def count_fr(exact, cms):
    with open("./livros/3_musk_fr_lower.txt", "r", encoding="utf-8") as file:
        for line in file:
            strip = line.rstrip("\n")
            words = strip.split(" ")
            for word in words:
                if word in exact:
                    exact[word] += 1
                else:
                    exact[word] = 1

                cms.update(word, 1)


def save_results(exact, cms, language):
    nome = language + "_" + str(cms.m) + "_" + str(cms.d) + "_" + str(cms.delta) + "_" + str(cms.epsilon)
    rel_error_sum = 0
    with open("./results/" + nome + ".tsv", "w", encoding="utf-8") as file:
        file.write("Words\tExact\tCMS\tAbs_Err\tRel_Err\tRel_Err_Mean\n")
        for item in sorted(exact.items(), key=lambda x: x[0]):
            line = ""
            line += item[0]
            line += "\t"
            line += str(item[1])
            line += "\t"
            line += str(cms.query(item[0]))
            line += "\t"
            line += str(cms.query(item[0]) - item[1])
            line += "\t"
            rel_error_sum += (cms.query(item[0]) - item[1]) / item[1]
            line += str((cms.query(item[0]) - item[1]) / item[1])
            line += "\n"
            file.write(line)

    file = open("./results/" + nome + ".tsv", "r", encoding="utf-8")
    lines = file.readlines()
    line = lines[1].rstrip("\n")
    line += "\t" + str(round(rel_error_sum / len(exact), 5)) + "\n"
    lines[1] = line
    file = open("./results/" + nome + ".tsv", "w", encoding="utf-8")
    file.writelines(lines)
    file.close()


if __name__ == "__main__":

    # argument parser
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-m', '--mode', help='MODE:\t0 -> converter ficheiros\t1 -> exact counting\t2 -> count-min sketch', required=True)
    parser.add_argument("-f", "--file", help="FILE path para as caraterísticas do count-min sketch", required=False)
    args = vars(parser.parse_args())

    res = int(args["mode"])

    if res == 0:  # converter ficheiros
        print("A converter ficheiros...")
        converter = Converter()
        converter.big2small()

    elif res == 1:
        en_exact_counter = {}
        fr_exact_counter = {}
        if args["file"] is None:
            en_cms = CountMinSketch(delta=0.0001, epsilon=0.0001)
            fr_cms = CountMinSketch(delta=0.0001, epsilon=0.0001)

        else:
            en_cms = create_cms(args["file"])
            fr_cms = create_cms(args["file"])

        count_en(en_exact_counter, en_cms)
        count_fr(fr_exact_counter, fr_cms)

        save_results(en_exact_counter, en_cms, "en")
        save_results(fr_exact_counter, fr_cms, "fr")

    else:  # opção que não existe
        print("Opção errada.")
        print("A sair...")
        exit()
