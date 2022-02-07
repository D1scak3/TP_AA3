import argparse
import math
import os
import matplotlib
import matplotlib.pyplot as plt

from Converter import Converter
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

    # coisas a analisar
    over_estimates = []
    over_estimate_count = 0  # afetado pelo m(maior m, menos colisões) -> verificar quantidade de erros para o mesmo d
    # se quisermos um erro da quantidade de contagens realizadas baixo(<epsilon) -> aumentar m diminui epsilon

    # afetado pelo d(maior d, menor quantidade de más estimativas) -> verificar média dos erros relativos para o mesmo m
    # se quisermos ter certeza que as contagens são inferiores ou iguais ao erro(% >= 1-delta) -> aumentar d diminui delta
    # certeza(chance) do obtained_max_error não superar o max_error
    certainty = 1 - math.pow(0.5, cms.d)
    # chance de o cms_count <= exact_count * (1 + epsilon)

    # contagens
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
            over_estimate_count += 1
            over_estimates.append(err)

    # maior o m, menor a quantidade de más estimativas em relação à quantidade de palavras
    over_estimate_percent = (over_estimate_count/len(exact.keys())) * 100  # quantidad de más estimativas / quantiade de palavras
    # maior o d, menor a média das más estimativas
    if over_estimate_count > 0:
        over_estimate_mean = float(sum(over_estimates) / over_estimate_count)  # soma das más estimativas / quantidade de más estimativas
    else:
        over_estimate_mean = 0

    print("-----------------------Resultados obtidos " + language + "-----------------------")
    print(f"Caraterísticas do CMS:  m:{cms.m}  d:{cms.d}  delta:{cms.delta}  epsilon:{cms.epsilon}")
    print(f"Contagens exatas: {exact_counts}   Contagens da Count-Min Sketch: {cms_counts} ({cms_counts - exact_counts} adicionais)")
    print(f"Quantidade de palavras: {len(exact.keys())}")
    print(f"Quantidade de palavras sobre estimadas: {over_estimate_count}")
    print(f"Percentagem de sobre estimativas em relação à quantidade de palavras: {over_estimate_percent}%")
    print(f"Médias das sobre estimativas: {over_estimate_mean}")
    print(f"Certeza: {certainty}%")
    # print(f"Quantidade de vezes máxima que cms_count > exact_count * (1+epsilon) **baseado na certeza**: {max_times_cms_over}")
    # print(f"Quantidade de vezes que cms_count > exact_count * (1 + epsilon): {times_cms_over}  Percentagem: {(times_cms_over/amount_of_results) * 100}%")

    return (cms.m, cms.d, cms.delta, cms.epsilon, exact_counts, cms_counts, over_estimate_count, over_estimate_mean)


def write_results(tup, language):
    with open("./results/" + language + "_results.tsv", "a", encoding="utf-8") as file:
        line = ""
        line += str(tup[0])
        for ind, el in enumerate(tup):
            if ind > 0:
                line += "\t"
                line += str(el)
        line += "\n"
        file.write(line)


def create_m_variation_graphs(variable_attribute_results, cms, language):
    # count variation
    figure = plt.figure(num=1, figsize=(16, 9))
    figure.xlabel("m")
    figure.ylabel("Contagens")
    figure.title(f"Variação das contagens consoante m, para d={cms.d}")

    m_variations = []
    contagens = []
    for x in variable_attribute_results:
        m_variations.append(x[0])  # m(valores do eixo x)
        contagens.append(x[5])  # cms_counts(valores do eixo y)

    figure.bar(m_variations, contagens, color="b", width=0.2, edgecolor="grey", label="Quantidade de contagens do Count-Min Sketch")
    figure.axhline(y=variable_attribute_results[0][4], color="r", linestyle="-", label="Quantidade de contagens exatas")

    figure.legend("d:", cms.d)
    # plt.show()
    figure.savefig("./results/" + language + "_m_count_variation.png")
    # figure.close(1)

    # median variation
    figure = plt.figure(num=2, figsize=(16, 9))
    figure.xlabel("m")
    figure.ylabel("Médias")
    figure.title(f"Variação das médias das sobre estimativas consoante m, para d={cms.d}")

    medias = []
    for x in variable_attribute_results:
        medias.append(x[7])

    figure.bar(m_variations, medias, color="g", width=0.2, edgecolor="grey", label="Médias das sobre estimativas")
    figure.legend("d:", cms.d)

    figure.savefig("./results/" + language + "_m_mean_variation.png")


def create_d_variation_graphs(variable_attribute_results, cms, language):
    # todo fazer gráficos em que o d varia
    pass


# módulos
def parse_arguments():
    parser = argparse.ArgumentParser(description='Descrição do programa')
    parser.add_argument('-m', '--mode',
                        help='MODE:\t0 -> converter ficheiros\t1 -> ',
                        required=True)
    parser.add_argument("-f", "--file", help="FILE path até cms.conf (caraterísticas do count-min sketch)", required=False)
    parser.add_argument("-b", "--book", help="FILE path para os livros a converter", required=True)
    return vars(parser.parse_args())


def convert_files(path_to_files):
    print("A converter ficheiros...")
    converter = Converter(path_to_files)
    converter.big2small()


def count_words(path_to_conf=None, min_m=None, max_m=None, min_d=None, max_d=None):
    print("A contar palavras...")

    # cria contadores
    en_exact_counter = {}
    fr_exact_counter = {}
    if path_to_conf is None:
        # resultados da variação do m, com d=min_d
        var_m_en_res = []  # versão inglesa
        var_m_fr_res = []  # versão francesa
        for m in range(min_m, max_m+1):
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
        for d in range(min_d, max_d+1):
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

    else:
        en_cms = create_cms(path_to_conf)
        fr_cms = create_cms(path_to_conf)

        count_en(en_exact_counter, en_cms)
        count_fr(fr_exact_counter, fr_cms)

        calculate_result(en_exact_counter, en_cms, "EN")
        calculate_result(fr_exact_counter, fr_cms, "FR")


if __name__ == "__main__":

    # argument parser
    args = parse_arguments()

    res = int(args["mode"])

    if res == 0:  # converter ficheiros
        convert_files(args["book"])

    elif res == 1:
        count_words(args["file"])

    # elif res == 2:
    #     analise("EN")
    #     analise("FR")

    else:  # opção que não existe
        print("Opção errada.")
        print("A sair...")
        exit()
