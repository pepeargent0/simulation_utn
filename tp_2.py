import argparse
import random
import matplotlib.pyplot as plt
import numpy as np

num_fibo= [0,1]
def fibonacci(n):
    if n == 0 or n == 1:
        return num_fibo[n]
    for i in range(2, n+1):
        num_fibo.append(num_fibo[i-1]+num_fibo[i-2])
    return num_fibo[n]

def martingala(numero_elgido, numero_resultado, nonto_apostar):
    print(numero_elgido, numero_resultado, nonto_apostar)
    if numero_elgido == numero_resultado:
        return -1
    return nonto_apostar*2
def d_alembert(numero_elgido, numero_resultado, monto_apostar):
    if numero_elgido == numero_resultado:
        return monto_apostar-1
    return monto_apostar+1

def fibonacci_estrategia(numero_elgido, numero_resultado, monto_apostar):
    if numero_elgido != numero_resultado:
        return fibonacci(monto_apostar+1)
    return monto_apostar

monto_maximo = 1000000
class Ruleta:
    def __init__(self, _numero_elegido, _cantidad_tiradas, _cantidad_corridas, _estrategia, _tipo_capital):
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
        self.estrategia = _estrategia
        self.tipo_capital = _tipo_capital
        self.bancas_rotas = 0
        self.monto_apostar = 1
        self.ganadas_mg = 0
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
            self.monto_apostar = self.ejecutar_estrategia(tirada)

            if self.tipo_capital == 'f' and self.monto_apostar > monto_maximo:
                self.bancas_rotas += 1

            if self.monto_apostar == -1:
                self.ganadas_mg += 1
                print('gano con martin gala')
                self.monto_apostar = 1

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
        print(self.monto_apostar)
        return frecuencias_relativas, promedios, varianzas, desvios

    def ejecutar_estrategia(self, numero_resultado):
        """
        Ejecuta la estrategia de apuesta especificada.

        Parámetros:
            numero_resultado (int): Resultado de la tirada de la ruleta.

        Retorna:
            int: Monto de apuesta para la siguiente tirada.
        """

        estrategias = {
            'm': martingala(self.numero_elegido, numero_resultado, self.monto_apostar),
            'd': d_alembert(self.numero_elegido, numero_resultado, self.monto_apostar),
            'f': fibonacci_estrategia(self.numero_elegido, numero_resultado, self.monto_apostar),
            'o': 0
        }
        return estrategias[self.estrategia]

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
parser.add_argument('-s','--strategic', type=str, default='m', help='Ingrese la estregia que va a usar '
                                                                    '(por defecto: m)')
parser.add_argument('-a', '--capital', type=str, default='i', help='Ingrese la capital que va a '
                                                                   'usar (por defecto: es infinito)')

args = parser.parse_args()
cantidad_corridas, cantidad_tiradas, numero_elegido, estrategia, tipo_capital = (args.numero_corridas,
                                                                                 args.numero_tiradas,
                                                                                 args.numero_eleguido,
                                                                                 args.strategic,
                                                                                 args.capital)
try:
    if cantidad_corridas < 0:
        raise ValueError("-c debe ser un entero positivo")
    if cantidad_tiradas < 0:
        raise ValueError("-n debe ser un entero positivo")
    if not 0 <= numero_elegido <= 36:
        raise ValueError("-e debe ser un entero positivo entre 0 y 36")
    if estrategia not in ['m','d','f','o']:
        raise ValueError("-s debe ser m, d, f, u o")
    if tipo_capital not in ['i','f']:
        raise ValueError("-a los posibles valores son i o f")

except ValueError as ve:
    print("Error en los argumentos de entrada:", ve)
    exit()


ruleta = Ruleta(numero_elegido, cantidad_tiradas, cantidad_corridas, estrategia, tipo_capital
print('fin')
"""
ruleta.graficar_frecuencia_relativa()
ruleta.graficar_promedio()
ruleta.graficar_varianza()
ruleta.graficar_desvio()
"""
"""
links https://liquidity-provider.com/es/articles/what-is-the-martingale-strategy-in-trading/#:~:text=La%20estrategia%20Martingala%20consiste%20en,una%20cantidad%20infinita%20de%20capital.
https://mundoruleta.es/guia/dalembert/
https://mundoruleta.es/guia/fibonacci/
https://blog.bodog.com/es/sistema-andrucci/
"""