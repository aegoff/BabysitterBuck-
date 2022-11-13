import pytest
from ..logic import WorkHours,WorkCompensation



#####GENERAL TESTS######

def test_allfuturedates(): #due to client-side validation, this should not be possible
    '''
    GIVEN: A start date in the future
    WHEN: When calculating pay
    THEN: Return ValueError
    '''
    with pytest.raises(ValueError):
        WorkHours("2022-11-24T18:00","2022-11-24T20:00","2022-11-25T22:15").returnTimeDiff("2022-11-24T18:00","2022-11-24T20:00","2022-11-25T22:15")


####START TO BEDTIME#######

def test_morethan1daydiff_start2bed():
    '''
    GIVEN: A multi-day difference between start and bed
    WHEN: When calculating pay
    THEN: Return ValueError
    '''
    with pytest.raises(ValueError):
        WorkHours("2020-12-24T18:00","2020-12-27T0:00","2020-12-25T01:15").returnTimeDiff("2020-12-24T18:00","2020-12-27T0:00","2020-12-25T01:15")

def test_starttime_before5():
    '''
    GIVEN: A start time that is NOT between the hours of 17 to 23
    WHEN: When calculating pay
    THEN: Return ValueError
    '''
    with pytest.raises(ValueError):
        WorkHours("2020-12-24T14:00","2020-12-25T0:00","2020-12-25T06:15").returnTimeDiff("2020-12-24T14:00","2020-12-25T0:00","2020-12-25T06:15")

def test_pay_start2bed():
    '''
    GIVEN: Valid start datetime and valid bed datetime (Client-side validation)
    WHEN: When calculating pay
    THEN: Valid integer value of pay is returned
    '''
    myhours=WorkHours("2020-12-24T18:05","2020-12-24T20:05","2020-12-24T20:05").returnTimeDiff("2020-12-24T18:05","2020-12-24T20:05","2020-12-24T20:05")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_start2bed(myhours) == 24


def test_zerotime_start2bed():
    '''
    GIVEN: No difference in times
    WHEN: When calculating pay
    THEN: return 0
    '''
    myhours=WorkHours("2020-12-24T18:05","2020-12-24T18:05","2020-12-24T20:05").returnTimeDiff("2020-12-24T18:05","2020-12-24T18:05","2020-12-24T20:05")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_start2bed(myhours) == 0


def test_negativetime_start2bed():
    '''
    GIVEN: Bedtime is before starttime
    WHEN: When calculating pay
    THEN: return ValueError
    '''
    with pytest.raises(ValueError):
        WorkHours("2020-12-24T18:05","2020-12-24T16:05","2020-12-24T20:05").returnTimeDiff("2020-12-24T18:05","2020-12-24T16:05","2020-12-24T20:05")


def test_partialoverhalf_start2bed():
    '''
    GIVEN: Work is more than or equal to 30min but less than 1 hr
    WHEN: When calculating pay
    THEN: return value rounded to next integer
    '''
    myhours=WorkHours("2020-12-24T18:05","2020-12-24T18:35","2020-12-24T18:45").returnTimeDiff("2020-12-24T18:05","2020-12-24T18:35","2020-12-24T18:45")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_start2bed(myhours) == 12 #30min rounded up to one hour's worth of compensation of $12


