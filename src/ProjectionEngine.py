

def calc_ucoe(rf: float, rm: float, beta_u: float) -> float:
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

def calc_reinvestment_rate(cap_ex: float,
                           d_and_a: float,
                           r_and_d: float,
                           change_nwc: float,
                           ebit: float,
                           tax_rate: float):
    return ((cap_ex - d_and_a + r_and_d + change_nwc)
            / ((ebit + r_and_d) * (1 - tax_rate)))

def calc_growth(roic: float, reinvestment_rate: float) -> float:
    """
    Calculate long-term growth rate.

    Parameters:
        roic (float): The return on invested capital.
        reinvestment_rate (float): The reinvestment rate.

    Returns:
        The long-term growth rate.
    """
    return roic * reinvestment_rate