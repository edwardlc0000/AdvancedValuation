import numpy as np
import pandas as pd
import unittest

from src.ProjectionUtils import (
    calc_revenue_growth,
    calc_r_and_d_revenue,
    calc_ucoe,
    calc_reinvestment_rate,
    calc_growth
)

class TestCalcRevenueGrowth(unittest.TestCase):
    def test_typical_case(self):
        # Test with a typical revenue series
        revenue = pd.Series([100, 110, 125, 140, 160])
        result = calc_revenue_growth(revenue)

        # Expected growth rates: (110-100)/100, (125-110)/110, etc.
        expected = np.array([0.1, 0.136363636, 0.12, 0.142857143])

        # Check shape and values
        self.assertEqual(len(result), len(revenue) - 1)
        np.testing.assert_almost_equal(result, expected)

    def test_zero_revenue(self):
        # Test with zero in revenue (should raise ZeroDivisionError)
        revenue = pd.Series([0, 110, 125])
        with self.assertRaises(ZeroDivisionError):
            calc_revenue_growth(revenue)

    def test_negative_revenue(self):
        # Test with negative revenue
        revenue = pd.Series([100, -110, 125])
        result = calc_revenue_growth(revenue)
        # Growth should be negative when revenue goes negative
        self.assertTrue(result[0] < 0)

class TestCalcRandDRevenue(unittest.TestCase):
    def test_typical_case(self):
        # Test with typical revenue and R&D series
        revenue = pd.Series([100, 110, 125, 140, 160])
        r_and_d = pd.Series([10, 12, 15, 18, 22])

        result = calc_r_and_d_revenue(revenue, r_and_d)

        # Expected ratios: 12/110, 15/125, etc.
        # Note the implementation slices both arrays starting from index 1
        expected = np.array([12 / 110, 15 / 125, 18 / 140, 22 / 160])

        self.assertEqual(len(result), len(revenue) - 1)
        np.testing.assert_almost_equal(result, expected)

    def test_zero_revenue(self):
        # Test with zero in revenue (should raise ZeroDivisionError)
        revenue = pd.Series([100, 0, 125])
        r_and_d = pd.Series([10, 12, 15])
        with self.assertRaises(ZeroDivisionError):
            calc_r_and_d_revenue(revenue, r_and_d)

    def test_different_length(self):
        # Test with different length series
        revenue = pd.Series([100, 110, 125])
        r_and_d = pd.Series([10, 12])

        # This should raise an IndexError since the arrays have different lengths
        with self.assertRaises(IndexError):
            calc_r_and_d_revenue(revenue, r_and_d)


class TestCalcUcoe(unittest.TestCase):
    def test_typical_case(self):
        # Test with typical values
        rf = 0.02  # Risk-free rate: 2%
        rm = 0.08  # Market return: 8%
        beta_u = 1.2  # Unlevered beta

        result = calc_ucoe(rf, rm, beta_u)

        # Expected: rf + beta_u * (rm - rf) = 0.02 + 1.2 * (0.08 - 0.02) = 0.092
        expected = 0.092

        self.assertAlmostEqual(result, expected)

    def test_zero_beta(self):
        # Test with zero beta
        rf = 0.02
        rm = 0.08
        beta_u = 0.0

        result = calc_ucoe(rf, rm, beta_u)

        # With zero beta, result should equal risk-free rate
        expected = rf

        self.assertAlmostEqual(result, expected)

    def test_negative_beta(self):
        # Test with negative beta (unusual but possible)
        rf = 0.02
        rm = 0.08
        beta_u = -0.5

        result = calc_ucoe(rf, rm, beta_u)

        # With negative beta: 0.02 + (-0.5) * (0.08 - 0.02) = 0.02 - 0.03 = -0.01
        expected = -0.01

        self.assertAlmostEqual(result, expected)


class TestCalcReinvestmentRate(unittest.TestCase):
    def test_typical_case(self):
        # Test with typical values
        cap_ex = 100.0  # Capital expenditure
        d_and_a = 50.0  # Depreciation and amortization
        r_and_d = 30.0  # R&D
        change_nwc = 5.0  # Change in net working capital
        ebit = 200.0  # Earnings before interest and taxes
        tax_rate = 0.25  # Tax rate (25%)

        result = calc_reinvestment_rate(cap_ex, d_and_a, r_and_d, change_nwc, ebit, tax_rate)

        # Expected: (100 - 50 + 30 + 5) / ((200 + 30) * (1 - 0.25)) = 85 / (230 * 0.75) = 85 / 172.5 = 0.4927536232
        expected = 85 / 172.5

        self.assertAlmostEqual(result, expected)

    def test_zero_ebit(self):
        # Test with zero EBIT (should handle division by zero)
        cap_ex = 100.0
        d_and_a = 50.0
        r_and_d = 0.0
        change_nwc = 5.0
        ebit = 0.0
        tax_rate = 0.25

        with self.assertRaises(ZeroDivisionError):
            calc_reinvestment_rate(cap_ex, d_and_a, r_and_d, change_nwc, ebit, tax_rate)

    def test_full_tax_rate(self):
        # Test with 100% tax rate (should handle division by zero)
        cap_ex = 100.0
        d_and_a = 50.0
        r_and_d = 30.0
        change_nwc = 5.0
        ebit = 200.0
        tax_rate = 1.0

        with self.assertRaises(ZeroDivisionError):
            calc_reinvestment_rate(cap_ex, d_and_a, r_and_d, change_nwc, ebit, tax_rate)


class TestCalcGrowth(unittest.TestCase):
    def test_typical_case(self):
        # Test with typical values
        roic = 0.15  # Return on invested capital
        reinvestment_rate = 0.40  # Reinvestment rate

        result = calc_growth(roic, reinvestment_rate)

        # Expected: roic * reinvestment_rate = 0.15 * 0.40 = 0.06
        expected = 0.06

        self.assertAlmostEqual(result, expected)

    def test_zero_roic(self):
        # Test with zero ROIC
        roic = 0.0
        reinvestment_rate = 0.40

        result = calc_growth(roic, reinvestment_rate)

        # Expected: 0 * 0.40 = 0
        expected = 0.0

        self.assertAlmostEqual(result, expected)

    def test_zero_reinvestment(self):
        # Test with zero reinvestment rate
        roic = 0.15
        reinvestment_rate = 0.0

        result = calc_growth(roic, reinvestment_rate)

        # Expected: 0.15 * 0 = 0
        expected = 0.0

        self.assertAlmostEqual(result, expected)

    def test_negative_values(self):
        # Test with negative values
        roic = -0.05
        reinvestment_rate = 0.40

        result = calc_growth(roic, reinvestment_rate)

        # Expected: -0.05 * 0.40 = -0.02
        expected = -0.02

        self.assertAlmostEqual(result, expected)


if __name__ == '__main__':
    unittest.main()