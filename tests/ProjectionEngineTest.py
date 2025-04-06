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

        # Use enough years and ensure each data series has enough variability
        years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']

        # Create income statement with meaningful variation in the data
        income_data = {}
        for i, year in enumerate(years):
            # Create data with clear trends and variability to ensure valid correlations
            revenue = 100 + i * 20
            cogs = revenue * (0.45 + 0.01 * i)  # COGS as % of revenue with slight trend
            rnd = revenue * (0.08 + 0.005 * i)  # R&D as % of revenue with slight trend
            sga = revenue * (0.20 - 0.003 * i)  # SG&A as % of revenue with slight trend

            income_data[year] = [revenue, cogs, rnd, sga]

        income_index = ['Revenue', 'Cost of Goods Sold', 'R&D Exp.', 'Selling General & Admin Exp.']
        enterprise.income_statement = pd.DataFrame(income_data, index=income_index)

        # Create balance sheet data with consistent relationship to income data
        balance_data = {}
        for i, year in enumerate(years):
            # PP&E typically correlates with revenue
            nppe = income_data[year][0] * 0.7 + i * 5  # 70% of revenue plus growth
            balance_data[year] = [nppe]

        balance_index = ['Net Property Plant & Equipment']
        enterprise.balance_sheet = pd.DataFrame(balance_data, index=balance_index)

        # Create cash flow statement data
        cf_data = {}
        for i, year in enumerate(years):
            # Depreciation typically around 5-10% of PP&E
            depreciation = balance_data[year][0] * (0.08 + 0.003 * i)  # 8% of PP&E with slight increase
            cf_data[year] = [depreciation]

        cf_index = ['Depreciation & Amort.']
        enterprise.cash_flow_statement = pd.DataFrame(cf_data, index=cf_index)

        return enterprise

    def test_calc_correlation(self):
        # Test the correlation calculation
        self.projection_engine.calc_correlation()

        # Verify the correlation matrix has the right shape (5x5 for the 5 metrics)
        self.assertIsInstance(self.projection_engine.correlation_matrix, np.ndarray)
        self.assertEqual(self.projection_engine.correlation_matrix.shape, (5, 5))

        # Check for NaN values before proceeding with other assertions
        nan_count = np.isnan(self.projection_engine.correlation_matrix).sum()
        self.assertEqual(nan_count, 0, "Correlation matrix contains NaN values")

        # Verify the diagonal elements are 1.0 (correlation with self)
        for i in range(5):
            self.assertAlmostEqual(self.projection_engine.correlation_matrix[i, i], 1.0)

        # Verify all correlation coefficients are in a valid range [-1, 1]
        for i in range(5):
            for j in range(5):
                self.assertTrue(-1.0 <= self.projection_engine.correlation_matrix[i, j] <= 1.0)

        # Verify symmetry of the correlation matrix
        for i in range(5):
            for j in range(5):
                self.assertAlmostEqual(
                    self.projection_engine.correlation_matrix[i, j],
                    self.projection_engine.correlation_matrix[j, i]
                )

    def test_calc_correlation_with_empty_data(self):
        # Test with empty data arrays
        enterprise = Enterprise(name='Test', ticker='TEST', fdso=0, debt_value=0.0)

        # Create empty DataFrames with correct structure
        enterprise.income_statement = pd.DataFrame({}, index=['Revenue', 'Cost of Goods Sold',
                                                              'R&D Exp.', 'Selling General & Admin Exp.'])
        enterprise.balance_sheet = pd.DataFrame({}, index=['Net Property Plant & Equipment'])
        enterprise.cash_flow_statement = pd.DataFrame({}, index=['Depreciation & Amort.'])

        projection_engine = ProjectionEngine(enterprise)

        # Should raise ValueError with empty data
        with self.assertRaises(ValueError):
            projection_engine.calc_correlation()


if __name__ == '__main__':
    unittest.main()