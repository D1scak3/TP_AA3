import argparse
import math
import os
import matplotlib
import matplotlib.pyplot as plt

from Converter import Converter
from Counter import Counter
from count_min_sketch import CountMinSketch

"""
Nome: Miguel Filipe Rodrigues ALmeida de MAtos fazenda
Nmec: 110877
Curso: Mestrado em Engenharia Informática
Tp3: Most Frequent Words with Count-Min Sketch
"""


# funções de auxílio
def create_cms(path_to_conf):
    args = {}
    with open(path_to_conf, "r", encoding="utf-8") as file:
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
                if word != "":
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
                if word != "":
                    if word in exact:
                        exact[word] += 1
                    else:
                        exact[word] = 1

                    cms.update(word, 1)


def create_dir_for_counts():
    # cria pasta para resultados
    try:
        print("A criar diretoria para os resultados...")
        parent = os.getcwd()  # diretoria atual
        path = os.path.join(parent, "/results")  # nova diretoria
        os.mkdir(path)  # cria nova diretoria
    except:
        print("Diretoria já existente.")


def save_results(exact, cms, language):
    # escreve info para um tsv
    nome = language + "_" + str(cms.m) + "_" + str(cms.d) + "_" + str(cms.delta) + "_" + str(cms.epsilon)
    rel_error_sum = 0
    with open("./results/" + nome + ".tsv", "w", encoding="utf-8") as file:
        file.write("Words\tExact\tCMS\tAbs_Err\tRel_Err\n")
        for item in sorted(exact.items(), reverse=True, key=lambda x: x[1]):  # escreve ordenadamente por contagem exata
            line = ""
            line += item[0]
            line += "\t"
            line += str(item[1])
            line += "\t"
            line += str(cms.query(item[0]))
            line += "\t"
            line += str(cms.query(item[0]) - item[1])
            line += "\t"
            rel_error_sum += ((cms.query(item[0]) - item[1]) / item[1])
            line += str(round((cms.query(item[0]) - item[1]) / item[1], 5))
            line += "\n"
            file.write(line)


def calculate_result(exact, cms, language):

    over_estimates = []

    exact_counts = 0
    cms_counts = 0

    # percorre contagens
    for word in exact:
        exact_count = exact[word]
        cms_count = cms.query(word)
        exact_counts += exact_count
        cms_counts += cms_count
        err = cms_count - exact_count
        if err > 0:  # se houver erro
            over_estimates.append(err)

    if len(over_estimates) > 0:
        over_estimate_mean = float(sum(over_estimates) / len(over_estimates))
    else:
        over_estimate_mean = 0

    return (cms.m, cms.d, cms.delta, cms.epsilon, exact_counts, cms_counts, len(over_estimates), over_estimate_mean)


# def write_results(tup, language):
#     with open("./results/" + language + "_results.tsv", "a", encoding="utf-8") as file:
#         line = ""
#         line += str(tup[0])
#         for ind, el in enumerate(tup):
#             if ind > 0:
#                 line += "\t"
#                 line += str(el)
#         line += "\n"
#         file.write(line)


def create_m_variation_graphs(variable_attribute_results, cms, language):
    # count variation
    figure = plt.figure(num=1, figsize=(16, 9))
    plt.xlabel("m")
    plt.ylabel("Contagens")
    plt.title(f"Variação das contagens consoante m, para d={cms.d}")

    m_variations = []
    contagens = []
    for x in variable_attribute_results:
        m_variations.append(x[0])  # m(valores do eixo x)
        contagens.append(x[5])  # cms_counts(valores do eixo y)

    plt.bar(m_variations, contagens, color="b", width=0.4, edgecolor="grey", label="Quantidade de contagens do Count-Min Sketch")
    plt.axhline(y=variable_attribute_results[0][4], color="r", linestyle="-", label="Quantidade de contagens exatas")

    # plt.show()
    plt.savefig("./results/" + language + "_m_count_variation.png")
    plt.close(figure)

    # median variation
    figure = plt.figure(num=2, figsize=(16, 9))
    plt.xlabel("m")
    plt.ylabel("Médias")
    plt.title(f"Variação das médias das sobre estimativas consoante m, para d={cms.d}")

    medias = []
    for x in variable_attribute_results:
        medias.append(x[7])

    plt.bar(m_variations, medias, color="g", width=0.4, edgecolor="grey", label="Médias das sobre estimativas")

    plt.savefig("./results/" + language + "_m_mean_variation.png")
    plt.close(figure)


