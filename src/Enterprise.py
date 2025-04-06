"""
A class modeling the financial statements of an enterprise
"""

import pandas as pd
import numpy as np

class Enterprise:

    def __init__(self,
                 name: str, ticker: str, fdso: int,
                 debt_value: np.float64,
                 income_statement: pd.DataFrame = pd.DataFrame(),
                 cash_flow_statement: pd.DataFrame = pd.DataFrame(),
                 balance_sheet: pd.DataFrame = pd.DataFrame()):
        self.name: str = name
        self.ticker: str = ticker
        self.fdso: int = fdso
        self.enterprise_value: np.float64
        self.debt_value: np.float64 = debt_value
        self.equity_value: np.float64
        self.income_statement: pd.DataFrame = income_statement
        self.cash_flow_statement: pd.DataFrame = cash_flow_statement
        self.balance_sheet: pd.DataFrame = balance_sheet





