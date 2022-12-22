import numpy as np
from datetime import datetime, date, timedelta

#check whether the date format is valid
def CheckValidDate(YYYYMMDDhhmm):
    date = str(YYYYMMDDhhmm)
    if len(date) == 12:
        print('The date is vaild')
    else:
        print('The date is not vaild. Please follow by the format YYYYMMDDhhmm')

#seperate date input into YYYY, MM ,DD , hh , mm
def FindDate(YYYYMMDDhhmm):

    DATE = str(YYYYMMDDhhmm)
    YYYY = int(DATE[:4])
    MM = int(DATE[4:6])
    DD = int(DATE[6:8])
    hh = int(DATE[8:10])
    mm = int(DATE[10:12])

    amount = GetSubDateSplitAmount(YYYYMMDDhhmm)
    output = np.empty([1,amount])[0]

    return np.array([YYYY,MM,DD,hh,mm],dtype = np.int32)

def GetSubDateSplitAmount(YYYYMMDDhhmm):

    if len(str(YYYYMMDDhhmm)) == 4:
        return 1

    elif len(str(YYYYMMDDhhmm)) == 6:
        return 2

    elif len(str(YYYYMMDDhhmm)) == 8:
        return 3

    elif len(str(YYYYMMDDhhmm)) == 10:
        return 4

    elif len(str(YYYYMMDDhhmm)) == 12:
        return 5

    elif len(str(YYYYMMDDhhmm)) == 14:
        return 6

# A function to let numpy array to tuple which can be used in pandas indexing
def ToTuple(DateArray):

    output = [[] for i in range(len(DateArray))]
    for k in range(len(DateArray)):
        element = tuple(DateArray[k])
        output[k] = element
    
    return output

def GetSplitedArray(DateArray):

    #in i th element : [YYYY,MM,DD,hh,mm]
    Date_element_amount = GetSubDateSplitAmount(DateArray[0])
    output = np.empty([len(DateArray),Date_element_amount],dtype = int)
    for i in range(len(DateArray)):
        Date = FindDate(DateArray[i])
        for j in range(len(Date)):
            output[i,j] = Date[j]
    
    return output

#roll until target date
def RollDate(YYYYMMDDhhmm, no_day, no_hr, no_min):

    YYYY,MM,DD,hh,mm = FindDate(YYYYMMDDhhmm)
    base = datetime(year = YYYY, month = MM, day = DD, hour = hh, minute = mm )
    roll = timedelta(days = no_day, hours = no_hr, minutes = no_min)
    newtime = base + roll
    newtime = int(newtime.strftime('%Y%m%d%H%M'))
    return newtime

#find date amount
def FindDateAmount(start_YYYYMMDDhhmm,end_YYYYMMDDhhmm,int_hour,int_minite):

    start,end = GetStartAndEndObject(start_YYYYMMDDhhmm,end_YYYYMMDDhhmm)
    diff_seconds = FindDiffSeconds(start,end)
    interval_seconds = int_hour*60*60 + int_minite*60
    amount = diff_seconds//interval_seconds + 1

    return amount

def FindDiffSeconds(start_object, end_object):

    diff = end_object - start_object
    diff_seconds = int(diff.total_seconds())

    return diff_seconds

def GetStartAndEndObject(start_YYYYMMDDhhmm, end_YYYYMMDDhhmm):

    splited_start_YYYYMMDDhhmm = FindDate(start_YYYYMMDDhhmm)
    splited_end_YYYYMMDDhhmm = FindDate(end_YYYYMMDDhhmm)
    start = datetime(year = splited_start_YYYYMMDDhhmm[0], month = splited_start_YYYYMMDDhhmm[1],
                     day = splited_start_YYYYMMDDhhmm[2], hour = splited_start_YYYYMMDDhhmm[3], minute = splited_start_YYYYMMDDhhmm[4])
    end = datetime(year = splited_end_YYYYMMDDhhmm[0], month = splited_end_YYYYMMDDhhmm[1],
                     day = splited_end_YYYYMMDDhhmm[2], hour = splited_end_YYYYMMDDhhmm[3], minute = splited_end_YYYYMMDDhhmm[4])
    return start, end

#get full date array in certain interval
def GetDateArray(start_YYYYMMDDhhmm, end_YYYYMMDDhhmm, int_hour, int_minute):

    target_date = start_YYYYMMDDhhmm
    start,end = GetStartAndEndObject(start_YYYYMMDDhhmm,end_YYYYMMDDhhmm)
    amount = FindDateAmount(start_YYYYMMDDhhmm, end_YYYYMMDDhhmm, int_hour, int_minute)
    DATE_array = np.empty([1,amount],dtype = np.int64)[0]
    index = 0
    diff_seconds = FindDiffSeconds(start,end)

    #loop to find date at each element
    while diff_seconds >= 0.0:
        DATE_array[index] = target_date
        target_date = RollDate(target_date,0,int_hour, int_minute)
        target, end = GetStartAndEndObject(target_date,end_YYYYMMDDhhmm)
        diff_seconds = FindDiffSeconds(target,end)
        index += 1
    
    return DATE_array


if __name__ == '__main__':

    CheckValidDate(201701010100)
    print('CheckValidDate is workable')
    newtime = RollDate(201701010100,1,2,10)
    print('CheckValidDate is workable')
    YYYY,MM,DD,hh,mm = FindDate(201701010100)
    print('FindDate is workable')
    amount = FindDateAmount(201701010000,201701010000,0,4)
    print(amount)
    print('FindDateAmount is workable')
    DateArray = GetDateArray(201701010000,201701010011,0,4)
    print(DateArray)
    print('GetDateArray is workable')
    Splited_Date = GetSplitedArray(DateArray)
    print('GetSplitedArray is workable')