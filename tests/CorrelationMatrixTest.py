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
        enterprise = Enterprise(name='Test Corp',
                                ticker='TEST',
                                fdso=100,
                                debt_value=0.0)

        # Create consistent data across all years to avoid NaN values
        # Use 7 years of data to ensure enough data points for correlation
        years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']

        # Creating income statement data
        # Ensure values change over time to have meaningful correlations
        # Using synthetic data with clear patterns
        income_data = {
            'Revenues': [100, 110, 121, 133, 146.3, 161, 177.1],
            'Cost of Goods Sold': [60, 65, 71.5, 78.6, 86.5, 95.1, 104.6],
            'R&D Exp.': [10, 11, 12.1, 13.3, 14.6, 16.1, 17.7],
            'Selling General & Admin Exp.': [15, 16.5, 18.2, 20, 22, 24.2, 26.6]
        }

        # Transpose the data to match the expected format (years as columns)
        income_df = pd.DataFrame(income_data)
        income_df.index = years
        enterprise.income_statement = income_df.T  # Transpose to have rows as metrics, columns as years

        # Creating balance sheet data with consistent patterns
        balance_data = {
            'Net Property Plant & Equipment': [70, 77, 84.7, 93.2, 102.5, 112.7, 124],
            'Total Cash & ST Investments': [20, 22, 24.2, 26.6, 29.3, 32.2, 35.4],
            'Total Current Assets': [40, 44, 48.4, 53.2, 58.5, 64.4, 70.8],
            'Current Portion of Long Term Debt': [5, 5.5, 6.1, 6.7, 7.3, 8.1, 8.9],
            'Total Current Liabilities': [30, 33, 36.3, 39.9, 43.9, 48.3, 53.1]
        }

        balance_df = pd.DataFrame(balance_data)
        balance_df.index = years
        enterprise.balance_sheet = balance_df.T

        # Creating cash flow data with consistent patterns
        cf_data = {
            'Depreciation & Amort.': [7, 7.7, 8.5, 9.3, 10.3, 11.3, 12.4],
            'Cash from Investing': [-12, -13.2, -14.5, -16, -17.6, -19.3, -21.3]
        }

        cf_df = pd.DataFrame(cf_data)
        cf_df.index = years
        enterprise.cash_flow_statement = cf_df.T

        return enterprise

    def test_calc_correlation(self):
        """Test that the correlation calculation works properly."""
        # Call the method to be tested
        self.projection_engine.calc_correlation()

        # Verify the correlation matrix has the right shape for the metrics it's using
        self.assertIsInstance(self.projection_engine.correlation_matrix, np.ndarray)

        # Print the parameters for debugging
        print("Parameters in projection engine:")
        for key, value in self.projection_engine.params.items():
            print(f"  {key}: {value}")

        # Check if correlation matrix has the proper shape
        shape = self.projection_engine.correlation_matrix.shape
        self.assertEqual(len(shape), 2, "Correlation matrix should be 2-dimensional")
        self.assertEqual(shape[0], shape[1], "Correlation matrix should be square")

        # Print the correlation matrix for debugging
        print("Correlation matrix shape:", shape)
        print(self.projection_engine.correlation_matrix)

        # Verify no NaN values in the correlation matrix
        if np.isnan(self.projection_engine.correlation_matrix).any():
            nan_indices = np.argwhere(np.isnan(self.projection_engine.correlation_matrix))
            print(f"NaN found at indices: {nan_indices}")

        self.assertFalse(np.isnan(self.projection_engine.correlation_matrix).any(),
                         "Correlation matrix should not contain NaN values")

        # Check that diagonal elements are 1.0 (correlation of a variable with itself)
        for i in range(shape[0]):
            self.assertAlmostEqual(
                self.projection_engine.correlation_matrix[i, i],
                1.0,
                msg=f"Diagonal element at position {i},{i} should be 1.0"
            )

        # Check that all correlation values are in the valid range [-1, 1]
        self.assertTrue(
            (self.projection_engine.correlation_matrix >= -1.0).all() and
            (self.projection_engine.correlation_matrix <= 1.0).all(),
            "All correlation values should be between -1.0 and 1.0"
        )

        # Check symmetry of correlation matrix
        for i in range(shape[0]):
            for j in range(shape[0]):
                self.assertAlmostEqual(
                    self.projection_engine.correlation_matrix[i, j],
                    self.projection_engine.correlation_matrix[j, i],
                    msg=f"Correlation matrix should be symmetric: [{i},{j}] should equal [{j},{i}]"
                )

    def test_calc_correlation_with_empty_data(self):
        """Test that correlation calculation properly handles empty data."""
        # Create Enterprise object with empty data frames
        enterprise = Enterprise(name='Test', ticker='TEST', fdso=0, debt_value=0.0)

        # Create empty DataFrames with the expected indexes
        income_index = ['Revenues', 'Cost of Goods Sold', 'R&D Exp.', 'Selling General & Admin Exp.']
        enterprise.income_statement = pd.DataFrame({}, index=income_index)

        balance_index = [
            'Net Property Plant & Equipment',
            'Total Cash & ST Investments',
            'Total Current Assets',
            'Current Portion of Long Term Debt',
            'Total Current Liabilities'
        ]
        enterprise.balance_sheet = pd.DataFrame({}, index=balance_index)

        cf_index = ['Depreciation & Amort.', 'Cash from Investing']
        enterprise.cash_flow_statement = pd.DataFrame({}, index=cf_index)

        # Creating a ProjectionEngine with empty data should raise ValueError
        with self.assertRaises(ValueError):
            ProjectionEngine(enterprise)

    def test_params_initialization(self):
        """Test that parameters are properly initialized."""
        # Check that params dictionary is created
        self.assertIsInstance(self.projection_engine.params, dict)

        # Check that params dictionary is not empty
        self.assertTrue(len(self.projection_engine.params) > 0,
                        "Params dictionary should not be empty")


if __name__ == '__main__':
    unittest.main()