def create_d_variation_graphs(variable_attribute_results, cms, language):
    # count variation
    figure = plt.figure(num=1, figsize=(16, 9))
    plt.xlabel("d")
    plt.ylabel("Contagens")
    plt.title(f"Variação das contagens consoante d, para m={cms.m}")

    d_variations = []
    contagens = []
    for x in variable_attribute_results:
        d_variations.append(x[1])  # d(valores do eixo x)
        contagens.append(x[5])  # cms_counts(valores do eixo y)

    plt.bar(d_variations, contagens, color="b", width=0.1, edgecolor="grey",
            label="Quantidade de contagens do Count-Min Sketch")
    plt.axhline(y=variable_attribute_results[0][4], color="r", linestyle="-", label="Quantidade de contagens exatas")

    # plt.legend("d:", cms.d)

    # plt.show()
    plt.savefig("./results/" + language + "_d_count_variation.png")
    plt.close(figure)

    # median variation
    figure = plt.figure(num=2, figsize=(16, 9))
    plt.xlabel("d")
    plt.ylabel("Médias")
    plt.title(f"Variação das médias das sobre estimativas consoante m, para d={cms.d}")

    medias = []
    for x in variable_attribute_results:
        medias.append(x[7])

    plt.bar(d_variations, medias, color="g", width=0.1, edgecolor="grey", label="Médias das sobre estimativas")

    plt.savefig("./results/" + language + "_d_mean_variation.png")
    plt.close(figure)


# módulos
def parse_arguments():
    parser = argparse.ArgumentParser(description='Descrição do programa')
    parser.add_argument('-m', '--mode',
                        help='MODE:\t0 -> converter ficheiros\t1 -> ',
                        required=True)
    parser.add_argument("-b", "--book", help="FILE path para os livros a converter", required=True)
    return vars(parser.parse_args())


def convert_files(path_to_files):
    print("A converter ficheiros...")
    converter = Converter(path_to_files)
    converter.big2small()


def count_words(min_m=None, max_m=None, min_d=None, max_d=None):
    print("A contar palavras...")

    # cria contadores
    en_exact_counter = {}
    fr_exact_counter = {}

    # resultados da variação do m, com d=min_d
    var_m_en_res = []  # versão inglesa
    var_m_fr_res = []  # versão francesa
    for m in range(min_m, max_m+1, 1000):
        en_cms = CountMinSketch(m=m, d=min_d)
        fr_cms = CountMinSketch(m=m, d=min_d)
        count_en(en_exact_counter, en_cms)
        count_fr(fr_exact_counter, fr_cms)
        var_m_en_res.append(calculate_result(en_exact_counter, en_cms, "EN"))
        var_m_fr_res.append(calculate_result(fr_exact_counter, fr_cms, "FR"))
        en_exact_counter.clear()
        fr_exact_counter.clear()

    create_m_variation_graphs(var_m_en_res, en_cms, "EN")
    create_m_variation_graphs(var_m_fr_res, fr_cms, "FR")

    # resultados da variação do d, com m=min_m
    var_d_en_res = []
    var_d_fr_res = []
    for d in range(min_d, max_d+1, 1):
        en_cms = CountMinSketch(m=min_m, d=d)
        fr_cms = CountMinSketch(m=min_m, d=d)
        count_en(en_exact_counter, en_cms)
        count_fr(fr_exact_counter, fr_cms)
        var_d_en_res.append(calculate_result(en_exact_counter, en_cms, "EN"))
        var_d_fr_res.append(calculate_result(fr_exact_counter, fr_cms, "FR"))
        en_exact_counter.clear()
        fr_exact_counter.clear()

    create_d_variation_graphs(var_d_en_res, en_cms, "EN")
    create_d_variation_graphs(var_d_fr_res, fr_cms, "FR")


if __name__ == "__main__":

    # argument parser
    args = parse_arguments()

    res = int(args["mode"])

    if res == 0:  # converter ficheiros
        convert_files(args["book"])

    elif res == 1:
        # c = Counter()
        # c.count_words()
        count_words(min_m=2000, max_m=20000, min_d=5, max_d=20)

    else:  # opção que não existe
        print("Opção errada.")
        print("A sair...")
        exit()
