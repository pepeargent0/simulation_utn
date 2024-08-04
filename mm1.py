import simpy
import random
import numpy as np
import matplotlib.pyplot as plt


class MM1Queue:
    def __init__(self, env, arrival_rate, service_rate):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.queue_length = []
        self.wait_times = []
        self.customers_served = 0

    def process_customer(self, customer):
        arrival_time = self.env.now
        with self.server.request() as request:
            yield request
            wait_time = self.env.now - arrival_time
            self.wait_times.append(wait_time)
            service_time = random.expovariate(self.service_rate)
            yield self.env.timeout(service_time)
            self.queue_length.append(len(self.server.queue))
            self.customers_served += 1

    def run(self):
        customer_id = 0
        while True:
            yield self.env.timeout(random.expovariate(self.arrival_rate))
            self.env.process(self.process_customer(customer_id))
            customer_id += 1


# Función para realizar los cálculos teóricos
def calcular_valores_teoricos(arrival_rate, service_rate, K):
    if arrival_rate >= service_rate:
        return {
            'rho': float('inf'),
            'L': float('inf'),
            'L_q': float('inf'),
            'W': float('inf'),
            'W_q': float('inf'),
            'P_n': [float('inf')] * (K + 1),
            'P_denegacion': float('inf')
        }

    rho = arrival_rate / service_rate
    L = arrival_rate / (service_rate - arrival_rate)
    L_q = (arrival_rate ** 2) / (service_rate * (service_rate - arrival_rate))
    W = 1 / (service_rate - arrival_rate)
    W_q = arrival_rate / (service_rate * (service_rate - arrival_rate))
    P_n = [(1 - rho) * (rho ** n) for n in range(K + 1)]
    P_denegacion = rho ** K
    return {
        'rho': rho,
        'L': L,
        'L_q': L_q,
        'W': W,
        'W_q': W_q,
        'P_n': P_n,
        'P_denegacion': P_denegacion
    }


def simulate_mm1(arrival_rate, service_rate, num_runs, sim_time, K):
    avg_customers_in_system = []
    avg_customers_in_queue = []
    avg_time_in_system = []
    avg_time_in_queue = []
    server_utilization = []
    P_n = [[] for _ in range(K + 1)]
    denegacion_count = []

    for _ in range(num_runs):
        env = simpy.Environment()
        mm1_queue = MM1Queue(env, arrival_rate, service_rate)
        env.process(mm1_queue.run())
        env.run(until=sim_time)
        avg_customers_in_system.append(
            np.mean(mm1_queue.queue_length) + np.mean([1 if i < service_rate else 0 for i in mm1_queue.wait_times]))
        avg_customers_in_queue.append(np.mean(mm1_queue.queue_length))
        avg_time_in_system.append(np.mean(mm1_queue.wait_times) + (1 / service_rate))
        avg_time_in_queue.append(np.mean(mm1_queue.wait_times))
        server_utilization.append(arrival_rate / service_rate)
        queue_lengths = np.array(mm1_queue.queue_length)
        for n in range(K + 1):
            P_n[n].append(np.sum(queue_lengths == n) / len(queue_lengths))
        denegacion_count.append(np.sum(queue_lengths >= K) / len(queue_lengths))

    P_n_avg = [np.mean(P_n_n) for P_n_n in P_n]
    P_denegacion_avg = np.mean(denegacion_count)

    return {
        'L': np.mean(avg_customers_in_system),
        'L_q': np.mean(avg_customers_in_queue),
        'W': np.mean(avg_time_in_system),
        'W_q': np.mean(avg_time_in_queue),
        'rho': np.mean(server_utilization),
        'P_n': P_n_avg,
        'P_denegacion': P_denegacion_avg
    }


def comparar_resultados(resultados_teoricos, resultados_simulacion, K):
    print("Comparación de Resultados:")
    for key in ['rho', 'L', 'L_q', 'W', 'W_q']:
        valor_teorico = resultados_teoricos[key]
        valor_simulacion = resultados_simulacion[key]
        diferencia = valor_simulacion - valor_teorico if valor_teorico != float('inf') else 'N/A'
        print(
            f"{key}: Teórico = {valor_teorico if valor_teorico != float('inf') else 'Inestable'}, Simulado = {valor_simulacion:.4f}, Diferencia = {diferencia}")

    print("\nProbabilidades de encontrar n clientes en cola (P_n):")
    for n in range(K + 1):
        valor_teorico = resultados_teoricos['P_n'][n]
        valor_simulacion = resultados_simulacion['P_n'][n]
        diferencia = valor_simulacion - valor_teorico if valor_teorico != float('inf') else 'N/A'
        print(
            f"n = {n}: Teórico = {valor_teorico if valor_teorico != float('inf') else 'Inestable'}, Simulado = {valor_simulacion:.4f}, Diferencia = {diferencia}")

    print("\nProbabilidad de denegación de servicio (P_denegacion):")
    valor_teorico = resultados_teoricos['P_denegacion']
    valor_simulacion = resultados_simulacion['P_denegacion']
    diferencia = valor_simulacion - valor_teorico if valor_teorico != float('inf') else 'N/A'
    print(
        f"Teórico = {valor_teorico if valor_teorico != float('inf') else 'Inestable'}, Simulado = {valor_simulacion:.4f}, Diferencia = {diferencia}")


def graficar_resultados(arrival_rates, resultados_teoricos, resultados_simulacion, metricas):
    for metrica in metricas:
        valores_teoricos = [res[metrica] for res in resultados_teoricos]
        valores_simulados = [res[metrica] for res in resultados_simulacion]

        plt.figure(figsize=(10, 6))
        plt.plot(arrival_rates, valores_teoricos, marker='o', label='Teórico')
        plt.plot(arrival_rates, valores_simulados, marker='x', label='Simulado')
        plt.xlabel('Tasa de arribo (proporción de la tasa de servicio)')
        plt.ylabel(metrica)
        plt.title(f'{metrica} vs Tasa de Arribo')
        plt.legend()
        plt.grid(True)
        plt.show()


def graficar_densidad_probabilidad(arrival_rates, resultados_simulacion, K):
    for arrival_rate, res_sim in zip(arrival_rates, resultados_simulacion):
        plt.figure(figsize=(10, 6))
        plt.bar(range(K + 1), res_sim['P_n'])
        plt.xlabel('Número de clientes en cola')
        plt.ylabel('Probabilidad')
        plt.title(f'Densidad de Probabilidad de Clientes en Cola\nTasa de arribo = {arrival_rate}')
        plt.grid(True)
        plt.show()


arrival_rates = [0.25, 0.5, 0.75, 1.0, 1.25]
service_rate = 1.0
num_runs = 1
sim_time = 1000
K = 50

resultados_teoricos = []
resultados_simulacion = []

for arrival_rate in arrival_rates:
    resultados_teoricos.append(calcular_valores_teoricos(arrival_rate, service_rate, K))
    resultados_simulacion.append(simulate_mm1(arrival_rate, service_rate, num_runs, sim_time, K))

metricas = ['rho', 'L', 'L_q', 'W', 'W_q']

graficar_resultados(arrival_rates, resultados_teoricos, resultados_simulacion, metricas)
graficar_densidad_probabilidad(arrival_rates, resultados_simulacion, K)
