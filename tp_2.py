import argparse
import random
import matplotlib.pyplot as plt
import numpy as np

num_fibo = [0, 1]


def fibonacci(n):
    if n == 0 or n == 1:
        return num_fibo[n]
    for i in range(2, n + 1):
        num_fibo.append(num_fibo[i - 1] + num_fibo[i - 2])
    return num_fibo[n]


def fibonacci_estrategia(numero_elegido, numero_resultado, monto_apostar):
    if numero_elegido != numero_resultado:
        return fibonacci(monto_apostar + 1)
    return monto_apostar

def martingala(criterio, numero_resultado, monto_apostar):
    if numero_resultado in criterio:
        return monto_apostar
    else:
        return monto_apostar * 2


def paroli(criterio, numero_resultado, monto_apostar):
    if numero_resultado in criterio:
        return monto_apostar * 2
    return monto_apostar

def d_alembert(criterio, numero_resultado, monto_apostar):
    if numero_resultado in criterio:
        return max(1, monto_apostar - 1)
    return monto_apostar + 1


def fibonacci_estrategia(criterio, numero_resultado, monto_apostar):
    if numero_resultado not in criterio:
        return fibonacci(monto_apostar + 1)
    return monto_apostar



class Ruleta:
    def __init__(self, _cantidad_tiradas, _cantidad_corridas, _estrategia, _tipo_capital, _criterio=[], _apuesta_inicial=1):
        """
        Inicializa una instancia de la clase Ruleta.

        Parámetros:
            _cantidad_tiradas (int): Cantidad de tiradas por corrida.
            _cantidad_corridas (int): Cantidad de corridas a simular.
            _estrategia (str): Estrategia que se utilizará en la simulación.
            _tipo_capital (str): Tipo de capital que se utilizará en la simulación.
            _criterio (int, opcional): Criterio que determina cuándo termina una corrida (por ejemplo, una cantidad mínima de capital).
            _apuesta_inicial (int, opcional): La cantidad de apuesta inicial con la que se comenzará en cada corrida.
        """
        self.cantidad_tiradas = _cantidad_tiradas
        self.cantidad_corridas = _cantidad_corridas
        self.estrategia = _estrategia
        self.tipo_capital = _tipo_capital
        self.criterio = _criterio
        self.monto_apostar = _apuesta_inicial
        self.bancas_rotas = 0
        self.ganadas_mg = 0
        try:
            self.resultados = self._simular_corridas()
        except Exception as e:
            print("Error al simular las corridas:", e)


    def simular_corrida(self):
        """
        Simula una corrida de la ruleta y calcula las medidas estadísticas.
        """
        try:
            resultados = [random.randint(0, 36) for _ in range(self.cantidad_tiradas)]

            for tirada in resultados:

                if self.estrategia == 'm':
                    self.monto_apostar = martingala(self.criterio, tirada, self.monto_apostar)

                if self.estrategia == 'd':
                    self.monto_apostar = d_alembert(self.criterio, tirada, self.monto_apostar)

                if self.estrategia == 'p':
                    self.monto_apostar = paroli(self.criterio, tirada, self.monto_apostar)

                if self.estrategia == 'f':
                    self.monto_apostar = fibonacci_estrategia(self.criterio, tirada, self.monto_apostar)

                if self.tipo_capital is not None:
                    self.tipo_capital = float(self.tipo_capital)
                    if self.monto_apostar > self.tipo_capital:
                        self.bancas_rotas = self.bancas_rotas + 1

        except IndexError as e:
            print("Error al simular las corridas:", e)



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


parser = argparse.ArgumentParser(description='Simulación de ruleta')
parser.add_argument('-c', '--numero_corridas', type=int, default=3, help='Número de corridas (por defecto: 5)')
parser.add_argument('-n', '--numero_tiradas', type=int, default=10, help='Número de tiradas (por defecto: 100)')
parser.add_argument('-s', '--estrategia', type=str, default='m',
                    help='Ingrese la estrategia que va a usar (por defecto: m)')
parser.add_argument('-a', '--capital', type=str, default=None,
                    help='Ingrese la capital que va a usar (por defecto: es infinito)')
parser.add_argument('--apuesta', type=float, default=2, help='Ingrese la capital que va a apostar (por defecto: 1)')
parser.add_argument('--color', type=str, choices=['rojo', 'negro'], help='Elija el color (rojo o negro)')
parser.add_argument('--paridad', type=str, choices=['par', 'impar'], help='Elija la paridad (par o impar)')
parser.add_argument('--alto_bajo', type=str, choices=['alto', 'bajo'], help='Elija si alto (19-36) o bajo (1-18)')

args = parser.parse_args()
cantidad_corridas = args.numero_corridas
cantidad_tiradas = args.numero_tiradas
estrategia = args.estrategia
tipo_capital = args.capital
color = args.color
paridad = args.paridad
alto_bajo = args.alto_bajo
apuesta_minimo = args.apuesta
try:
    if not color and not paridad and not alto_bajo:
        raise ValueError("Se requiere definir criterio de apuesta: color O paridad O alto_bajo")

    if color and color not in ['rojo', 'negro']:
        raise ValueError("--color debe ser rojo o negro")
    if paridad and paridad not in ['par', 'impar']:
        raise ValueError("--paridad debe ser par o impar")

    if alto_bajo and alto_bajo not in ['alto', 'bajo']:
        raise ValueError("--alto_bajo debe ser alto o bajo")

    if cantidad_corridas < 0:
        raise ValueError("-c debe ser un entero positivo")
    if cantidad_tiradas < 0:
        raise ValueError("-n debe ser un entero positivo")

    if estrategia not in ['m', 'd', 'f', 'p']:
        raise ValueError("-s debe ser m, d, f, u p")

    if (color and paridad) or (color and alto_bajo) or (paridad and alto_bajo):
        raise ValueError("Solo puede elegir una opción entre color, paridad, y alto/bajo")
    criterio = []
    if color:
        if color == 'rojo':
            criterio = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        else:
            criterio = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    if paridad:
        if paridad == 'par':
            criterio = [x for x in range(37) if x % 2 == 0]
        else:
            criterio = [x for x in range(37) if x % 2 != 0]

    if alto_bajo:
        if alto_bajo == 'alto':
            criterio = [x for x in range(19, 37)]
        else:
            criterio = [x for x in range(1, 19)]

except ValueError as ve:
    print("Error en los argumentos de entrada:", ve)
    exit()
print(apuesta_minimo, 'minimo')
ruleta = Ruleta(_cantidad_tiradas=cantidad_tiradas, _cantidad_corridas=cantidad_corridas, _estrategia=estrategia,
                 _tipo_capital=tipo_capital, _criterio=criterio, _apuesta_inicial=apuesta_minimo)

if tipo_capital:
    print('num bancarotas: ',ruleta.bancas_rotas)
print('ultima apuesta: ',ruleta.monto_apostar)
"""
ruleta.graficar_frecuencia_relativa()
ruleta.graficar_promedio()
ruleta.graficar_varianza()
ruleta.graficar_desvio()
"""
"""
links https://liquidity-provider.com/es/articles/what-is-the-martingale-strategy-
in-trading/#:~:text=La%20estrategia%20Martingala%20consiste%20en,una%20cantidad%20infinita%20de%20capital.
https://mundoruleta.es/guia/dalembert/
https://mundoruleta.es/guia/fibonacci/
https://blog.bodog.com/es/sistema-andrucci/
"""