def test_partialunderhalf_start2bed():
    '''
    GIVEN: Work is less than 30min
    WHEN: When calculating pay
    THEN: return value rounded to the previous integer
    '''
    myhours=WorkHours("2020-12-24 18:00","2020-12-24T18:15","2020-12-24T18:15").returnTimeDiff("2020-12-24T18:00","2020-12-24T18:15","2020-12-24T18:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_start2bed(myhours) == 0

#####BEDTIME TO MIDNIGHT#########

def test_negativetime_bed2mid():
    '''
    GIVEN: Bedtime is after midnight
    WHEN: calculating pay
    THEN: return 0 
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-25T01:15","2020-12-25T02:15").returnTimeDiff("2020-12-24T18:00","2020-12-25T01:15","2020-12-25T02:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_bed2mid(myhours) == 0 #child went to bed after midnight, no pay here

def test_pay_bed2mid():
    '''
    GIVEN: Valid start datetime and valid bed datetime (Client-side validation)
    WHEN: When calculating pay
    THEN: Valid integer value of pay is returned
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-24T22:00","2020-12-25T02:15").returnTimeDiff("2020-12-24T18:00","2020-12-24T22:00","2020-12-25T02:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_bed2mid(myhours) == 16 #2hrs of $8 compensation

def test_zerotime_bed2mid():
    '''
    GIVEN: No difference in times
    WHEN: When calculating pay
    THEN: return 0
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-25 0:00","2020-12-25T02:15").returnTimeDiff("2020-12-24T18:00","2020-12-25T0:00","2020-12-25T02:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_bed2mid(myhours) == 0 #2hrs of $8 compensation

def test_partialoverhalf_bed2mid():
    '''
    GIVEN: Work is more than or equal to 30min but less than 1 hr
    WHEN: When calculating pay
    THEN: return value rounded to next integer
    '''
    myhours=WorkHours("2020-12-24 18:05","2020-12-24T23:30","2020-12-25T03:35").returnTimeDiff("2020-12-24T18:05","2020-12-24T23:30","2020-12-25T03:35")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_bed2mid(myhours) == 8 #rounded up to one hour's worth of compensation due to 30min to midnight


def test_partialunderhalf_bed2mid():
    '''
    GIVEN: Work is less than 30min
    WHEN: When calculating pay
    THEN: return value rounded to the previous integer
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-24T23:45","2020-12-25T01:15").returnTimeDiff("2020-12-24T18:00","2020-12-24T23:45","2020-12-25T01:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_bed2mid(myhours) == 0 #only 15 min between bedtime and midnight, no pay


######MIDNIGHT TO END#######

def test_morethan1daydiff_start2end():
    '''
    GIVEN: A multi-day difference between start and end
    WHEN: When calculating pay
    THEN: Return ValueError
    '''
    with pytest.raises(ValueError):
        WorkHours("2020-12-24T18:00","2020-12-25T0:00","2020-12-28T06:15").returnTimeDiff("2020-12-24T18:00","2020-12-25T0:00","2020-12-28T06:15")


def test_late_end_time():

    '''
    GIVEN: Parents arrive home later than 4am the next day
    WHEN: When calculating pay
    THEN: Raise ValueError
    '''
    with pytest.raises(ValueError):
        WorkHours("2020-12-24T18:00","2020-12-25T0:00","2020-12-25T06:15").returnTimeDiff("2020-12-24T18:00","2020-12-25T0:00","2020-12-25T06:15")

def test_partialoverhalf_mid2end():
    '''
    GIVEN: Work is more than or equal to 30min but less than 1 hr
    WHEN: When calculating pay
    THEN: return value rounded to next integer
    '''
    myhours=WorkHours("2020-12-24T18:05","2020-12-24T18:15","2020-12-25T00:30").returnTimeDiff("2020-12-24T18:05","2020-12-24T18:15","2020-12-25T00:30")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_mid2end(myhours) == 16 #rounded up to one hour's worth of compensation because 30 min post midnight


def test_partialunderhalf_mid2end():
    '''
    GIVEN: Work is less than 30min
    WHEN: When calculating pay
    THEN: return value rounded to the previous integer
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-24T18:15","2020-12-24T18:15").returnTimeDiff("2020-12-24T18:00","2020-12-24T18:15","2020-12-24T18:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_mid2end(myhours) == 0

def test_zerotime_mid2end():
    '''
    GIVEN: No difference in times
    WHEN: When calculating pay
    THEN: return 0
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-25T0:00","2020-12-25T00:00").returnTimeDiff("2020-12-24T18:00","2020-12-25T0:00","2020-12-25T00:00")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_mid2end(myhours) == 0 #2hrs of $8 compensation


def test_negativetime_mid2end():
    '''
    GIVEN: End time is before midnight
    WHEN: calculating pay
    THEN: return 0 
    '''
    myhours=WorkHours("2020-12-24T18:00","2020-12-24T20:15","2020-12-24T22:15").returnTimeDiff("2020-12-24T18:00","2020-12-24T20:15","2020-12-24T22:15")
    workpay=WorkCompensation(myhours)
    assert workpay.pay_mid2end(myhours) == 0 #parents arrived before midnight, no pay here


def test_negativetime_start2end():
    '''
    GIVEN: End time is before start time (impossible)
    WHEN: calculating pay
    THEN: return 0 
    '''
    with pytest.raises(ValueError):
        WorkHours("2020-12-24T14:00","2020-12-25T0:00","2020-12-23T06:15").returnTimeDiff("2020-12-24T14:00","2020-12-25T0:00","2020-12-23T06:15")



