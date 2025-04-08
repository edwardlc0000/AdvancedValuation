"""
A class modeling the financial statements of an enterprise
"""

import pandas as pd

class Enterprise:

    def __init__(self,
                 name: str, ticker: str, fdso: int,
                 debt_value: float, stat_tax: float,
                 income_statement: pd.DataFrame = pd.DataFrame(),
                 cash_flow_statement: pd.DataFrame = pd.DataFrame(),
                 balance_sheet: pd.DataFrame = pd.DataFrame()):
        self.name: str = name
        self.ticker: str = ticker
        self.fdso: int = fdso
        self.enterprise_value: float
        self.debt_value: float = debt_value
        self.stat_tax: float = stat_tax
        self.equity_value: float
        self.income_statement: pd.DataFrame = income_statement
        self.cash_flow_statement: pd.DataFrame = cash_flow_statement
        self.balance_sheet: pd.DataFrame = balance_sheet





