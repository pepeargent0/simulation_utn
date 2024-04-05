import random
import matplotlib.pyplot as plt
import numpy as np

def simular_corrida(numero_elegido, cantidad_tiradas):
    resultados = [random.randint(0, 36) for _ in range(cantidad_tiradas)]
    frecuencias_relativas = []
    contador_7 = 0
    promedios = []
    varianzas = []
    desvios = []
    for i, tirada in enumerate(resultados, start=1):
        if tirada == numero_elegido:
            contador_7 += 1
        frecuencia_relativa = contador_7 / i
        frecuencias_relativas.append(frecuencia_relativa)
        promedio = sum(resultados[:i]) / i
        promedios.append(promedio)
        varianza = sum((x - promedio) ** 2 for x in resultados[:i]) / i
        varianzas.append(varianza)
        desvio = np.sqrt(varianza)
        desvios.append(desvio)
    return frecuencias_relativas, promedios, varianzas, desvios

# Ingresar número de corridas, número elegido y número de tiradas para cada corrida
cantidad_corridas = int(input("Ingrese el número de corridas: "))
numero_elegido = int(input("Ingrese el número elegido (entre 0 y 36): "))
cantidad_tiradas = int(input("Ingrese el número de tiradas para cada corrida: "))

# Realizar la simulación para cada corrida y graficar las curvas
plt.figure(figsize=(8, 6))
for i in range(cantidad_corridas):
    frecuencias_relativas, promedios, varianzas, desvios = simular_corrida(numero_elegido, cantidad_tiradas)
    # Graficar la frecuencia relativa
    plt.plot(range(cantidad_tiradas), frecuencias_relativas, label=f'Corrida {i+1}')
plt.xlabel('Cantidad de tiradas')
plt.ylabel('Frecuencia Relativa')
plt.title('Frecuencia Relativa')
plt.legend()
plt.grid(True)
plt.show()
plt.figure(figsize=(8, 6))
for i in range(cantidad_corridas):
    frecuencias_relativas, promedios, varianzas, desvios = simular_corrida(numero_elegido, cantidad_tiradas)
    plt.plot(range(cantidad_tiradas), promedios, label=f'Corrida {i+1}')
plt.xlabel('Cantidad de tiradas')
plt.ylabel('Promedio')
plt.title('Promedio')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
for i in range(cantidad_corridas):
    frecuencias_relativas, promedios, varianzas, desvios = simular_corrida(numero_elegido, cantidad_tiradas)
    plt.plot(range(cantidad_tiradas), varianzas, label=f'Corrida {i + 1}')
plt.xlabel('Cantidad de tiradas')
plt.ylabel('Varianza')
plt.title('Varianza')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
for i in range(cantidad_corridas):
    frecuencias_relativas, promedios, varianzas, desvios = simular_corrida(numero_elegido, cantidad_tiradas)
    plt.plot(range(cantidad_tiradas), desvios, label=f'Corrida {i+1}')
plt.xlabel('Cantidad de tiradas')
plt.ylabel('Desvío')
plt.title('Desvío')
plt.legend()
plt.grid(True)
plt.show()
"""
    # Graficar la varianza
    
    

    # Graficar el desvío
    plt.figure(figsize=(8, 6))
    plt.plot(range(cantidad_tiradas), desvios, label=f'Corrida {i+1}')
    plt.xlabel('Cantidad de tiradas')
    plt.ylabel('Desvío')
    plt.title('Desvío')
    plt.legend()
    plt.grid(True)
    plt.show()
"""
