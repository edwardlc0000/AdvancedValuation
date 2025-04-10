import numpy as np
import pandas as pd

def calc_revenue_growth(revenue:pd.Series) -> np.ndarray:
    """
    Calculate revenue growth.

    Parameters:
        revenue (pd.Series): The revenue data.
    Returns:
        revenue_growth (np.ndarray): The revenue growth.
    """
    revenue: np.ndarray = revenue.to_numpy()

    if 0 in revenue:
        raise ZeroDivisionError("Invalid revenue data. Revenue should not be zero.")

    revenue_change: np.ndarray = np.diff(revenue)
    revenue_growth: np.ndarray = revenue_change / revenue[:-1]
    return revenue_growth

def calc_cogs_revenue(revenue: pd.Series,
                      cogs: pd.Series) -> np.ndarray:
    """

    """
    revenue: np.ndarray = revenue.to_numpy()
    cogs: np.ndarray = cogs.to_numpy()

    if 0 in revenue:
        raise ZeroDivisionError("Invalid revenue data. Revenue should not be zero.")

    if len(revenue) != len(cogs):
        raise IndexError("The length of revenue and COGS data should be the same.")

    cogs_revenue: np.ndarray = cogs[1:] / revenue[1:]
    return cogs_revenue

def calc_r_and_d_revenue(revenue: pd.Series,
                         r_and_d: pd.Series) -> np.ndarray:
    """
    Calculate the ratio of revenue to R&D.

    Parameters:
        revenue (pd.Series): The revenue data.
        r_and_d (pd.Series): The R&D data.
    Returns:
        r_and_d_revenue (np.ndarray): The ratio of revenue to R&D.
    """
    revenue: np.ndarray = revenue.to_numpy()
    r_and_d: np.ndarray = r_and_d.to_numpy()

    if 0 in revenue:
        raise ZeroDivisionError("Invalid revenue data. Revenue should not be zero.")

    if len(revenue) != len(r_and_d):
        raise IndexError("The length of revenue and R&D data should be the same.")

    r_and_d_revenue: np.ndarray = r_and_d[1:] / revenue[1:]
    return r_and_d_revenue

def calc_sga_revenue(revenue: pd.Series,
                     sga: pd.Series) -> np.ndarray:
    """
    Calculate the ratio of revenue to SG&A.

    Parameters:
        revenue (pd.Series): The revenue data.
        sga (pd.Series): The SG&A data.
    Returns:
        sga_revenue (np.ndarray): The ratio of revenue to SG&A.
    """
    revenue: np.ndarray = revenue.to_numpy()
    sga: np.ndarray = sga.to_numpy()

    if 0 in revenue:
        raise ZeroDivisionError("Invalid revenue data. Revenue should not be zero.")

    if len(revenue) != len(sga):
        raise IndexError("The length of revenue and SGA data should be the same.")

    sga_revenue: np.ndarray = sga[1:] / revenue[1:]
    return sga_revenue

def calc_da_prior_nppe(da: pd.Series,
                       nppe: pd.Series) -> np.ndarray:
    """
    Calculate the ratio of depreciation and amortization to prior Net-PP&E.

    Parameters:
        da (pd.Series): The depreciation and amortization data.
        nppe (pd.Series): The Net-PP&E data.
    Returns:
        da_nppe (np.ndarray): The ratio of depreciation and amortization to prior Net-PP&E.
    """
    da: np.ndarray = da.to_numpy()
    nppe: np.ndarray = nppe.to_numpy()

    if 0 in nppe:
        raise ZeroDivisionError("Invalid Net-PP&E data. Net-PP&E should not be zero.")

    if len(da) != len(nppe):
        raise IndexError("The length of depreciation & amortization and Net-PP&E data should be the same.")

    da_nppe: np.ndarray = da[1:] / nppe[:-1]
    return da_nppe

def calc_nwc_revenue(revenue: pd.Series,
                     cce: pd.Series,
                     ca: pd.Series, cld: pd.Series,
                     cl: pd.Series) -> np.ndarray:
    """

    """
    revenue: np.ndarray = revenue.to_numpy()
    cce: np.ndarray = cce.to_numpy()
    ca: np.ndarray = ca.to_numpy()
    cl: np.ndarray = cl.to_numpy()
    cld: np.ndarray = cld.to_numpy()

    if 0 in revenue:
        raise ZeroDivisionError("Invalid revenue data. Revenue should not be zero.")

    if len(revenue) != len(cce) or len(revenue) != len(ca) or len(revenue) != len(cl) or len(revenue) != len(cld):
        raise IndexError("The length of revenue, CCE, CA, and CL data should be the same.")

    nwc: np.ndarray = (ca - cce) - (cl - cld)
    nwc_revenue: np.ndarray = nwc[1:] / revenue[1:]
    return nwc_revenue

def calc_net_capex_revenue(revenue: pd.Series,
                           capex: pd.Series,
                           da: pd.Series) -> np.ndarray:
    """

    """
    revenue: np.ndarray = revenue.to_numpy()
    capex: np.ndarray = capex.to_numpy()
    da: np.ndarray = da.to_numpy()

    if 0 in revenue:
        raise ZeroDivisionError("Invalid revenue data. Revenue should not be zero.")

    if len(revenue) != len(capex) or len(revenue) != len(da):
        raise IndexError("The length of revenue, CAPEX, and depreciation and amortization data should be the same.")

    capex = np.multiply(capex, -1.0)
    net_capex: np.ndarray = capex - da
    net_capex_revenue: np.ndarray = net_capex[1:] / revenue[1:]
    return net_capex_revenue

def calc_ucoe(rf: float,
              rm: float,
              beta_u: float) -> float:
    """
    Calculate unlevered cost of equity.

    Parameters:
        rf (float): The expected risk-free return.
        rm (float): The expected market return.
        beta_u (float): The unlevered beta.
    Returns:
        float: The unlevered cost of equity.
    """
    return rf + beta_u * (rm - rf)

def calc_coe(ucoe: float, cod: float, lev: float) -> float:
    """

    """
    return ucoe + ((lev / (1 - lev)) * (ucoe - cod))

def calc_wacc(coe: float, cod: float, lev: float, tax_rate: float):
    """

    """
    return (coe * (1.0 - lev)) + (cod * (1.0 - tax_rate) * lev)

def calc_reinvestment_rate(cap_ex: float,
                           d_and_a: float,
                           r_and_d: float,
                           change_nwc: float,
                           ebit: float,
                           tax_rate: float) -> float:
    """
    Calculate the reinvestment rate.

    Parameters:
        cap_ex (float): Capital expenditure.
        d_and_a (float): Depreciation and amortization.
        r_and_d (float): Research and development.
        change_nwc (float): Change in net-working capital.
        ebit (float): Earnings before interest and taxes.
        tax_rate (float): The tax rate.
    Returns:
        float: The reinvestment rate.
    """
    return ((cap_ex - d_and_a + r_and_d + change_nwc)
            / ((ebit + r_and_d) * (1 - tax_rate)))

def calc_growth(roic: float,
                reinvestment_rate: float) -> float:
    """
    Calculate long-term growth rate.

    Parameters:
        roic (float): The return on invested capital.
        reinvestment_rate (float): The reinvestment rate.
    Returns:
        The long-term growth rate.
    """
    return roic * reinvestment_rate