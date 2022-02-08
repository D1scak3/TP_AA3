from matplotlib import pyplot as plt

from count_min_sketch import CountMinSketch


class Counter:
    def __init__(self, conf_path=None, min_m=1000, max_m=20000, min_d=5, max_d=20):
        self.min_m = min_m
        self.max_m = max_m
        self.min_d = min_d
        self.max_d = max_d

        self.exact_en = {}
        self.exact_fr = {}
        if conf_path is not None:
            self.conf_path = conf_path
            self.cms_en = self.create_cms(conf_path)
            self.cms_fr = self.create_cms(conf_path)
        else:
            self.conf_path = None
            self.cms_en = None
            self.cms_fr = None

    def create_cms(self, path):
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

    def count_en(self, exact, cms):
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

    def count_fr(self, exact, cms):
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

    def calculate_result(self, exact, cms):
        over_estimates = []
        exact_counts = 0
        cms_counts = 0

        for word in exact:
            exact_count = exact[word]
            cms_count = cms.query(word)
            exact_counts += exact_count
            cms_counts += cms_count
            err = cms_count - exact_count
            if err > 0:
                over_estimates.append(err)

        if len(over_estimates) > 0:
            over_estimate_mean = float(sum(over_estimates) / len(over_estimates))
        else:
            overe_estimate_mean = 0

        return (exact_counts, cms_counts, len(over_estimates), over_estimate_mean)

    def create_m_variation_graphs(self,variable_attribute_results, cms, language):
        # count variation
        figure = plt.figure(num=1, figsize=(16, 9))
        plt.xlabel("m")
        plt.ylabel("Contagens")
        plt.title(f"Variação das contagens consoante m, para d={cms.d}")

        m_variations = []
        contagens = []
        for x in variable_attribute_results:
            m_variations.append(x[0])  # m(valores do eixo x)
            contagens.append(x[1])  # cms_counts(valores do eixo y)

        plt.bar(m_variations, contagens, color="b", width=0.4, edgecolor="grey",
                label="Quantidade de contagens do Count-Min Sketch")
        plt.axhline(y=variable_attribute_results[0][0], color="r", linestyle="-",
                    label="Quantidade de contagens exatas")

        # plt.legend("d:", cms.d)

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
            medias.append(x[3])

        plt.bar(m_variations, medias, color="g", width=0.4, edgecolor="grey", label="Médias das sobre estimativas")
        # plt.legend("d:", cms.d)

        plt.savefig("./results/" + language + "_m_mean_variation.png")
        plt.close(figure)

    def create_d_variation_graphs(self, variable_attribute_results, cms, language):
        # count variation
        figure = plt.figure(num=1, figsize=(16, 9))
        plt.xlabel("d")
        plt.ylabel("Contagens")
        plt.title(f"Variação das contagens consoante d, para m={cms.m}")

        d_variations = []
        contagens = []
        for x in variable_attribute_results:
            d_variations.append(x[1])  # d(valores do eixo x)
            contagens.append(x[1])  # cms_counts(valores do eixo y)

        plt.bar(d_variations, contagens, color="b", width=0.1, edgecolor="grey",
                label="Quantidade de contagens do Count-Min Sketch")
        plt.axhline(y=variable_attribute_results[0][0], color="r", linestyle="-",
                    label="Quantidade de contagens exatas")

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
            medias.append(x[3])

        plt.bar(d_variations, medias, color="g", width=0.1, edgecolor="grey", label="Médias das sobre estimativas")
        # plt.legend("d:", cms.d)

        plt.savefig("./results/" + language + "_d_mean_variation.png")
        plt.close(figure)

    def count_words(self):
        print("A contar palavras...")

        # fazer grafos com variação das caraterísticas
        # if self.cms_en is None and self.cms_fr is None:  # não possui path to cms.conf
            # resultados da variação do m, com d=min_d
        var_m_en_res = []
        var_m_fr_res = []
        for m in range(self.min_m, self.max_m, 1000):
            en_cms = CountMinSketch(m=m, d=self.min_d)
            fr_cms = CountMinSketch(m=m, d=self.min_d)
            self.count_en(self.exact_en, self.en_cms)
            self.count_fr(self.exact_fr, self.fr_cms)
            var_m_en_res.append(self.calculate_result(self.exact_en, self.en_cms))
            var_m_fr_res.append(self.calculate_result(self.exact_fr, self.fr_cms))
            self.exact_en.clear()
            self.exact_fr.clear()

        self.create_m_variation_graphs(var_m_en_res, self.en_cms, "EN")
        self.create_m_variation_graphs(var_m_fr_res, self.fr_cms, "FR")

        # resultados da variação do d, com m=min_d
        var_d_en_res = []
        var_d_fr_res = []
        for d in range(self.min_d, self.max_d + 1, 1):
            en_cms = CountMinSketch(m=self.min_m, d=d)
            fr_cms = CountMinSketch(m=self.min_m, d=d)
            self.count_en(self.exact_en, en_cms)
            self.count_fr(self.exact_fr, fr_cms)
            var_d_en_res.append(self.calculate_result(self.exact_en, en_cms))
            var_d_fr_res.append(self.calculate_result(self.exact_fr, fr_cms))
            self.exact_en.clear()
            self.exact_fr.clear()

        self.create_d_variation_graphs(var_d_en_res, self.en_cms, "EN")
        self.create_d_variation_graphs(var_d_fr_res, self.fr_cms, "FR")

        # else:  # possui path para o cms.conf
        #     en_cms = self.create_cms(self.conf_path)
        #     fr_cms = self.create_cms(self.conf_path)
        #
        #     self.count_en(self.exact_en, en_cms)
        #     self.count_fr(self.exact_fr, fr_cms)
        #
        #     self.calculate_result(self.exact_en, en_cms)
        #     self.calculate_result(self.exact_fr, fr_cms)
        #
        #     self.create

