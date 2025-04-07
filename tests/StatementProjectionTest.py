import unittest
import numpy as np
import pandas as pd
from src.ProjectionEngine import ProjectionEngine
from src.Enterprise import Enterprise


class TestProjectionEngine(unittest.TestCase):
    def setUp(self):
        self.enterprise = self._create_mock_enterprise()
        self.projection_engine = ProjectionEngine(self.enterprise,
                                                  revenue_growth_e=np.array([0.1, 0.1, 0.1]),
                                                  cogs_revenue_e=np.array([0.6, 0.6, 0.6]),
                                                  sga_revenue_e=np.array([0.15, 0.15, 0.15]),
                                                  r_and_d_revenue_e=np.array([0.1, 0.1, 0.1]),
                                                  da_nppe_e=np.array([0.1, 0.1, 0.1]),
                                                  nwc_revenue_e=np.array([0.2, 0.2, 0.2]),
                                                  net_capex_revenue_e=np.array([0.05, 0.05, 0.05]))

    # Reusing your provided mock enterprise creator
    def _create_mock_enterprise(self):
        enterprise = Enterprise(name='Test Corp',
                                ticker='TEST',
                                fdso=100,
                                debt_value=0.0)

        years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']

        income_data = {
            'Revenues': [100, 110, 121, 133, 146.3, 161, 177.1],
            'Cost of Goods Sold': [60, 65, 71.5, 78.6, 86.5, 95.1, 104.6],
            'R&D Exp.': [10, 11, 12.1, 13.3, 14.6, 16.1, 17.7],
            'Selling General & Admin Exp.': [15, 16.5, 18.2, 20, 22, 24.2, 26.6]
        }
        income_df = pd.DataFrame(income_data, index=years).T
        enterprise.income_statement = income_df

        balance_data = {
            'Net Property Plant & Equipment': [70, 77, 84.7, 93.2, 102.5, 112.7, 124],
            'Total Cash & ST Investments': [20, 22, 24.2, 26.6, 29.3, 32.2, 35.4],
            'Total Current Assets': [40, 44, 48.4, 53.2, 58.5, 64.4, 70.8],
            'Current Portion of Long Term Debt': [5, 5.5, 6.1, 6.7, 7.3, 8.1, 8.9],
            'Total Current Liabilities': [30, 33, 36.3, 39.9, 43.9, 48.3, 53.1]
        }
        balance_df = pd.DataFrame(balance_data, index=years).T
        enterprise.balance_sheet = balance_df

        cf_data = {
            'Depreciation & Amort.': [7, 7.7, 8.5, 9.3, 10.3, 11.3, 12.4],
            'Cash from Investing': [-12, -13.2, -14.5, -16, -17.6, -19.3, -21.3]
        }
        cf_df = pd.DataFrame(cf_data, index=years).T
        enterprise.cash_flow_statement = cf_df

        return enterprise

    def test_project_revenue(self):
        projected_revenue = self.projection_engine.project_revenue()
        expected_revenue = [177.1 * 1.1, 177.1 * (1.1 ** 2), 177.1 * (1.1 ** 3)]
        np.testing.assert_allclose(projected_revenue, expected_revenue, rtol=1e-5,
                                   err_msg="Projected Revenues don't match expected growth values.")

    def test_project_cogs(self):
        self.projection_engine.revenues_e.append(self.projection_engine.project_revenue())
        projected_cogs = self.projection_engine.project_cogs()
        projected_revenue = [177.1 * 1.1, 177.1 * (1.1 ** 2), 177.1 * (1.1 ** 3)]
        expected_cogs = [rev * 0.6 for rev in projected_revenue]
        np.testing.assert_allclose(projected_cogs, expected_cogs, rtol=1e-5,
                                   err_msg="Projected COGS don't match expected proportional values.")

    def test_project_sga(self):
        self.projection_engine.revenues_e.append(self.projection_engine.project_revenue())
        projected_sga = self.projection_engine.project_sga()
        projected_revenue = [177.1 * 1.1, 177.1 * (1.1 ** 2), 177.1 * (1.1 ** 3)]
        expected_sga = [rev * 0.15 for rev in projected_revenue]
        np.testing.assert_allclose(projected_sga, expected_sga, rtol=1e-5,
                                   err_msg="Projected SG&A don't match expected proportional values.")

    def test_project_r_and_d(self):
        self.projection_engine.revenues_e.append(self.projection_engine.project_revenue())
        projected_r_and_d = self.projection_engine.project_r_and_d()
        projected_revenue = [177.1 * 1.1, 177.1 * (1.1 ** 2), 177.1 * (1.1 ** 3)]
        expected_r_and_d = [rev * 0.1 for rev in projected_revenue]
        np.testing.assert_allclose(projected_r_and_d, expected_r_and_d, rtol=1e-5,
                                   err_msg="Projected R&D don't match expected proportional values.")

    def test_project_fixed_assets(self):
        self.projection_engine.revenues_e.append(self.projection_engine.project_revenue())
        projected_fixed_assets = self.projection_engine.project_fixed_assets()
        # simplified example for expected fixed-assets calculation
        self.assertEqual(len(projected_fixed_assets), 3)

    def test_project_net_working_capital(self):
        self.projection_engine.revenues_e.append(self.projection_engine.project_revenue())
        projected_nwc = self.projection_engine.project_change_net_working_capital()
        expected_nwc = [47.762, 3.8962, 4.28582]
        np.testing.assert_allclose(projected_nwc, expected_nwc, rtol=1e-5,
                                   err_msg="Projected NWC doesn't match expected proportional values.")

    def test_project_stmt(self):
        # Run projection twice, saving outputs each iteration
        for _ in range(2):
            self.projection_engine.project_stmt()

        # Assert correct storage structure:
        self.assertEqual(len(self.projection_engine.revenues_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.cogs_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.sga_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.r_and_d_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.da_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.capex_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.nppe_e), 2,
                         "The container should have exactly two projected statements.")
        self.assertEqual(len(self.projection_engine.change_nwc_e), 2,
                         "The container should have exactly two projected statements.")


if __name__ == '__main__':
    unittest.main()