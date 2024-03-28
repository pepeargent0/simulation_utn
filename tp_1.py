from random import randint
import argparse
import matplotlib as plt


class RouletteSimulation:
    def __init__(self, number_runs, number_rolls, chosen_number):
        self.results = []
        self.number_runs = number_runs
        self.number_rolls = number_rolls
        self.chosen_number = chosen_number
        self.frecuency_absolute = 0

    def simulation(self):
        for run in range(self.number_runs):
            self.results.append({})
            for rolls in range(self.number_rolls):
                _key = randint(0, 36)
                if _key == self.chosen_number:
                    self.frecuency_absolute += 1
                if _key in self.results[run].keys():
                    self.results[run][_key] += 1
                else:
                    self.results[run][_key] = 1
        print('frecuencia Absoluta:', self.frecuency_absolute)
        print('freciencia relativa: ', self.frecuency_absolute / (self.number_runs * self.number_rolls))


parser = argparse.ArgumentParser(description='Simulacion de ruleta')
parser.add_argument('-c', '--numero_corridas', type=int, help='Corridas')
parser.add_argument('-n', '--numero_tiradas', type=int, help='numero de tiradas')
parser.add_argument('-e', '--numero_eleguido', type=int, help='numero de eleguido')

args = parser.parse_args()
if ((args.numero_corridas and args.numero_tiradas and args.numero_eleguido)
        and (args.numero_corridas >= 0 and args.numero_tiradas >= 0 and args.numero_eleguido >= 0)):
    simulation = RouletteSimulation(args.numero_corridas, args.numero_tiradas, args.numero_eleguido)
    simulation.simulation()
else:
    print(' Los valores -c -n -e son obligatorios')
    exit()
