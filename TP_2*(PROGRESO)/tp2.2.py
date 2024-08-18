import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chisquare, kstest


class RandomNumberGenerator:
    def __init__(self, dist_name, **kwargs):
        self.dist_name = dist_name
        self.kwargs = kwargs
        self.numbers = []

    def generate(self, size=1000):
        """Genera números pseudoaleatorios según la distribución especificada."""
        distribution_methods = {
            'uniform': self._generate_uniform,
            'exponential': self._generate_exponential,
            'normal': self._generate_normal,
            'pascal': self._generate_pascal,
            'binomial': self._generate_binomial,
            'poisson': self._generate_poisson,
            'empirical_discrete': self._generate_empirical_discrete
        }

        if self.dist_name in distribution_methods:
            self.numbers = distribution_methods[self.dist_name](size)
        else:
            raise ValueError(f"Distribución {self.dist_name} no soportada.")
        return self.numbers

    def _generate_uniform(self, size):
        """Genera números según una distribución uniforme."""
        a = self.kwargs.get('a', 0)
        b = self.kwargs.get('b', 1)
        return np.random.uniform(a, b, size)

    def _generate_exponential(self, size):
        """Genera números según una distribución exponencial."""
        scale = self.kwargs.get('scale', 1)
        return np.random.exponential(scale, size)

    def _generate_normal(self, size):
        """Genera números según una distribución normal."""
        mu = self.kwargs.get('mu', 0)
        sigma = self.kwargs.get('sigma', 1)
        return np.random.normal(mu, sigma, size)

    def _generate_pascal(self, size):
        """Genera números según una distribución Pascal (Binomial Negativa)."""
        n = self.kwargs.get('n', 1)
        p = self.kwargs.get('p', 0.5)
        return np.random.negative_binomial(n, p, size)

    def _generate_binomial(self, size):
        """Genera números según una distribución binomial."""
        n = self.kwargs.get('n', 1)
        p = self.kwargs.get('p', 0.5)
        return np.random.binomial(n, p, size)

    def _generate_poisson(self, size):
        """Genera números según una distribución de Poisson."""
        lam = self.kwargs.get('lam', 1)
        return np.random.poisson(lam, size)

    def _generate_empirical_discrete(self, size):
        """Genera números según una distribución empírica discreta."""
        values = self.kwargs.get('values', [0, 1])
        probabilities = self.kwargs.get('probabilities', [0.5, 0.5])
        return np.random.choice(values, size=size, p=probabilities)

    def _expected_frequencies(self, size, bins):
        """Calcula las frecuencias esperadas para la prueba de Chi-Cuadrado."""
        if self.dist_name == 'uniform':
            expected_freq, _ = np.histogram(np.random.uniform(self.kwargs.get('a', 0), self.kwargs.get('b', 1), size),
                                            bins=bins)
        elif self.dist_name == 'normal':
            expected_freq, _ = np.histogram(
                np.random.normal(self.kwargs.get('mu', 0), self.kwargs.get('sigma', 1), size), bins=bins)
        elif self.dist_name == 'pascal':
            expected_freq, _ = np.histogram(
                np.random.negative_binomial(self.kwargs.get('n', 1), self.kwargs.get('p', 0.5), size), bins=bins)
        elif self.dist_name == 'binomial':
            expected_freq, _ = np.histogram(
                np.random.binomial(self.kwargs.get('n', 1), self.kwargs.get('p', 0.5), size), bins=bins)
        elif self.dist_name == 'poisson':
            expected_freq, _ = np.histogram(np.random.poisson(self.kwargs.get('lam', 1), size), bins=bins)
        elif self.dist_name == 'empirical_discrete':
            values = self.kwargs.get('values', [0, 1])
            probabilities = self.kwargs.get('probabilities', [0.5, 0.5])
            expected_freq, _ = np.histogram(np.random.choice(values, size=size, p=probabilities), bins=bins)
        elif self.dist_name == 'exponential':
            scale = self.kwargs.get('scale', 1)
            expected_freq, _ = np.histogram(np.random.exponential(scale, size), bins=bins)
        else:
            raise ValueError(f"Distribución {self.dist_name} no soportada para la prueba de Chi-Cuadrado")

        # Evitar divisiones por cero asegurando que ninguna frecuencia esperada sea cero
        expected_freq = np.maximum(expected_freq, 1e-8)
        return expected_freq

    def chi_square_test(self):
        """Realiza la prueba de Chi-Cuadrado para comparar las frecuencias observadas con las esperadas."""
        observed_freq, bins = np.histogram(self.numbers, bins='auto', density=False)
        expected_freq = self._expected_frequencies(len(self.numbers), bins)

        # Normalizar las frecuencias para asegurarse de que ambas sumen lo mismo
        observed_freq = observed_freq * (expected_freq.sum() / observed_freq.sum())

        chi2_stat, p_value = chisquare(observed_freq, expected_freq)
        return chi2_stat, p_value

    def ks_test(self):
        """Realiza la prueba de Kolmogorov-Smirnov específica para cada distribución."""
        if self.dist_name == 'uniform':
            d_stat, p_value = kstest(self.numbers, 'uniform',
                                     args=(self.kwargs.get('a', 0), self.kwargs.get('b', 1) - self.kwargs.get('a', 0)))
        elif self.dist_name == 'exponential':
            d_stat, p_value = kstest(self.numbers, 'expon', args=(0, self.kwargs.get('scale', 1)))
        elif self.dist_name == 'normal':
            d_stat, p_value = kstest(self.numbers, 'norm', args=(self.kwargs.get('mu', 0), self.kwargs.get('sigma', 1)))
        elif self.dist_name == 'pascal':
            n, p = self.kwargs.get('n', 1), self.kwargs.get('p', 0.5)
            d_stat, p_value = kstest(self.numbers, 'nbinom', args=(n, p))
        elif self.dist_name == 'binomial':
            n, p = self.kwargs.get('n', 1), self.kwargs.get('p', 0.5)
            d_stat, p_value = kstest(self.numbers, 'binom', args=(n, p))
        elif self.dist_name == 'poisson':
            d_stat, p_value = kstest(self.numbers, 'poisson', args=(self.kwargs.get('lam', 1),))
        elif self.dist_name == 'empirical_discrete':
            raise ValueError(f"Distribución {self.dist_name} no soportada para la prueba K-S")
        else:
            raise ValueError(f"Distribución {self.dist_name} no soportada para la prueba K-S")
        return d_stat, p_value

    def custom_empirical_ks_test(self):
        """Implementa una prueba personalizada para distribuciones empíricas discretas."""
        values, counts = np.unique(self.numbers, return_counts=True)
        empirical_cdf = np.cumsum(counts) / len(self.numbers)
        theoretical_cdf = np.cumsum(self.kwargs.get('probabilities', [0.5, 0.5]))

        d_stat = np.max(np.abs(empirical_cdf - theoretical_cdf))
        # Aquí no se puede calcular un p-value exacto de manera directa sin simulación
        return d_stat, None


