import simpy
import numpy as np
import matplotlib.pyplot as plt
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModeloInventario:
    def __init__(self, D, Q, R, i, k, h, p):
        self.D = D  # Demanda anual
        self.Q = Q  # Cantidad de pedido
        self.R = R  # Punto de reorden
        self.i = i  # Costo unitario del producto
        self.k = k  # Costo de preparación
        self.h = h  # Costo de mantenimiento por unidad por año
        self.p = p  # Costo de faltante por unidad
        logger.info('ModeloInventario inicializado con parámetros D=%d, Q=%d, R=%d, i=%d, k=%d, h=%d, p=%d', D, Q, R, i, k, h, p)

    def calcular_valores_teoricos(self):
        """Calcula los valores teóricos de costos."""
        C_o = (self.D / self.Q) * self.k
        C_h = (self.Q / 2) * self.h
        C_s = (self.D / self.Q) * self.p
        C_t = C_o + C_h + C_s
        valores_teoricos = {
            'Costo de Orden': C_o,
            'Costo de Mantenimiento': C_h,
            'Costo de Faltante': C_s,
            'Costo Total': C_t
        }
        logger.info('Valores teóricos calculados: %s', valores_teoricos)
        return valores_teoricos

    def proceso_inventario(self, env, sim_time, costos_diarios):
        """Proceso de simulación del inventario."""
        inventario = self.Q
        costo_orden = 0
        costo_mantenimiento = 0
        costo_faltante = 0

        while env.now < sim_time:
            demanda = np.random.poisson(self.D / 365)
            if inventario >= demanda:
                inventario -= demanda
            else:
                costo_faltante += (demanda - inventario) * self.p
                inventario = 0

            costo_mantenimiento += inventario * self.h / 365
            if inventario <= self.R:
                inventario += self.Q
                costo_orden += self.k

            # Registrar costos diarios
            costos_diarios.append({
                'Día': env.now,
                'Costo de Orden': costo_orden,
                'Costo de Mantenimiento': costo_mantenimiento,
                'Costo de Faltante': costo_faltante,
                'Costo Total': costo_orden + costo_mantenimiento + costo_faltante
            })

            yield env.timeout(1)

        resultados_corrida = {
            'Costo de Orden': costo_orden,
            'Costo de Mantenimiento': costo_mantenimiento,
            'Costo de Faltante': costo_faltante,
            'Costo Total': costo_orden + costo_mantenimiento + costo_faltante
        }
        logger.info('Resultados de la simulación: %s', resultados_corrida)
        return resultados_corrida

    def simular_inventario(self, sim_time):
        """Simula el inventario para un tiempo de simulación dado."""
        env = simpy.Environment()
        costos_diarios = []
        resultado = env.process(self.proceso_inventario(env, sim_time, costos_diarios))
        env.run()
        return resultado.value, costos_diarios

    def multiple_corridas(self, num_runs, sim_time):
        """Realiza múltiples corridas de la simulación."""
        logger.info('Iniciando múltiples corridas: num_runs=%d, sim_time=%d', num_runs, sim_time)
        resultados = []
        todos_costos_diarios = []
        for _ in range(num_runs):
            resultado, costos_diarios = self.simular_inventario(sim_time)
            resultados.append(resultado)
            todos_costos_diarios.append(costos_diarios)
        logger.info('Resultados de todas las corridas: %s', resultados)
        return resultados, todos_costos_diarios

    def calcular_promedios(self, resultados):
        """Calcula los promedios de los resultados de las corridas."""
        if not resultados:
            logger.warning('No hay resultados para calcular promedios')
            return {'Costo de Orden': np.nan, 'Costo de Mantenimiento': np.nan, 'Costo de Faltante': np.nan, 'Costo Total': np.nan}

        promedios = {
            'Costo de Orden': np.mean([r['Costo de Orden'] for r in resultados]),
            'Costo de Mantenimiento': np.mean([r['Costo de Mantenimiento'] for r in resultados]),
            'Costo de Faltante': np.mean([r['Costo de Faltante'] for r in resultados]),
            'Costo Total': np.mean([r['Costo Total'] for r in resultados])
        }
        logger.info('Promedios calculados: %s', promedios)
        return promedios

    def graficar_resultados(self, valores_teoricos, promedios_simulacion):
        """Genera gráficos comparando los resultados teóricos con los resultados simulados."""
        categorias = list(valores_teoricos.keys())
        valores_teoricos_lista = list(valores_teoricos.values())
        valores_simulacion_lista = list(promedios_simulacion.values())

        x = np.arange(len(categorias))  # La posición de las etiquetas en el eje x
        width = 0.35  # El ancho de las barras

        fig, ax = plt.subplots()
        barras_teoricas = ax.bar(x - width/2, valores_teoricos_lista, width, label='Teórico')
        barras_simuladas = ax.bar(x + width/2, valores_simulacion_lista, width, label='Simulado')

        # Añadir etiquetas, título y leyenda
        ax.set_xlabel('Categoría')
        ax.set_ylabel('Costo')
        ax.set_title('Comparación de Costos Teóricos y Simulados')
        ax.set_xticks(x)
        ax.set_xticklabels(categorias, rotation=45)
        ax.legend()

        # Añadir etiquetas de valores encima de las barras
        def agregar_etiquetas(barras):
            for barra in barras:
                altura = barra.get_height()
                ax.annotate('{}'.format(round(altura, 2)),
                            xy=(barra.get_x() + barra.get_width() / 2, altura),
                            xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                            textcoords="offset points",
                            ha='center', va='bottom')

        agregar_etiquetas(barras_teoricas)
        agregar_etiquetas(barras_simuladas)

        plt.show()
        logger.info('Gráficos generados y mostrados')

    def graficar_evolucion_costos(self, todos_costos_diarios):
        """Genera gráficos de la evolución de los costos a lo largo del tiempo de simulación."""
        indicadores = ['Costo de Orden', 'Costo de Mantenimiento', 'Costo de Faltante', 'Costo Total']
        titulos = [
            'Evolución del Costo de Orden a lo Largo del Tiempo de Simulación',
            'Evolución del Costo de Mantenimiento a lo Largo del Tiempo de Simulación',
            'Evolución del Costo de Faltante a lo Largo del Tiempo de Simulación',
            'Evolución del Costo Total a lo Largo del Tiempo de Simulación'
        ]
        archivos = ['costo_orden.png', 'costo_mantenimiento.png', 'costo_faltante.png', 'costo_total.png']

        for i, indicador in enumerate(indicadores):
            plt.figure(figsize=(12, 8))
            for costos_diarios in todos_costos_diarios:
                dias = [costo['Día'] for costo in costos_diarios]
                plt.plot(dias, [costo[indicador] for costo in costos_diarios], alpha=0.5)
            plt.title(titulos[i])
            plt.xlabel('Día')
            plt.ylabel(indicador)
            plt.savefig(archivos[i])
            plt.close()
            logger.info(f'Gráfico de {indicador} generado y guardado como {archivos[i]}')


