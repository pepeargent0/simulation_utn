import matplotlib.pyplot as plt
import random

def jugar_ruleta(tiradas, capital_inicial, capital_tipo):
    victorias = 0
    capital = capital_inicial
    frecuencia_relativa = []

    for i in range(tiradas):
        resultado = random.randint(0, 36)
        if resultado % 2 == 0:  # Victoria (número par)
            victorias += 1
        frecuencia_relativa.append(victorias / (i + 1))

        if capital_tipo == 'f':
            if capital <= 0:
                break
            if resultado % 2 == 0:
                capital += 100  # Aumentar capital en caso de victoria
            else:
                capital -= 100  # Reducir capital en caso de derrota

    return frecuencia_relativa

def obtener_valor_numerico(prompt):
    while True:
        try:
            valor = int(input(prompt))
            return valor
        except ValueError:
            print("Por favor, ingrese un número válido.")

def main():
    # Pedir al usuario que ingrese el número de tiradas y el monto inicial para el capital finito e infinito
    tiradas = obtener_valor_numerico("Ingrese el número de tiradas: ")
    capital_inicial_f = obtener_valor_numerico("Ingrese el monto inicial para el capital finito: ")
    capital_inicial_i = obtener_valor_numerico("Ingrese el monto inicial para el capital infinito: ")

    # Simulación para capital finito
    frecuencia_relativa_f = jugar_ruleta(tiradas, capital_inicial_f, 'f')

    # Simulación para capital infinito
    frecuencia_relativa_i = jugar_ruleta(tiradas, capital_inicial_i, 'i')

    # Graficar histogramas
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(frecuencia_relativa_f, bins=20, color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel('Frecuencia relativa de victorias')
    plt.ylabel('Número de ocurrencias')
    plt.title('Histograma de frecuencia relativa (Capital finito)')

    plt.subplot(1, 2, 2)
    plt.hist(frecuencia_relativa_i, bins=20, color='green', edgecolor='black', alpha=0.7)
    plt.xlabel('Frecuencia relativa de victorias')
    plt.ylabel('Número de ocurrencias')
    plt.title('Histograma de frecuencia relativa (Capital infinito)')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
