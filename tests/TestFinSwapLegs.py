###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import sys
sys.path.append("..")

from financepy.utils.math import ONE_MILLION
from financepy.utils.global_types import FinSwapTypes
from financepy.utils.calendar import BusDayAdjustTypes
from financepy.utils.calendar import DateGenRuleTypes
from financepy.utils.day_count import DayCountTypes
from financepy.utils.amount import FinAmount
from financepy.utils.frequency import FrequencyTypes
from financepy.utils.calendar import CalendarTypes
from financepy.utils.date import Date
from financepy.products.rates.FinFixedLeg import FinFixedLeg
from financepy.products.rates.FinFloatLeg import FinFloatLeg
from financepy.market.discount.curve_flat import DiscountCurveFlat

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinFixedIborSwapLeg():

    effectiveDate = FinDate(28, 10, 2020)
    maturityDate = FinDate(28, 10, 2025)
    
    coupon = -0.44970/100.0
    freqType = FinFrequencyTypes.ANNUAL    
    dayCountType = FinDayCountTypes.THIRTY_360_BOND
    notional = 10.0 * ONE_MILLION
    legPayRecType = FinSwapTypes.PAY
    calendarType = FinCalendarTypes.TARGET
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    paymentLag = 0
    principal = 0.0

    swapFixedLeg = FinFixedLeg(effectiveDate,
                               maturityDate,
                               legPayRecType,
                               coupon,
                               freqType,
                               dayCountType,
                               notional,
                               principal,
                               paymentLag,
                               calendarType,
                               busDayAdjustType,
                               dateGenRuleType)

###############################################################################

def test_FinFixedOISSwapLeg():

    effectiveDate = FinDate(28, 10, 2020)
    maturityDate = FinDate(28, 10, 2025)
    
    coupon = -0.515039/100.0
    freqType = FinFrequencyTypes.ANNUAL    
    dayCountType = FinDayCountTypes.ACT_360
    notional = 10.0 * ONE_MILLION
    legPayRecType = FinSwapTypes.PAY
    calendarType = FinCalendarTypes.TARGET
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    paymentLag = 1
    principal = 0.0

    swapFixedLeg = FinFixedLeg(effectiveDate,
                                  maturityDate,
                                  legPayRecType,
                                  coupon,
                                  freqType,
                                  dayCountType,
                                  notional,
                                  principal,
                                  paymentLag,
                                  calendarType,
                                  busDayAdjustType,
                                  dateGenRuleType)

###############################################################################

def test_FinFloatIborLeg():

    effectiveDate = FinDate(28, 10, 2020)
    maturityDate = FinDate(28, 10, 2025)
    
    spread = 0.0
    freqType = FinFrequencyTypes.ANNUAL    
    dayCountType = FinDayCountTypes.THIRTY_360_BOND
    notional = 10.0 * ONE_MILLION
    legPayRecType = FinSwapTypes.PAY
    calendarType = FinCalendarTypes.TARGET
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    paymentLag = 0
    principal = 0.0

    swapFloatLeg = FinFloatLeg(effectiveDate,
                               maturityDate,
                               legPayRecType,
                               spread,
                               freqType,
                               dayCountType,
                               notional,
                               principal,
                               paymentLag,
                               calendarType,
                               busDayAdjustType,
                               dateGenRuleType)

    liborCurve = FinDiscountCurveFlat(effectiveDate, 0.05)

    firstFixing = 0.03

    v = swapFloatLeg.value(effectiveDate, liborCurve, liborCurve, 
                           firstFixing)


###############################################################################

def test_FinFloatOISLeg():

    effectiveDate = FinDate(28, 10, 2020)
    maturityDate = FinDate(28, 10, 2025)
    
    spread = 0.0
    freqType = FinFrequencyTypes.ANNUAL    
    dayCountType = FinDayCountTypes.ACT_360
    notional = 10.0 * ONE_MILLION
    legPayRecType = FinSwapTypes.PAY
    calendarType = FinCalendarTypes.TARGET
    busDayAdjustType = FinBusDayAdjustTypes.FOLLOWING
    dateGenRuleType = FinDateGenRuleTypes.BACKWARD
    paymentLag = 1
    principal = 0.0

    swapFloatLeg = FinFloatLeg(effectiveDate,
                                  maturityDate,
                                  legPayRecType,
                                  spread,
                                  freqType,
                                  dayCountType,
                                  notional,
                                  principal,
                                  paymentLag,
                                  calendarType,
                                  busDayAdjustType,
                                  dateGenRuleType)

    liborCurve = FinDiscountCurveFlat(effectiveDate, 0.05)

    firstFixing = 0.03

    v = swapFloatLeg.value(effectiveDate, liborCurve, liborCurve, 
                           firstFixing)

###############################################################################

# Ibor Swap
test_FinFixedIborSwapLeg()
test_FinFloatIborLeg()

# OIS Swap
test_FinFixedOISSwapLeg()
test_FinFloatOISLeg()

testCases.compareTestCases()