# Parámetros del modelo ajustados para aumentar la probabilidad de faltante
D = 2000  # Demanda anual
Q = 100  # Cantidad de pedido
R = 10  # Punto de reorden
i = 1  # Costo unitario del producto
k = 50  # Costo de preparación
h = 1  # Costo de mantenimiento por unidad por año
p = 10  # Costo de faltante por unidad
num_runs = 10  # Número de corridas
sim_time = 365  # Tiempo de simulación (días)

# Crear instancia del modelo de inventario
modelo = ModeloInventario(D, Q, R, i, k, h, p)

# Calcular valores teóricos
valores_teoricos = modelo.calcular_valores_teoricos()
print("Valores Teóricos:")
for key, value in valores_teoricos.items():
    print(f"{key}: {value}")

# Realizar múltiples corridas
resultados_simulacion, todos_costos_diarios = modelo.multiple_corridas(num_runs, sim_time)

# Calcular promedios de las corridas
promedios_simulacion = modelo.calcular_promedios(resultados_simulacion)
print("\nPromedios de Simulación:")
for key, value in promedios_simulacion.items():
    print(f"{key}: {value}")

# Generar gráficos comparativos
modelo.graficar_resultados(valores_teoricos, promedios_simulacion)

# Generar gráficos de la evolución de los costos
modelo.graficar_evolucion_costos(todos_costos_diarios)