# Definición de las distribuciones a ser generadas y testeadas
distributions = [
    ('uniform', {'a': 0, 'b': 1}),
    ('exponential', {'scale': 1}),
    ('normal', {'mu': 0, 'sigma': 1}),
    ('pascal', {'n': 10, 'p': 0.5}),
    ('binomial', {'n': 10, 'p': 0.5}),
    ('poisson', {'lam': 5}),
    ('empirical_discrete', {'values': [0, 1], 'probabilities': [0.5, 0.5]})
]

# Generación y testeo de números para cada distribución
for dist_name, params in distributions:
    rng = RandomNumberGenerator(dist_name, **params)
    numbers = rng.generate(size=1000)

    if dist_name == 'empirical_discrete':
        # Prueba personalizada para distribuciones empíricas discretas
        d_stat, p_value = rng.custom_empirical_ks_test()
        print(f"{dist_name} - Custom Empirical K-S Test: Statistic={d_stat}, p-value={p_value}")
    else:
        # Prueba de Kolmogorov-Smirnov
        d_stat, p_value = rng.ks_test()
        print(f"{dist_name} - Kolmogorov-Smirnov Test: Statistic={d_stat}, p-value={p_value}")

    # Prueba de Chi-Cuadrado
    chi2_stat, p_value_chi2 = rng.chi_square_test()
    print(f"{dist_name} - Chi-Square Test: Statistic={chi2_stat}, p-value={p_value_chi2}")

    # Visualización de la distribución
    plt.figure()
    plt.hist(numbers, bins=30, density=True, alpha=0.6, color='g')
    plt.title(f'{dist_name.capitalize()} Distribution')
    plt.show()
