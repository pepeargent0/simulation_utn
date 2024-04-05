import argparse
import random
import matplotlib.pyplot as plt
import numpy as np


class Ruleta:
    def __init__(self, _numero_elegido, _cantidad_tiradas, _cantidad_corridas):
        self.numero_elegido = _numero_elegido
        self.cantidad_tiradas = _cantidad_tiradas
        self.cantidad_corridas = _cantidad_corridas
        self.resultados = self.simular_corridas()

    def simular_corrida(self):
        resultados = [random.randint(0, 36) for _ in range(self.cantidad_tiradas)]
        _contador = 0
        frecuencias_relativas = []
        promedios = []
        varianzas = []
        desvios = []
        for i, tirada in enumerate(resultados, start=1):
            if tirada == self.numero_elegido:
                _contador += 1
            frecuencia_relativa = _contador / i
            frecuencias_relativas.append(frecuencia_relativa)
            promedio = sum(resultados[:i]) / i
            promedios.append(promedio)
            varianza = sum((x - promedio) ** 2 for x in resultados[:i]) / i
            varianzas.append(varianza)
            desvio = np.sqrt(varianza)
            desvios.append(desvio)
        return frecuencias_relativas, promedios, varianzas, desvios

    def simular_corridas(self):
        return [self.simular_corrida() for _ in range(self.cantidad_corridas)]

    def graficar_frecuencia_relativa(self):
        plt.figure(figsize=(20, 10))
        for i, corrida in enumerate(self.resultados, start=1):
            plt.plot(corrida)
            plt.plot(range(self.cantidad_tiradas), corrida[0], label=f'Corrida {i}')
        plt.xlabel('Cantidad de corridas')
        plt.ylabel('Frecuencia Relativa')
        plt.title('Frecuencia Relativa')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(self.resultados), fancybox=True, shadow=True)
        plt.grid(True)
        plt.show()

    def graficar_promedio(self):
        plt.figure(figsize=(20, 10))
        for i, corrida in enumerate(self.resultados, start=1):
            plt.plot(range(self.cantidad_tiradas), corrida[1], label=f'Corrida {i}')
        plt.xlabel('Cantidad de tiradas')
        plt.ylabel('Promedio')
        plt.title('Promedio')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(self.resultados), fancybox=True, shadow=True)
        plt.grid(True)
        plt.show()

    def graficar_varianza(self):
        plt.figure(figsize=(20, 10))
        for i, corrida in enumerate(self.resultados, start=1):
            plt.plot(range(self.cantidad_tiradas), corrida[2], label=f'Corrida {i}')
        plt.xlabel('Cantidad de tiradas')
        plt.ylabel('Varianza')
        plt.title('Varianza')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(self.resultados), fancybox=True, shadow=True)
        plt.grid(True)
        plt.show()

    def graficar_desvio(self):
        plt.figure(figsize=(20, 10))
        for i, corrida in enumerate(self.resultados, start=1):
            plt.plot(range(self.cantidad_tiradas), corrida[3], label=f'Corrida {i}')
        plt.xlabel('Cantidad de tiradas')
        plt.ylabel('Desvío')
        plt.title('Desvío')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(self.resultados), fancybox=True, shadow=True)
        plt.grid(True)
        plt.show()


parser = argparse.ArgumentParser(description='Simulacion de ruleta')
parser.add_argument('-c', '--numero_corridas', type=int, help='Corridas')
parser.add_argument('-n', '--numero_tiradas', type=int, help='numero de tiradas')
parser.add_argument('-e', '--numero_eleguido', type=int, help='numero de eleguido')

args = parser.parse_args()
cantidad_corridas, cantidad_tiradas, numero_elegido = args.numero_corridas, args.numero_tiradas, args.numero_eleguido

if not 0 <= numero_elegido <= 36:
    print('-e debe ser un entero positivo entre 0 y 36')
    exit()

if all(isinstance(arg, int) and arg >= 0 for arg in [cantidad_corridas, cantidad_tiradas, numero_elegido]):
    ruleta = Ruleta(_numero_elegido=numero_elegido,_cantidad_tiradas=cantidad_tiradas, _cantidad_corridas=cantidad_corridas)
    ruleta.graficar_frecuencia_relativa()
    ruleta.graficar_promedio()
    ruleta.graficar_varianza()
    ruleta.graficar_desvio()

else:
    print('Los valores -c -n -e son obligatorios.')
    print('-c debe ser un entero positivo')
    print('-n debe ser un entero positivo')
    print('-e debe ser un entero positivo entre 0 y 36')
