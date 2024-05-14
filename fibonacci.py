import matplotlib.pyplot as plt
import random


def fibonacci(n):
  if n == 0 or n == 1:
    return n
  else:
    return fibonacci(n - 1) + fibonacci(n - 2)

def simulacion(tipo_capital, capital, corridas):
  secuencia_fibonacci = []
  ganancias_perdidas = []

  for i in range(corridas):
    secuencia_fibonacci.append(capital)

    # Apuesta
    apuesta = capital

    # Simulación de la tirada
    if random.random() < 0.5:  # Gana
      capital += apuesta
      secuencia_fibonacci.append(capital)
      ganancias_perdidas.append(1)

      # Retroceder dos pasos en la secuencia de Fibonacci
      if tipo_capital == "finito":
        capital = secuencia_fibonacci[-3]
      else:  # Capital infinito
        capital = max(capital_minimo, secuencia_fibonacci[-3])

    else:  # Pierde
      capital -= apuesta
      secuencia_fibonacci.append(capital)
      ganancias_perdidas.append(-1)

      # Avanzar un paso en la secuencia de Fibonacci
      capital = secuencia_fibonacci[-2]

  return secuencia_fibonacci, ganancias_perdidas

# Ingresar parámetros
capital_inicial = float(input("Ingrese el capital inicial: "))
capital_minimo = float(input("Ingrese el capital mínimo (infinito): "))
corridas = int(input("Ingrese el número de corridas: "))

# Simular capital finito
secuencia_fibonacci_finito, ganancias_perdidas_finito = simulacion("finito", capital_inicial, corridas)

# Simular capital infinito
secuencia_fibonacci_infinito, ganancias_perdidas_infinito = simulacion("infinito", capital_minimo, corridas)

# Gráficas
plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)
plt.plot(secuencia_fibonacci_finito)
plt.title(f"Capital finito ({capital_inicial}€)")
plt.xlabel("Tirada")
plt.ylabel("Capital")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(secuencia_fibonacci_infinito)
plt.title(f"Capital infinito (mínimo: {capital_minimo}€)")
plt.xlabel("Tirada")
plt.ylabel("Capital")
plt.grid(True)

plt.tight_layout()
plt.show()
