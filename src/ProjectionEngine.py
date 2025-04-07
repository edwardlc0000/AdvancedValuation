
import numpy as np

from .Enterprise import Enterprise
from .Parameter import Parameter
from .ProjectionUtils import (
    calc_revenue_growth,
    calc_cogs_revenue,
    calc_r_and_d_revenue,
    calc_sga_revenue,
    calc_da_prior_nppe,
    calc_nwc_revenue,
    calc_net_capex_revenue,
    calc_ucoe,
    calc_reinvestment_rate,
    calc_growth
)

class ProjectionEngine:

    def __init__(self, enterprise: Enterprise,
                 revenue_growth_e: np.ndarray = np.ndarray(0),
                 cogs_revenue_e: np.ndarray = np.ndarray(0),
                 sga_revenue_e: np.ndarray = np.ndarray(0),
                 r_and_d_revenue_e: np.ndarray = np.ndarray(0),
                 da_nppe_e: np.ndarray = np.ndarray(0),
                 nwc_revenue_e: np.ndarray = np.ndarray(0),
                 net_capex_revenue_e: np.ndarray = np.ndarray(0)):
        self.correlation_matrix: np.ndarray = None
        self.enterprise: Enterprise = enterprise
        self.params: dict = {}

        # Check for empty data
        if (self.enterprise.income_statement.empty or
                self.enterprise.balance_sheet.empty or
                self.enterprise.cash_flow_statement.empty):
            raise ValueError("Cannot calculate correlation with empty data")

        # Initialize all parameters at once instead of individual assignments
        param_functions = {
            'revenue_growth_a': lambda: calc_revenue_growth(
                self.enterprise.income_statement.loc['Revenues']),

            'cogs_revenue_a': lambda: calc_cogs_revenue(
                self.enterprise.income_statement.loc['Revenues'],
                self.enterprise.income_statement.loc['Cost of Goods Sold']),

            'r_and_d_revenue_a': lambda: calc_r_and_d_revenue(
                self.enterprise.income_statement.loc['Revenues'],
                self.enterprise.income_statement.loc['R&D Exp.']),

            'sga_revenue_a': lambda: calc_sga_revenue(
                self.enterprise.income_statement.loc['Revenues'],
                self.enterprise.income_statement.loc['Selling General & Admin Exp.']),

            'da_nppe_a': lambda: calc_da_prior_nppe(
                self.enterprise.cash_flow_statement.loc['Depreciation & Amort.'],
                self.enterprise.balance_sheet.loc['Net Property Plant & Equipment']),

            'nwc_revenue_a': lambda: calc_nwc_revenue(
                self.enterprise.income_statement.loc['Revenues'],
                self.enterprise.balance_sheet.loc['Total Cash & ST Investments'],
                self.enterprise.balance_sheet.loc['Total Current Assets'],
                self.enterprise.balance_sheet.loc['Current Portion of Long Term Debt'],
                self.enterprise.balance_sheet.loc['Total Current Liabilities']),

            'net_capex_revenue_a': lambda: calc_net_capex_revenue(
                self.enterprise.income_statement.loc['Revenues'],
                self.enterprise.cash_flow_statement.loc['Cash from Investing'],
                self.enterprise.cash_flow_statement.loc['Depreciation & Amort.'])
        }

        # Run calculations and store results in a single params dictionary
        for param_name, calculate_func in param_functions.items():
            try:
                self.params[param_name] = Parameter(calculate_func())
            except (ValueError, ZeroDivisionError, IndexError) as e:
                print(f"Warning: Could not calculate {param_name}: {e}")

        self.params['revenue_growth_e'] = Parameter(data=revenue_growth_e,
                                                    std=self.params['revenue_growth_a'].std)
        self.params['cogs_revenue_e'] = Parameter(data=cogs_revenue_e,
                                                  std=self.params['cogs_revenue_a'].std)
        self.params['r_and_d_revenue_e'] = Parameter(data=r_and_d_revenue_e,
                                                     std=self.params['r_and_d_revenue_a'].std)
        self.params['sga_revenue_e'] = Parameter(data=sga_revenue_e,
                                                 std=self.params['sga_revenue_a'].std)
        self.params['da_nppe_e'] = Parameter(data=da_nppe_e,
                                             std=self.params['da_nppe_a'].std)
        self.params['nwc_revenue_e'] = Parameter(data=nwc_revenue_e,
                                                 std=self.params['nwc_revenue_a'].std)
        self.params['net_capex_revenue_e'] = Parameter(data=net_capex_revenue_e,
                                                       std=self.params['net_capex_revenue_a'].std)

    def calc_correlation(self) -> None:
        if (self.enterprise.income_statement.empty or
            self.enterprise.balance_sheet.empty or
            self.enterprise.cash_flow_statement.empty):
            raise ValueError("Cannot calculate correlation with empty data")

        revenue_growth: np.ndarray = self.params['revenue_growth_a'].data
        cogs_revenue: np.ndarray = self.params['cogs_revenue_a'].data
        r_and_d_revenue: np.ndarray = self.params['r_and_d_revenue_a'].data
        sga_revenue: np.ndarray = self.params['sga_revenue_a'].data
        da_nppe: np.ndarray = self.params['da_nppe_a'].data
        nwc_revenue: np.ndarray = self.params['nwc_revenue_a'].data
        net_capex_revenue: np.ndarray = self.params['net_capex_revenue_a'].data

        data_matrix: np.ndarray = np.vstack([revenue_growth,
                                             cogs_revenue,
                                             sga_revenue,
                                             r_and_d_revenue,
                                             da_nppe,
                                             nwc_revenue,
                                             net_capex_revenue])
        self.correlation_matrix = np.corrcoef(data_matrix)

    def project_stmt(self) -> None:
        self.project_revenue()
        self.project_cogs()
        self.project_sga()
        self.project_r_and_d()
        self.project_fixed_assets()
        self.project_net_working_capital()

    def project_revenue(self) -> None:
        revenue0: float = self.enterprise.income_statement.loc['Revenues'].index[-1]
        for growth_rate in self.params['revenue_growth_e'].data:
            revenue = revenue0 * (1 + growth_rate)
            self.params['revenues_e'].append(revenue)
            revenue0 = revenue

    def project_cogs(self) -> None:
        self.params['cogs_e'] = np.multiply(self.params['revenues_e'].data,
                                            self.params['cogs_revenue_e'].data)

    def project_sga(self) -> None:
        self.params['sga_e'] = np.multiply(self.params['revenues_e'].data,
                                           self.params['sga_revenue_e'].data)

    def project_r_and_d(self) -> None:
        self.params['r_and_d_e'] = np.multiply(self.params['revenues_e'].data,
                                               self.params['r_and_d_revenue_e'].data)

    def project_fixed_assets(self) -> None:
        self.params['da_e'] = Parameter(np.ndarray(0))
        self.params['nppe_e'] = Parameter(np.ndarray(0))
        self.params['capex_e'] = Parameter(np.ndarray(0))

    def project_net_working_capital(self) -> None:
        pass