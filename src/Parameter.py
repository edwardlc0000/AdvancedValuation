
import numpy as np

class Parameter:
    def __init__(self, data: np.ndarray, distribution: str = 'Normal'):
        self.data: np.ndarray = data
        self.mean: np.floating = np.mean(data)
        self.std: np.floating = np.std(data)
        self.distribution: str = distribution
