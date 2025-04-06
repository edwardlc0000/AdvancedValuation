import sys
import os
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Enterprise import Enterprise
from src.ProjectionEngine import ProjectionEngine


class TestProjectionEngine(unittest.TestCase):

    def setUp(self):
        # Create a mock Enterprise object with test data
        self.enterprise = self._create_mock_enterprise()
        self.projection_engine = ProjectionEngine(self.enterprise)


    def _create_mock_enterprise(self):
        # Create a mock Enterprise object with controlled test data
        enterprise = Enterprise(name='International Business Machines',
                                ticker='IBM',
                                fdso=100,
                                debt_value=0.0)

        # Populate with sample data - using index properly
        data = {
            '2018': [100, 10],
            '2019': [110, 12],
            '2020': [125, 15],
            '2021': [140, 18],
            '2022': [160, 22]
        }
        index = ['Revenue', 'R&D Exp.']
        enterprise.income_statement = pd.DataFrame(data, index=index)

        return enterprise

    def test_calc_correlation(self):
        # Test the correlation calculation
        self.projection_engine.calc_correlation()

        # Verify the correlation matrix has the right shape
        self.assertIsInstance(self.projection_engine.correlation_matrix, np.ndarray)
        self.assertEqual(self.projection_engine.correlation_matrix.shape, (2, 2))

        # Verify the diagonal elements are 1.0 (correlation with self)
        self.assertAlmostEqual(self.projection_engine.correlation_matrix[0, 0], 1.0)
        self.assertAlmostEqual(self.projection_engine.correlation_matrix[1, 1], 1.0)

        # Verify the correlation coefficient is in a valid range [-1, 1]
        self.assertTrue(-1.0 <= self.projection_engine.correlation_matrix[0, 1] <= 1.0)
        self.assertTrue(-1.0 <= self.projection_engine.correlation_matrix[1, 0] <= 1.0)

        # Verify symmetry
        self.assertAlmostEqual(
            self.projection_engine.correlation_matrix[0, 1],
            self.projection_engine.correlation_matrix[1, 0]
        )

    def test_calc_correlation_with_empty_data(self):
        # Test with empty data arrays
        enterprise = Enterprise(name='Test', ticker='TEST', fdso=0, debt_value=0.0)

        # Create empty DataFrame with correct structure
        data = {}  # Empty data
        index = ['Revenue', 'R&D Exp.']
        enterprise.income_statement = pd.DataFrame(data, index=index)

        projection_engine = ProjectionEngine(enterprise)

        # Should handle empty arrays without errors
        with self.assertRaises(ValueError):
            projection_engine.calc_correlation()

if __name__ == '__main__':
    unittest.main()
