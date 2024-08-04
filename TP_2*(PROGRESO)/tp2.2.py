import numpy as np
from scipy.stats import chisquare, kstest


class RandomNumberGenerator:
    def __init__(self, dist_name, **kwargs):
        self.dist_name = dist_name
        self.kwargs = kwargs
        self.numbers = []

    def generate(self, size=1000):
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
        a = self.kwargs.get('a', 0)
        b = self.kwargs.get('b', 1)
        return np.random.uniform(a, b, size)

    def _generate_exponential(self, size):
        scale = self.kwargs.get('scale', 1)
        return np.random.exponential(scale, size)

    def _generate_normal(self, size):
        mu = self.kwargs.get('mu', 0)
        sigma = self.kwargs.get('sigma', 1)
        return np.random.normal(mu, sigma, size)

    def _generate_pascal(self, size):
        n = self.kwargs.get('n', 1)
        p = self.kwargs.get('p', 0.5)
        return np.random.negative_binomial(n, p, size)

    def _generate_binomial(self, size):
        n = self.kwargs.get('n', 1)
        p = self.kwargs.get('p', 0.5)
        return np.random.binomial(n, p, size)

    def _generate_poisson(self, size):
        lam = self.kwargs.get('lam', 1)
        return np.random.poisson(lam, size)

    def _generate_empirical_discrete(self, size):
        values = self.kwargs.get('values', [0, 1])
        probabilities = self.kwargs.get('probabilities', [0.5, 0.5])
        return np.random.choice(values, size=size, p=probabilities)
    def _expected_frequencies(self, size, bins):
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
        else:
            raise ValueError(f"Distribución {self.dist_name} no soportada para la prueba de Chi-Cuadrado")

        return expected_freq

    def chi_square_test(self):
        observed_freq, bins = np.histogram(self.numbers, bins='auto', density=False)
        expected_freq = self._expected_frequencies(len(self.numbers), bins)
        chi2_stat, p_value = chisquare(observed_freq, expected_freq)
        return chi2_stat, p_value

    def ks_test(self):
        d_stat, p_value = kstest(self.numbers, 'uniform')
        return d_stat, p_value

distributions = [
    ('uniform', {'a': 0, 'b': 1}),
    ('exponential', {'scale': 1}),
    ('normal', {'mu': 0, 'sigma': 1}),
    ('pascal', {'n': 10, 'p': 0.5}),
    ('binomial', {'n': 10, 'p': 0.5}),
    ('poisson', {'lam': 5}),
    ('empirical_discrete', {'values': [0, 1], 'probabilities': [0.5, 0.5]})
]

for dist_name, params in distributions:
    rng = RandomNumberGenerator(dist_name, **params)
    numbers = rng.generate(size=1000)
    d_stat, p_value = rng.ks_test()
    print(f"{dist_name} - Kolmogorov-Smirnov Test: Statistic={d_stat}, p-value={p_value}")

