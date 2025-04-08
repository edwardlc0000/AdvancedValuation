
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

        self.revenues_e: list[list] = []
        self.cogs_e: list[list]  = []
        self.gross_profit_e: list[list]  = []
        self.sga_e: list[list]  = []
        self.r_and_d_e: list[list]  = []
        self.ebitda_e: list[list]  = []
        self.da_e: list[list]  = []
        self.ebit_e: list[list]  = []
        self.tax_e: list[list]  = []
        self.capex_e: list[list]  = []
        self.nppe_e: list[list]  = []
        self.change_nwc_e: list[list]  = []
        self.fcf_e: list[list]  = []
        self.pv_fcf_e: list[list]  = []

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
        self.revenues_e.append(self.project_revenue())
        self.cogs_e.append(self.project_cogs())
        self.gross_profit_e.append(self.project_gross_profit())
        self.sga_e.append(self.project_sga())
        self.r_and_d_e.append(self.project_r_and_d())
        self.ebitda_e.append(self.project_ebitda())
        fixed_assets = self.project_fixed_assets()
        self.da_e.append(fixed_assets[0])
        self.ebit_e.append(self.project_ebit())
        self.tax_e.append(self.project_tax())
        self.capex_e.append(fixed_assets[1])
        self.nppe_e.append(fixed_assets[2])
        self.change_nwc_e.append(self.project_change_net_working_capital())
        self.fcf_e.append(self.project_fcf())

    def project_revenue(self) -> list:
        iter_rev_e: list = []
        revenue0: float = self.enterprise.income_statement.loc['Revenues'].iloc[-1]

        for growth_rate in self.params['revenue_growth_e'].data:
            revenue = revenue0 * (1 + growth_rate)
            iter_rev_e.append(revenue)
            revenue0 = revenue

        return iter_rev_e

    def project_cogs(self) -> list:
        iter_cogs_e: list = np.multiply(np.array(self.revenues_e[-1]),
                                            self.params['cogs_revenue_e'].data).tolist()
        return iter_cogs_e

    def project_sga(self) -> list:
        iter_sga_e: list = np.multiply(np.array(self.revenues_e[-1]),
                                           self.params['sga_revenue_e'].data).tolist()
        return iter_sga_e

    def project_r_and_d(self) -> list:
        iter_r_and_d_e: list = np.multiply(np.array(self.revenues_e[-1]),
                                               self.params['r_and_d_revenue_e'].data).tolist()
        return iter_r_and_d_e

    def project_fixed_assets(self) -> tuple[list, list, list]:
        iter_da_e: list = []
        iter_capex_e: list = []
        iter_nppe_e: list = []
        nppe0: float = self.enterprise.balance_sheet.loc['Net Property Plant & Equipment'].iloc[-1]

        for i, da_ratio in enumerate(self.params['da_nppe_e'].data):
            da: float = da_ratio * nppe0
            iter_da_e.append(da)

            net_capex: float = np.multiply(self.params['net_capex_revenue_e'].data[i],
                                           np.array(self.revenues_e[-1][i]))
            capex: float = net_capex + da
            iter_capex_e.append(capex)

            nppe: float = nppe0 - da + capex
            iter_nppe_e.append(nppe)

            nppe0 = nppe

        return iter_da_e, iter_capex_e, iter_nppe_e

    def project_change_net_working_capital(self) -> list:
        iter_change_nwc_e: list = []
        cce0: float = self.enterprise.balance_sheet.loc['Total Cash & ST Investments'].iloc[-1]
        ca0: float = self.enterprise.balance_sheet.loc['Total Current Assets'].iloc[-1]
        cld0: float = self.enterprise.balance_sheet.loc['Current Portion of Long Term Debt'].iloc[-1]
        cl0: float = self.enterprise.balance_sheet.loc['Total Current Liabilities'].iloc[-1]
        nwc0: float = (ca0 - cce0) - (cl0 - cld0)

        for i, nwc_ratio in enumerate(self.params['nwc_revenue_e'].data):
            nwc: float = nwc_ratio * self.revenues_e[-1][i]
            change_nwc: float = nwc - nwc0
            iter_change_nwc_e.append(change_nwc)
            nwc0 = nwc

        return iter_change_nwc_e

    def project_gross_profit(self) -> list:
        iter_gross_profit_e: list = (np.array(self.revenues_e[-1])
                                     - np.array(self.cogs_e[-1])).tolist()
        return iter_gross_profit_e

    def project_ebitda(self) -> list:
        iter_ebitda_e: list = (np.array(self.gross_profit_e[-1])
                               - np.array(self.sga_e[-1])
                               - np.array(self.r_and_d_e[-1])).tolist()
        return iter_ebitda_e

    def project_ebit(self) -> list:
        iter_ebit_e: list = (np.array(self.ebitda_e[-1])
                             + np.array(self.da_e[-1])).tolist()
        return iter_ebit_e

    def project_tax(self):
        iter_tax_e: list = (np.array(self.ebit_e[-1]) * self.enterprise.stat_tax).tolist()
        return iter_tax_e

    def project_fcf(self) -> list:
        iter_fcf_e: list = (np.array(self.ebit_e[-1])
                            -np.array(self.tax_e[-1])
                            +np.array(self.da_e)
                            -np.array(self.capex_e)
                            -np.array(self.change_nwc_e)).tolist()
        return iter_fcf_e
