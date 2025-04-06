
import numpy as np
from numpy import ndarray, dtype, floating

from .Enterprise import Enterprise
from .ProjectionUtils import (
    calc_revenue_growth,
    calc_cogs_revenue,
    calc_r_and_d_revenue,
    calc_sga_revenue,
    calc_da_prior_nppe,
    calc_ucoe,
    calc_reinvestment_rate,
    calc_growth
)

class ProjectionEngine:

    def __init__(self, enterprise: Enterprise):
        self.correlation_matrix : np.ndarray
        self.enterprise: Enterprise = enterprise

    def calc_correlation(self) -> None:
        if (self.enterprise.income_statement.empty or
            self.enterprise.balance_sheet.empty or
            self.enterprise.cash_flow_statement.empty):
            raise ValueError("Cannot calculate correlation with empty data")

        revenue_growth: np.ndarray = calc_revenue_growth(self.enterprise.income_statement.loc['Revenue'])
        cogs_revenue: np.ndarray = calc_cogs_revenue(self.enterprise.income_statement.loc['Revenue'],
                                                     self.enterprise.income_statement.loc['Cost of Goods Sold'])
        r_and_d_revenue: np.ndarray = calc_r_and_d_revenue(self.enterprise.income_statement.loc['Revenue'],
                                                           self.enterprise.income_statement.loc['R&D Exp.'])
        sga_revenue: np.ndarray = calc_sga_revenue(self.enterprise.income_statement.loc['Revenue'],
                                                   self.enterprise.income_statement.loc['Selling General & Admin Exp.'])
        da_nppe: np.ndarray = calc_da_prior_nppe(self.enterprise.cash_flow_statement.loc['Depreciation & Amort.'],
                                                 self.enterprise.balance_sheet.loc['Net Property Plant & Equipment'])
        data_matrix: np.ndarray = np.vstack([revenue_growth,
                                             cogs_revenue,
                                             sga_revenue,
                                             r_and_d_revenue,
                                             da_nppe])
        self.correlation_matrix = np.corrcoef(data_matrix)