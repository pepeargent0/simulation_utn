from random import randint
import numpy as np
import argparse
import matplotlib.pyplot as plt


class RouletteSimulation:
    def __init__(self, cantidad_tiradas, number_rolls, numero_elegido):
        self.results = []
        self.cantidad_tiradas = cantidad_tiradas
        self.cantidad_tiradas = cantidad_tiradas
        self.numero_elegido = numero_elegido
        self.frequency_absolute = 0
        self.frecuencias_relativas = []
        self.average_values = []

    def simulation(self):
        resultados = [randint(0, 36) for _ in range(self.cantidad_tiradas)]
        frecuencias_relativas = []
        contador = 0
        promedios = []
        varianzas = []
        desvios = []
        for i, tirada in enumerate(resultados, start=1):
            if tirada == self.numero_elegido:
                contador += 1
            frecuencia_relativa = contador / i
            frecuencias_relativas.append(frecuencia_relativa)
            promedio = sum(resultados[:i]) / i
            promedios.append(promedio)
            varianza = sum((x - promedio) ** 2 for x in resultados[:i]) / i
            varianzas.append(varianza)
            desvio = np.sqrt(varianza)
            desvios.append(desvio)


    def get_frequencies(self):
        frequencies = {'FR': [], 'FRE': [], 'FRN': []}
        for run in self.average_values:  # Iterar sobre las frecuencias relativas por tirada en cada corrida
            total_rolls = sum(run)
            if total_rolls != 0:
                fr = run[self.chosen_number] / total_rolls  # Calcular la frecuencia relativa para el número elegido
            else:
                fr = 0.0
            fre = 1 / 36
            frn = fre / self.number_runs
            frequencies['FR'].append(fr)
            frequencies['FRE'].append(fre)
            frequencies['FRN'].append(frn)
        return frequencies




parser = argparse.ArgumentParser(description='Simulacion de ruleta')
parser.add_argument('-c', '--numero_corridas', type=int, help='Corridas')
parser.add_argument('-n', '--numero_tiradas', type=int, help='numero de tiradas')
parser.add_argument('-e', '--numero_eleguido', type=int, help='numero de eleguido')

args = parser.parse_args()
number_runs, number_rolls, chosen_number = args.numero_corridas, args.numero_tiradas, args.numero_eleguido

if all(isinstance(arg, int) and arg >= 0 for arg in [number_runs, number_rolls, chosen_number]):
    simulation = RouletteSimulation(number_runs, number_rolls, chosen_number)
    results, absolute_frequency, relative_frequency = simulation.simulation()
    frequencies = simulation.get_frequencies()
    print(frequencies['FR'])
    plt.figure(figsize=(10, 6))
    for i, fr_list in enumerate(frequencies['FR']):
        plt.plot(i+1, fr_list, label=f'Tirada {i + 1}', linestyle = 'dotted')
    plt.xlabel('Corridas')
    plt.ylabel('Frecuencia Relativa')
    plt.title('Evolución de la Frecuencia Relativa del Número Elegido')
    plt.legend()
    plt.grid(True)
    plt.show()
    """
    for i, fr in enumerate(frs):
        plt.plot(range(1, number_runs + 1), fr, label=f'Tirada {i + 1}')
    plt.xlabel('Corridas')
    plt.ylabel('Frecuencia Relativa')
    plt.title('Evolución de la Frecuencia Relativa del Número Elegido')
    plt.legend()
    plt.grid(True)
    plt.show()
    """
else:
    print('Los valores -c -n -e son obligatorios.')
    print('-c debe ser un entero positivo')
    print('-n debe ser un entero positivo')
    print('-e debe ser un entero positivo')
