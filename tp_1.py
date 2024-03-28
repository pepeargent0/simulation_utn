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

    def simulation(self):
        for run in range(self.number_runs):
            self.results.append({})
            for rolls in range(self.number_rolls):
                _key = randint(0, 36)
                if _key == self.chosen_number:
                    self.frequency_absolute += 1
                if _key in self.results[run].keys():
                    self.results[run][_key] += 1
                else:
                    self.results[run][_key] = 1
        frequency_relative = self.frequency_absolute / (self.number_runs * self.number_rolls)
        return self.results, self.frequency_absolute, frequency_relative


def plot_histogram(results):
    plt.figure(figsize=(10, 6))
    for run in results:
        plt.bar(run.keys(), run.values(), alpha=0.5)
    plt.xlabel('Número')
    plt.ylabel('Frecuencia Absoluta')
    plt.title('Histograma de Frecuencia Absoluta de Números')
    plt.show()

def plot_frequency(results, chosen_number):
    frequencies = []
    for run in results:
        print(run)
        frequencies.append(run[chosen_number] if chosen_number in run else 0)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(frequencies)), frequencies)
    plt.xlabel('Corridas')
    plt.ylabel('Frecuencia Absoluta del Número Elegido')
    plt.title('Frecuencia Absoluta del Número Elegido a lo largo de las Corridas')
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
    plot_histogram(results)
    plot_frequency(results, chosen_number)
else:
    print('Los valores -c -n -e son obligatorios.')
    print('-c debe ser un entero positivo')
    print('-n debe ser un entero positivo')
    print('-e debe ser un entero positivo')
