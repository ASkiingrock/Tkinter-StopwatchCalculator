from datetime import datetime
import re

def MillisToHMSM(time): # Argument is an int

    millis = int(str(time)[-3:]) # 3 from the end
    time -= millis # Find number of miliseconds and then minus them so it will be in seconds

    hours = time//3600000 # If no hours, it will just be 0
                          # 3600 seconds per hour *1000 milliseconds
    time -= hours*3600000 # Find number of hours then minus them

    minutes = time//60000 # same with minutes
                          # 60 seconds per minute *1000 milliseconds
    time -= minutes*60000 # Find number of minutes

    seconds = time//1000 # Find number of seconds

    if hours == 0: # Formatting
        if minutes == 0: # If less than 1 minute, make it "S.M"
            return f'{seconds:02}.{millis:03}'
        else: # If between 1 minute and 1 hour, make it "M:S.M"
            return f'{minutes:02}:{seconds:02}.{millis:03}'
    return f'{hours:02}:{minutes:02}:{seconds:02}.{millis:03}' # If more than an hour, return "H:M:S.M"

def convertToMillis(time): # HMSM to millis
    timeSplit = time.split(":") # Convert to ["H", "M", "S.M"]
                                # If there's no colon, it will just be the same
    if len(timeSplit) == 1: # If only seconds and millis
        Millis = int(timeSplit[0].split(".")[1]) + int(timeSplit[0].split(".")[0])*1000
    elif len(timeSplit) == 2: # If there are minutes, include those
        Millis = int(timeSplit[1].split(".")[1]) + int(timeSplit[1].split(".")[0])*1000 + int(timeSplit[0])*60000
    elif len(timeSplit) == 3: # If there are hours, include those
        Millis = int(timeSplit[2].split(".")[1]) + int(timeSplit[2].split(".")[0])*1000 + int(timeSplit[1])*60000 + int(timeSplit[0])*3600000
    return Millis

def GetTime():
    s2 = datetime.now().isoformat(sep=' ', timespec='milliseconds')[11:] # Gets time in format "HOUR:MINUTE:SECOND.MILLISECONDS"
    return s2

def newstopwatch(startTime, offset):
    return MillisToHMSM(convertToMillis(GetTime()) - convertToMillis(startTime) + offset) 
    # One liner now due to the functions
    # Take difference in milliseconds of current time and starttime, add the offset (time which it started), then convert to "H:M:S.M"

def printLapPlain(list):
    times = ""

    # Time:         Difference:
    # 00:00:00.000  00:00:00.000

    times += list[0]
    times += ' '*(14-len(list[0]))

    times += list[1]
    times += ' '*(12-len(list[1]))
    return times


def printMultipleLaps(list):
    if list == []:
        return ''
    dictLaps = {}
    output = ''
    for i,j in enumerate(list):
        dictLaps[str(i)] = printLapPlain(j)
    
    for item in dictLaps.keys():
        if item == "0":
            pass
        else:
            if int(item) < 1000:
                output += '\n' + item + ' '*(4-len(item)) + dictLaps[item]
            elif int(item) > 999:
                output += '\n999 ' + dictLaps[item]

    return output[1:]

def analyseTime(inputstring): 
    # Regexes to determine whether the time is valid
    # If the time is of the form ss.mmm / mm:ss.mmm / hh:mm:ss.mmm, that is valid already.
    # If the time is of the form ss / mm:ss / hh:mm:ss, i need to add .000 on the end so it can be interpreted by the convertToMillis function.
    # If the time is of the form s / m:ss / h:mm:ss, i need to add .000 on the end and a 0 in front of it.

    validTimeInSeconds = str.isdigit(inputstring) # Int value represents seconds

    validTimeNoMillis = bool(re.match("(^\d+[:]\d\d$)|(^\d+[:]\d+[:]\d\d$)", inputstring)) # mm:ss / hh:mm:ss

    validTimeNoFirstDigit = bool(re.match("(^\d[.]\d\d\d$)|(^\d[:]\d\d[.]\d\d\d$)|(^\d[:]\d\d[.]\d\d\d$)", inputstring)) # s.mmm / m:ss.mmm / h:mm:ss.mmm

    validTimeNoFirstOrMillis = bool(re.match("(^\d$)|(^\d[:]\d\d$)|(^\d[:]\d\d[:]\d\d$)", inputstring)) # s / m:ss / h:mm:ss

    if validTimeNoFirstDigit: # Add a zero at the start
        inputstring = "0" + inputstring
    elif validTimeNoMillis: # Add 3 zeroes for the milliseconds
        inputstring += ".000"
    elif validTimeNoFirstOrMillis: # Add both
        inputstring = "0" + inputstring + ".000" # Format correctly
    elif validTimeInSeconds: # Converts it to the proper form since itis already in Milliseconds
        inputstring = MillisToHMSM(int(inputstring)*1000)

    if bool(re.match("(^\d+[:]\d\d[.]\d{1,3}$)|(^\d+[.]\d{1,3}$)|(^\d+[:]\d\d[:]\d\d[.]\d{1,3}$)", inputstring)):
		# Fat regex
		# 3 conditions: 1st - m+:ss.m{1-3} allows any amount of minutes, 2 seconds digits and 1-3 millisecond values
		# 2nd - Any amount of seconds and 1-3 millisecond values
		# 3rd - Same but allows any amount of hours and only 2 minute digits
        inputstring += "0"*(3-len(inputstring.split(".")[1])) # Add on appropriate amount of milliseconds
        inputstring = MillisToHMSM(convertToMillis(inputstring)) # Converts it to proper format
        return True, inputstring # Returns true
    else:
        return False, "" # Not a valid time