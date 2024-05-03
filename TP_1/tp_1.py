import argparse
import random
import matplotlib.pyplot as plt
import numpy as np


class Ruleta:
    def __init__(self, _numero_elegido, _cantidad_tiradas, _cantidad_corridas):
        """
        Inicializa una instancia de la clase Ruleta.

        Parámetros:
            numero_elegido (int): Número elegido en la ruleta.
            cantidad_tiradas (int): Cantidad de tiradas por corrida.
            cantidad_corridas (int): Cantidad de corridas a simular.
        """
        self.numero_elegido = _numero_elegido
        self.cantidad_tiradas = _cantidad_tiradas
        self.cantidad_corridas = _cantidad_corridas
        try:
            self.resultados = self._simular_corridas()
        except Exception as e:
            print("Error al simular las corridas:", e)

    def simular_corrida(self):
        """
        Simula una corrida de la ruleta y calcula las medidas estadísticas.

        Retorna:
            tuple: Tupla conteniendo las listas de frecuencia relativa, promedio, varianza y desvío.
        """
        resultados = [random.randint(0, 36) for _ in range(self.cantidad_tiradas)]
        contador_numero_elegido = 0
        frecuencias_relativas = []
        promedios = []
        varianzas = []
        desvios = []
        for i, tirada in enumerate(resultados, start=1):
            if tirada == self.numero_elegido:
                contador_numero_elegido += 1
            frecuencia_relativa = contador_numero_elegido / i
            frecuencias_relativas.append(frecuencia_relativa)
            promedio = sum(resultados[:i]) / i
            promedios.append(promedio)
            varianza = sum((x - promedio) ** 2 for x in resultados[:i]) / i
            varianzas.append(varianza)
            desvio = np.sqrt(varianza)
            desvios.append(desvio)
        return frecuencias_relativas, promedios, varianzas, desvios

    def _simular_corridas(self):
        """
        Realiza todas las corridas de la simulación.

        Retorna:
            list: Lista de resultados de cada corrida.
        """
        return [self.simular_corrida() for _ in range(self.cantidad_corridas)]

    def graficar_frecuencia_relativa(self):
        """
        Grafica la frecuencia relativa para cada corrida.
        """
        try:
            self._graficar('Frecuencia Relativa')
        except Exception as e:
            print("Error al graficar la frecuencia relativa:", e)

    def graficar_promedio(self):
        """
        Grafica el promedio para cada corrida.
        """
        try:
            self._graficar('Promedio')
        except Exception as e:
            print("Error al graficar el promedio:", e)

    def graficar_varianza(self):
        """
        Grafica la varianza para cada corrida.
        """
        try:
            self._graficar('Varianza')
        except Exception as e:
            print("Error al graficar la varianza:", e)

    def graficar_desvio(self):
        """
        Grafica el desvío para cada corrida.
        """
        try:
            self._graficar('Desvío')
        except Exception as e:
            print("Error al graficar el desvío:", e)

    def _graficar(self, ylabel):
        """
        Función interna para graficar.

        Parámetros:
            ylabel (str): Etiqueta del eje y.
        """
        plt.figure(figsize=(20, 10))
        labels = {'Frecuencia Relativa': 0, 'Promedio': 1, 'Varianza': 2, 'Desvío': 3}
        index = labels[ylabel]
        for i, corrida in enumerate(self.resultados, start=1):
            data = corrida[index]
            plt.plot(range(self.cantidad_tiradas), data, label=f'Corrida {i}')
        plt.xlabel('Cantidad de tiradas')
        plt.ylabel(ylabel)
        plt.title(ylabel)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(self.resultados), fancybox=True,
                   shadow=True)
        plt.grid(True)
        plt.show()


# Manejo de argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Simulacion de ruleta')
parser.add_argument('-c', '--numero_corridas', type=int, default=-1, help='Número de corridas (por defecto: 5)')
parser.add_argument('-n', '--numero_tiradas', type=int, default=-1, help='Número de tiradas (por defecto: 100)')
parser.add_argument('-e', '--numero_eleguido', type=int, default=0, help='Número elegido (por defecto: 0)')

args = parser.parse_args()
cantidad_corridas, cantidad_tiradas, numero_elegido = args.numero_corridas, args.numero_tiradas, args.numero_eleguido
try:
    if cantidad_corridas < 0:
        raise ValueError("-c debe ser un entero positivo")
    if cantidad_tiradas < 0:
        raise ValueError("-n debe ser un entero positivo")
    if not 0 <= numero_elegido <= 36:
        raise ValueError("-e debe ser un entero positivo entre 0 y 36")
except ValueError as ve:
    print("Error en los argumentos de entrada:", ve)
    exit()


ruleta = Ruleta(numero_elegido, cantidad_tiradas, cantidad_corridas)
ruleta.graficar_frecuencia_relativa()
ruleta.graficar_promedio()
ruleta.graficar_varianza()
ruleta.graficar_desvio()
