import random
import time
import numpy as np
from scipy.stats import chisquare, kstest, norm

class RandomNumber:
    def __init__(self, num_numbers, method, **kwargs):
        self.num_numbers = num_numbers
        self.method = method
        self.kwargs = kwargs
        self.numbers = []

    def generate(self):
        if self.method == 'middle_square':
            self.numbers = self.middle_square_method()
        elif self.method == 'lcg':
            self.numbers = self.linear_congruential_generator()
        elif self.method == 'mersenne_twister':
            self.numbers = self.mersenne_twister()
        elif self.method == 'xorshift':
            self.numbers = self.xorshift()
        else:
            raise ValueError("Método no soportado. Usa 'middle_square', 'lcg', 'mersenne_twister' o 'xorshift'.")
        return self.numbers

    def middle_square_method(self):
        seed = self.kwargs.get('seed', int(time.time()))
        result = []
        for _ in range(self.num_numbers):
            seed = int(str(seed ** 2).zfill(8)[2:6])
            result.append(seed)
        return result

    def linear_congruential_generator(self):
        seed = self.kwargs.get('seed', int(time.time()))
        a = self.kwargs.get('a', 1103515245)
        c = self.kwargs.get('c', 12345)
        m = self.kwargs.get('m', 2**31)
        numbers = []
        x = seed
        for _ in range(self.num_numbers):
            x = (a * x + c) % m
            numbers.append(x)
        return numbers

    def mersenne_twister(self):
        seed = self.kwargs.get('seed', int(time.time()))
        random.seed(seed)
        return [random.randint(0, 2**32 - 1) for _ in range(self.num_numbers)]

    def xorshift(self):
        seed = self.kwargs.get('seed', int(time.time()))
        x = seed
        numbers = []
        for _ in range(self.num_numbers):
            x ^= (x << 13) & 0xFFFFFFFF
            x ^= (x >> 17)
            x ^= (x << 5) & 0xFFFFFFFF
            numbers.append(x)
        return numbers

    def chi_square_test(self):
        observed_freq, _ = np.histogram(self.numbers, bins='auto')
        expected_freq = np.full_like(observed_freq, np.mean(observed_freq))
        observed_sum = observed_freq.sum()
        expected_sum = expected_freq.sum()
        if observed_sum != expected_sum:
            scale_factor = observed_sum / expected_sum
            expected_freq = expected_freq * scale_factor
        chi2_stat, p_value = chisquare(observed_freq, expected_freq)
        return chi2_stat, p_value

    def runs_test(self):
        median = np.median(self.numbers)
        runs, n1, n2 = 0, 0, 0
        for i in range(1, len(self.numbers)):
            if (self.numbers[i] >= median and self.numbers[i-1] < median) or \
               (self.numbers[i] < median and self.numbers[i-1] >= median):
                runs += 1
            if self.numbers[i] >= median:
                n1 += 1
            else:
                n2 += 1
        runs += 1
        expected_runs = ((2 * n1 * n2) / (n1 + n2)) + 1
        std_runs = np.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2)**2 * (n1 + n2 - 1)))
        if std_runs == 0:
            return None, None
        z = (runs - expected_runs) / std_runs
        p_value = 2 * (1 - norm.cdf(abs(z)))
        return z, p_value

    def autocorrelation_test(self, lag=1):
        mean = np.mean(self.numbers)
        var = np.var(self.numbers)
        autocorr = np.correlate(self.numbers - mean, self.numbers - mean, mode='full')[self.num_numbers - 1:] / (var * self.num_numbers)
        return autocorr[lag]

    def ks_test(self):
        d_stat, p_value = kstest(self.numbers, 'uniform', args=(min(self.numbers), max(self.numbers) - min(self.numbers)))
        return d_stat, p_value

# Función para ejecutar pruebas y recolectar resultados
def run_tests(rng):
    chi2_stat, p_value_chi2 = rng.chi_square_test()
    runs_stat, p_value_runs = rng.runs_test()
    autocorr = rng.autocorrelation_test()
    ks_stat, p_value_ks = rng.ks_test()

    return {
        "method": rng.method,
        "chi_square_stat": chi2_stat,
        "p_value_chi2": p_value_chi2,
        "runs_stat": runs_stat,
        "p_value_runs": p_value_runs,
        "autocorr": autocorr,
        "ks_stat": ks_stat,
        "p_value_ks": p_value_ks
    }

num_numbers = 10000  # Ajusta el número de números a generar

methods = ['middle_square', 'lcg', 'mersenne_twister', 'xorshift']
results = []
for method in methods:
    rng = RandomNumber(num_numbers, method)
    numbers = rng.generate()
    result = run_tests(rng)
    results.append(result)

# Crear tabla de resultados
print("\nTabla de resultados:\n")
print(f"{'Generador':<20} {'Chi-Square':<15} {'Runs Test':<15} {'Autocorr':<15} {'K-S Test':<15}")
print("=" * 80)
for result in results:
    chi2 = f"{result['p_value_chi2']:<15.4f}" if result['p_value_chi2'] is not None else "N/A".ljust(15)
    runs = f"{result['p_value_runs']:<15.4f}" if result['p_value_runs'] is not None else "N/A".ljust(15)
    autocorr = f"{result['autocorr']:<15.4f}" if result['autocorr'] is not None else "N/A".ljust(15)
    ks = f"{result['p_value_ks']:<15.4f}" if result['p_value_ks'] is not None else "N/A".ljust(15)

    print(f"{result['method']:<20} {chi2} {runs} {autocorr} {ks}")
