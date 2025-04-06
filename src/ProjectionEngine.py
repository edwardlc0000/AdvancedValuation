
import numpy as np
import pandas as pd

from .Enterprise import Enterprise
from .ProjectionUtils import (
    calc_revenue_growth,
    calc_r_and_d_revenue,
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
        r_and_d_revenue: np.ndarray = calc_r_and_d_revenue(self.enterprise.income_statement.loc['Revenue'],
                                                           self.enterprise.income_statement.loc['R&D Exp.'])
        data_matrix: np.ndarray = np.vstack([revenue_growth,
                                             r_and_d_revenue])
        self.correlation_matrix = np.corrcoef(data_matrix)