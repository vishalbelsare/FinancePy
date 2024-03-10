##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

import numpy as np


from ...utils.math import n_vect  # n_prime_vect

from ...utils.global_vars import gDaysInYear
from ...utils.error import FinError
# from ...products.equity.EquityOption import FinOption
from ...utils.date import Date
# from ...products.fx.FinFXModelTypes import FinFXModel
from ...models.black_scholes import BlackScholes
from ...utils.helpers import check_argument_types
from ...utils.global_types import OptionTypes

###############################################################################


class FXDigitalOption:

    def __init__(self,
                 expiry_dt: Date,
                 strike_fx_rate: (float, np.ndarray),
                 currency_pair: str,  # FORDOM
                 option_type: (OptionTypes, list),
                 notional: float,
                 prem_currency: str,
                 spot_days: int = 0):
        """ Create the FX Digital Option object. Inputs include expiry date,
        strike, currency pair, option type (call or put), notional and the
        currency of the notional. And adjustment for spot days is enabled. All
        currency rates must be entered in the price in domestic currency of
        one unit of foreign. And the currency pair should be in the form FORDOM
        where FOR is the foreign currency pair currency code and DOM is the
        same for the domestic currency. """

        check_argument_types(self.__init__, locals())

        delivery_dt = expiry_dt.add_weekdays(spot_days)

        if delivery_dt < expiry_dt:
            raise FinError("Delivery date must be on or after expiry date.")

        if len(currency_pair) != 6:
            raise FinError("Currency pair must be 6 characters.")

        self._expiry_dt = expiry_dt
        self._delivery_dt = delivery_dt

        if np.any(strike_fx_rate < 0.0):
            raise FinError("Negative strike.")

        self._strike_fx_rate = strike_fx_rate

        self._currency_pair = currency_pair
        self._for_name = self._currency_pair[0:3]
        self._dom_name = self._currency_pair[3:6]

        if prem_currency != self._dom_name and prem_currency != self._for_name:
            raise FinError("Notional currency not in currency pair.")

        self._prem_currency = prem_currency

        self._notional = notional

        if option_type != OptionTypes.DIGITAL_CALL and\
           option_type != OptionTypes.DIGITAL_PUT:
            raise FinError("Unknown Digital Option Type:" + option_type)

        self._option_type = option_type
        self._spot_days = spot_days

###############################################################################

    def value(self,
              value_dt,
              spot_fx_rate,  # 1 unit of foreign in domestic
              domestic_curve,
              foreign_curve,
              model):
        """ Valuation of a digital option using Black-Scholes model. This
        allows for 4 cases - first upper barriers that when crossed pay out
        cash (calls) and lower barriers than when crossed from above cause a
        cash payout (puts) PLUS the fact that the cash payment can be in
        domestic or foreign currency. """

        if isinstance(value_dt, Date) is False:
            raise FinError("Valuation date is not a Date")

        if value_dt > self._expiry_dt:
            raise FinError("Valuation date after expiry date.")

        if domestic_curve.value_dt != value_dt:
            raise FinError(
                "Domestic Curve valuation date not same as valuation date")

        if foreign_curve.value_dt != value_dt:
            raise FinError(
                "Foreign Curve valuation date not same as valuation date")

        if isinstance(value_dt, Date):
            spot_dt = value_dt.add_weekdays(self._spot_days)
            tdel = (self._delivery_dt - spot_dt) / gDaysInYear
            t_exp = (self._expiry_dt - value_dt) / gDaysInYear
        else:
            tdel = value_dt
            t_exp = tdel

        if np.any(spot_fx_rate <= 0.0):
            raise FinError("spot_fx_rate must be greater than zero.")

        if np.any(tdel < 0.0):
            raise FinError("Option time to maturity is less than zero.")

        tdel = np.maximum(tdel, 1e-10)

        # TODO RESOLVE TDEL versus TEXP
        dom_df = domestic_curve._df(tdel)
        for_df = foreign_curve._df(tdel)

        r_d = -np.log(dom_df) / tdel
        rf = -np.log(for_df) / tdel

        s0 = spot_fx_rate
        K = self._strike_fx_rate

        if isinstance(model, BlackScholes):

            volatility = model._volatility
            ln_s0_k = np.log(s0 / K)
            den = volatility * np.sqrt(t_exp)
            v2 = volatility * volatility
            mu = r_d - rf
            d2 = (ln_s0_k + (mu - v2 / 2.0) * tdel) / den

            if self._option_type == OptionTypes.DIGITAL_CALL and \
                    self._for_name == self._prem_currency:
                v = s0 * np.exp(-rf * tdel) * n_vect(d2)
            elif self._option_type == OptionTypes.DIGITAL_PUT and \
                    self._for_name == self._prem_currency:
                v = s0 * np.exp(-rf * tdel) * n_vect(-d2)
            elif self._option_type == OptionTypes.DIGITAL_CALL and \
                    self._dom_name == self._prem_currency:
                v = np.exp(-r_d * tdel) * n_vect(d2)
            elif self._option_type == OptionTypes.DIGITAL_PUT and \
                    self._dom_name == self._prem_currency:
                v = np.exp(-r_d * tdel) * n_vect(-d2)
            else:
                raise FinError("Unknown option type")

            v = v * self._notional

        return v

###############################################################################
