from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import math
from dataclasses import dataclass


class Hours(ABC):
    @abstractmethod
    def appropriate_hours(self):
        pass

@dataclass(init=True)
class WorkHours(Hours):
    begin: str
    bed: str
    end: str
    
    def structure_datetime(self,begin,bed,end)-> str:
        datetime_start=datetime.strptime(begin, '%Y-%m-%dT%H:%M')
        datetime_bed=datetime.strptime(bed, '%Y-%m-%dT%H:%M')
        datetime_mid=datetime.combine((datetime_start + timedelta(days=1)),datetime.strptime('0000','%H%M').time())
        datetime_end=datetime.strptime(end, '%Y-%m-%dT%H:%M')
        return datetime_start,datetime_bed,datetime_mid,datetime_end

    def appropriate_hours(self,begin,bed,end)->bool:
        datetime_start,datetime_bed,datetime_mid,datetime_end=self.structure_datetime(begin,bed,end)
        if datetime_start.hour<17:
            raise ValueError("Start Time must be after 5pm.")
        if abs(datetime_start.day-datetime_bed.day)>1:
            raise ValueError("Times differences between start time and bedtime may not be greater than one night.")
        if abs(datetime_start.day-datetime_end.day)>1:
            raise ValueError("Times differences between start time and end time may not be greater than one night.")
        if datetime_start > datetime_end:
            raise ValueError("Start time must always be before end time.")
        if datetime_start > datetime_bed:
            raise ValueError("Start time must always be before bedtime.")
        if datetime_bed > datetime_end:
            raise ValueError("Bedtime must always be before end time.")
        if abs(datetime_bed.day-datetime_end.day)>1:
            raise ValueError("Times differences between midnight and end time may not be greater than one night.")
        if datetime_mid.day==datetime_end.day:
            if datetime_end.hour>4:
                raise ValueError("Valid work time cannot go later than 4am the next day.")
        return True

    def returnTimeDiff(self,begin,bed,end)->list[float]:
        datetime_start,datetime_bed,datetime_mid,datetime_end=self.structure_datetime(begin,bed,end)
        if self.appropriate_hours(begin,bed,end)==True:
            time_diff=[]
            begin2bed=((datetime_bed-datetime_start).total_seconds()/ 3600)  # duration in hours
            time_diff.append(begin2bed)
            bed2mid=((datetime_mid-datetime_bed).total_seconds()/ 3600)
            time_diff.append(bed2mid) 
            mid2end=((datetime_end-datetime_mid).total_seconds()/ 3600) 
            time_diff.append(mid2end)
            return time_diff

    def __str__(self,begin,bed,end)->str:
        time_diff=returnTimeDiff(begin,bed,end)
        return f'Babysitter arrived at {begin}, kid(s) went to bed at {bed}, and babysitter left at {end}. Time differencees between intervals are: {time_diff[0]},{time_diff[1]}, and {time_diff[2]}, respectively.'

    def __del__(self)->str:
        print("Work Hours have been deleted.")


class Compensation(ABC):
    @abstractmethod
    def pay_start2bed(self):
        pass
    @abstractmethod
    def pay_bed2mid(self):
        pass
    @abstractmethod
    def pay_mid2end(self):
        pass
    @abstractmethod
    def total_pay(self):
        pass

@dataclass(init=True)
class WorkCompensation(Compensation):
    time_diff: list[float]
    
    def pay_start2bed(self,time_diff)->int:
        if time_diff[0]<=0:
            return 0
        if time_diff[0] - math.floor(time_diff[0]) < 0.5:
            pay=math.floor(time_diff[0])*12
            return pay
        pay=math.ceil(time_diff[0])*12
        return pay
    def pay_bed2mid(self,time_diff)->int:
        if time_diff[1]<=0:
            return 0
        if time_diff[1] - math.floor(time_diff[1]) < 0.5:
            pay=math.floor(time_diff[1])*8
            return pay
        pay=math.ceil(time_diff[1])*8
        return pay
    def pay_mid2end(self,time_diff)->int:
        if time_diff[2]<=0:
            return 0
        if time_diff[2] - math.floor(time_diff[2]) < 0.5:
            pay=math.floor(time_diff[2])*16
            return pay
        pay=math.ceil(time_diff[2])*16
        return pay
    def total_pay(self,time_diff)->int:
        total_pay=self.pay_start2bed(time_diff)+self.pay_bed2mid(time_diff)+self.pay_mid2end(time_diff)
        return total_pay
    def __str__(self,time_diff):
        start2bed=pay_start2bed(time_diff)
        bed2mid=pay_bed2mid(time_diff)
        mid2end=pay_mid2end(time_diff)
        total=total_pay(time_diff)
        return f'Babysitter will get paid for each phase: ${start2bed}, ${bed2mid}, and ${mid2end}. In total: ${total}.'

    def __del__(self):
        print("Work compensation data has been deleted.")




