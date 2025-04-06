
import numpy as np

class Parameter:

    def __init__(self, data: np.ndarray, std: np.floating = None, distribution: str = 'Normal'):
        self.data: np.ndarray = data
        self.mean: np.floating = np.mean(data)
        if std is None:
            self.std: np.floating = np.std(data)
        else:
            self.std: np.floating = std
        self.distribution: str = distribution
