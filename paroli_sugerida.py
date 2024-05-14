import matplotlib.pyplot as plt
import random

def jugar_ruleta(tiradas, apuesta_inicial, capital_inicial, capital_tipo):
    capital = capital_inicial
    capital_historico = []
    bancarrota = 0

    for _ in range(tiradas):
        apuesta = apuesta_inicial

        if capital_tipo == 'f' and capital < apuesta:  # Verificar bancarrota en capital finito
            bancarrota += 1
            capital_historico.append(capital)
            continue

        resultado = random.randint(0, 36)
        if resultado % 2 == 0:  # Victoria (número par)
            capital += apuesta
            apuesta *= 2
        else:  # Derrota (número impar)
            capital -= apuesta
            apuesta = apuesta_inicial

        capital_historico.append(capital)

    return capital_historico, bancarrota

def graficar_evolucion_caja(capital_historico, capital_tipo):
    plt.plot(capital_historico)
    plt.xlabel('Número de tiradas')
    plt.ylabel('Capital')
    if capital_tipo == 'f':
        plt.title('Evolución de la caja (Capital finito)')
    else:
        plt.title('Evolución de la caja (Capital infinito)')
    plt.grid(True)

    # Ajustar los límites del eje y para mostrar valores por debajo de 0
    min_capital = min(capital_historico)
    max_capital = max(capital_historico)
    if min_capital < 0:
        plt.ylim(min_capital * 1.1, max_capital * 1.1)
    else:
        plt.ylim(0, max_capital * 1.1)

    plt.show()

def obtener_valor_numerico(prompt):
    while True:
        try:
            valor = int(input(prompt))
            return valor
        except ValueError:
            print("Por favor, ingrese un número válido.")

def main():
    # Pedir al usuario que ingrese el número de tiradas, el valor inicial de la apuesta y el monto mínimo con el que empezará
    tiradas = obtener_valor_numerico("Ingrese el número de tiradas: ")
    apuesta_inicial = obtener_valor_numerico("Ingrese el valor inicial de la apuesta: ")
    capital_inicial = obtener_valor_numerico("Ingrese el monto mínimo con el que va a empezar: ")

    # Simulación para capital finito
    capital_tipo = 'f'
    capital_historico, bancarrota = jugar_ruleta(tiradas, apuesta_inicial, capital_inicial, capital_tipo)
    print("Se fue a bancarrota", bancarrota, "veces (Capital finito).")
    graficar_evolucion_caja(capital_historico, capital_tipo)

    # Simulación para capital infinito
    capital_tipo = 'i'
    capital_historico, _ = jugar_ruleta(tiradas, apuesta_inicial, capital_inicial, capital_tipo)
    graficar_evolucion_caja(capital_historico, capital_tipo)

if __name__ == "__main__":
    main()
