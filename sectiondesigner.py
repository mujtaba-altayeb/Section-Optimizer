from fitnessfunc import design_section, brands
import numpy as np


class GA:
    def __init__(self, gk, qk, span, cover, b_range, h_range):
        self.pop_size = 100  # population size
        self.p_cross_rate = 0.4  # mating probability (DNA crossover)
        self.p_mutation = 0.01  # mutation probability
        self.gens = 100

        self.gk = gk
        self.qk = qk
        self.span = span
        self.cover = cover
        self.b_range = b_range
        self.h_range = h_range

    def get_best_prices(self, candidate):
        cost, n_bars_t, n_bars_c = design_section(self.gk, self.qk,
                                                  self.span,
                                                  candidate["b"],
                                                  candidate["h"],
                                                  self.cover,
                                                  candidate["Ast_dia"],
                                                  candidate["Asc_dia"],
                                                  candidate["fcu"],
                                                  candidate["fy"],
                                                  candidate["brand"])

        details = {
            "Cost": cost,
            "b": candidate["b"],
            "h": candidate["h"],
            "Selected brand": brands[candidate["brand"]],
            "tension bars diameter": candidate["Ast_dia"],
            "compression bars diameter": candidate["Asc_dia"],
            "number of tension bars": n_bars_t,
            "number of compression bars": n_bars_c,
            "Cover": self.cover,
        }
        return details

    def f(self, DNA):
        cost, n_bars_t, n_bars_c = design_section(self.gk, self.qk,
                                                  self.span,
                                                  DNA["b"],
                                                  DNA["h"],
                                                  self.cover,
                                                  DNA["Ast_dia"],
                                                  DNA["Asc_dia"],
                                                  DNA["fcu"],
                                                  DNA["fy"],
                                                  DNA["brand"])

        fitness = np.exp(1/cost)
        return fitness

    def populate(self, pop_size):
        pop = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
        for sample in range(pop_size - 1):
            dna = {"b": np.random.randint(self.b_range[0], self.b_range[1]),
                   "h": np.random.randint(self.h_range[0], self.h_range[1]),
                   "Ast_dia": np.random.choice([16, 20, 25]),
                   "Asc_dia": np.random.choice([16, 20, 25]),
                   "fcu": 30,
                   "fy": 500,
                   "brand": np.random.randint(0, 5),
                   }
            fitness = self.f(dna)
            dna["fitness"] = fitness
            dna = np.array(
                [[dna["b"], dna["h"], dna["Ast_dia"], dna["Asc_dia"], dna["fcu"], dna["fy"], dna["brand"],
                  dna["fitness"]]])
            pop = np.append(pop, dna, axis=0)
        return pop

    def select(self, population, population_size):
        fitness = population[:, -1]
        idx = np.random.choice(np.arange(
            population_size), size=population_size, replace=True, p=fitness / fitness.sum())
        return population[idx]

    def crossover(self, parent, pop):  # mating process (genes crossover)
        if np.random.rand() < self.p_cross_rate:
            # select another individual from pop
            i_ = np.random.randint(0, self.pop_size, size=1)
            cross_points = np.random.randint(0, 2, size=pop[0].size).astype(
                np.bool)  # choose crossover points
            # mating and produce one child
            parent[cross_points] = pop[i_, cross_points]
        return parent

    def mutate(self):
        if np.random.rand() < self.p_mutation:
            mutation = {"b": np.random.randint(self.b_range[0], self.b_range[1]),
                        "h": np.random.randint(self.h_range[0], self.h_range[1]),
                        "Ast_dia": np.random.choice([16, 20, 25]),
                        "Asc_dia": np.random.choice([16, 20, 25]),
                        "fcu": 30,
                        "fy": 500,
                        "brand": np.random.randint(0, 5)}
            fitness = self.f(mutation)
            mutation["fitness"] = fitness
            mutated_dna = np.array([[mutation["b"], mutation["h"],
                                     mutation["Ast_dia"], mutation["Asc_dia"],
                                     mutation["fcu"], mutation["fy"],
                                     mutation["brand"], mutation["fitness"]]])
            return mutated_dna

    def RunGA(self):
        pop = self.populate(self.pop_size)
        for _ in range(self.gens):
            fittest = self.select(pop, self.pop_size)
            for dna in fittest:
                child = self.crossover(dna, pop)
                child = self.mutate()
                dna = child
            best = fittest[np.argmax(fittest[:, -1])]
            print(f"Best DNA: ", best)
        best_candidate = {"b": best[0],
                          "h": best[1],
                          "Ast_dia": best[2],
                          "Asc_dia": best[3],
                          "fcu": best[4],
                          "fy": best[5],
                          "brand": int(best[6]),
                          "fitness": best[7]}

        best_section = self.get_best_prices(best_candidate)

        list_of_fittest = []

        for element in fittest:
            dictioned_element = {"b": element[0],
                                 "h": element[1],
                                 "Ast_dia": element[2],
                                 "Asc_dia": element[3],
                                 "fcu": element[4],
                                 "fy": element[5],
                                 "brand": int(element[6]),
                                 "fitness": element[7]}

            con_element = self.get_best_prices(dictioned_element)

            list_of_fittest.append(con_element)

        return best_section, list_of_fittest
