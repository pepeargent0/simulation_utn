import math
from random import randint
import argparse
import matplotlib.pyplot as plt


class RouletteSimulation:
    def __init__(self, number_runs, number_rolls, chosen_number):
        self.results = []
        self.number_runs = number_runs
        self.number_rolls = number_rolls
        self.chosen_number = chosen_number
        self.frequency_absolute = 0
        self.average_values = []

    def simulation(self):
        for run in range(self.number_runs):
            current_run = [0] * 37
            for rolls in range(self.number_rolls):
                _key = randint(0, 36)
                if _key == self.chosen_number:
                    self.frequency_absolute += 1
                current_run[_key] += 1
                self.calculate_average_values(current_run, rolls + 1)
            self.results.append(current_run)
        frequency_relative = self.frequency_absolute / (self.number_runs * self.number_rolls)
        return self.results, self.frequency_absolute, frequency_relative

    def calculate_average_values(self, current_run, n):
        vp = sum([i * current_run[i] for i in range(37)]) / sum(current_run)
        vpn = vp / n
        vpe = sum([i * (1 / 36) for i in range(37)])
        self.average_values.append((vp, vpn, vpe))

    def get_frequencies(self):
        frequencies = {'FR': [], 'FRE': [], 'FRN': []}
        for run in self.results:
            total_rolls = sum(run)
            fr = run[self.chosen_number] / total_rolls if self.chosen_number in run else 0
            fre = 1 / 36
            frn = (fre * self.number_runs)
            # dejo este print porque tengo un duda FRN me da mayor que 1 cundo c > 40
            print(f'FRN: {frn} fre: {fre} FR {fr} N: {self.number_runs}')
            frequencies['FR'].append(fr)
            frequencies['FRE'].append(fre)
            frequencies['FRN'].append(frn)
        return frequencies

    def show_fr_fre_frn(self):
        frequencies = self.get_frequencies()
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, self.number_runs + 1), frequencies['FR'], label='FR', marker='o')
        plt.plot(range(1, self.number_runs + 1), frequencies['FRE'], label='FRE', marker='o')
        plt.plot(range(1, self.number_runs + 1), frequencies['FRN'], label='FRN', marker='o')
        plt.xlabel('Número de Corridas')
        plt.ylabel('Valor')
        plt.title('Relación entre FR, FRE y FRN en función del Número de Corridas')
        plt.legend()
        plt.show()

    def calculate_deviation_values(self):
        deviations = []
        for run in self.results:
            n = sum(run)
            mean = sum(i * run[i] for i in range(37)) / n
            deviation = math.sqrt(sum(((i - mean) ** 2) * run[i] for i in range(37)) / n)
            vd = deviation
            vdxn = deviation * n
            vde = math.sqrt((1 / 36) * (1 - 1 / 36))
            deviations.append((vd, vdxn, vde))
        return deviations

    def show_vp_vpe_vpn(self):
        average_values = self.average_values

        vp_values = [vp for vp, _, _ in average_values]
        vpe_values = [vpe for _, vpe, _ in average_values]
        vpn_values = [vpn for _, _, vpn in average_values]

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(vp_values) + 1), vp_values, label='Valor Promedio de las Tiradas', marker='o')
        plt.plot(range(1, len(vpe_values) + 1), vpe_values, label='Valor Promedio Esperado', marker='o')
        plt.plot(range(1, len(vpn_values) + 1), vpn_values, label='Valor Promedio de las Tiradas respecto a N',
                 marker='o')
        plt.xlabel('Iteración de la Simulación')
        plt.ylabel('Valor')
        plt.title('Valores Promedio por Iteración')
        plt.legend()
        plt.grid(True)
        plt.show()

    def show_deviation_values(self):
        deviation_values = self.calculate_deviation_values()

        vd_values = [vd for vd, _, _ in deviation_values]
        vdxn_values = [vdxn for _, vdxn, _ in deviation_values]
        vde_values = [vde for _, _, vde in deviation_values]

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(vd_values) + 1), vd_values, label='Valor del Desvío', marker='o')
        plt.plot(range(1, len(vdxn_values) + 1), vdxn_values, label='Valor del Desvío x N', marker='o')
        plt.plot(range(1, len(vde_values) + 1), vde_values, label='Valor del Desvío Esperado', marker='o')
        plt.xlabel('Corridas')
        plt.ylabel('Valor')
        plt.title('Valores del Desvío por Corrida')
        plt.legend()
        plt.grid(True)
        plt.show()

    def calculate_variance_values(self):
        variances = []
        for run in self.results:
            n = sum(run)
            mean = sum(i * run[i] for i in range(37)) / n
            variance = sum(((i - mean) ** 2) * run[i] for i in range(37)) / n
            vv = variance
            vvxn = variance * self.chosen_number / n if self.chosen_number in run else 0
            vve = (1 / 36) * ((35 / 36) ** 2)
            variances.append((vv, vvxn, vve))
        return variances

    def show_variance_values(self):
        variance_values = self.calculate_variance_values()

        vv_values = [vv for vv, _, _ in variance_values]
        vvxn_values = [vvxn for _, vvxn, _ in variance_values]
        vve_values = [vve for _, _, vve in variance_values]

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(vv_values) + 1), vv_values, label='Valor de la Varianza', marker='o')
        plt.plot(range(1, len(vvxn_values) + 1), vvxn_values, label='Valor de la Varianza por Número', marker='o')
        plt.plot(range(1, len(vve_values) + 1), vve_values, label='Valor de la Varianza Esperada', marker='o')
        plt.xlabel('Corridas')
        plt.ylabel('Valor')
        plt.title('Valores de la Varianza por Corrida')
        plt.legend()
        plt.grid(True)
        plt.show()


parser = argparse.ArgumentParser(description='Simulacion de ruleta')
parser.add_argument('-c', '--numero_corridas', type=int, help='Corridas')
parser.add_argument('-n', '--numero_tiradas', type=int, help='numero de tiradas')
parser.add_argument('-e', '--numero_eleguido', type=int, help='numero de eleguido')

args = parser.parse_args()
number_runs, number_rolls, chosen_number = args.numero_corridas, args.numero_tiradas, args.numero_eleguido

if all(isinstance(arg, int) and arg >= 0 for arg in [number_runs, number_rolls, chosen_number]):
    simulation = RouletteSimulation(number_runs, number_rolls, chosen_number)
    results, absolute_frequency, relative_frequency = simulation.simulation()
    simulation.show_fr_fre_frn()
    simulation.show_vp_vpe_vpn()
    simulation.show_deviation_values()
    simulation.show_variance_values()
else:
    print('Los valores -c -n -e son obligatorios.')
    print('-c debe ser un entero positivo')
    print('-n debe ser un entero positivo')
    print('-e debe ser un entero positivo')
