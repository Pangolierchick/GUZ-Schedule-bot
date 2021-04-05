HOLIDAY_STR = 'holiday'
DAY_OF_WEEK_MAP = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def numToWeekDayStr(num:int):
    return DAY_OF_WEEK_MAP[num]

class ScheduleRecord:
    def __init__(self, b_time:str, e_time:str, subject:str):
        self.b_time  = str(b_time)
        self.e_time  = str(e_time)
        self.subject = str(subject)
#================================    
    def setBeginTime(self, b_time:str):
        self.b_time = str(b_time)
    
    def setEndTime(self, e_time:str):
        self.e_time = str(e_time)
    
    def setSubject(self, subject:str):
        self.subject = str(subject)
#================================
    def beginTime(self):
        return self.b_time
    
    def endTime(self):
        return self.e_time
    
    def subject(self):
        return self.subject
#================================
    
    def __str__(self):
        return f'{self.b_time}-{self.e_time} {self.subject}'

class Schedule:
    def __init__(self):
        pass

    def recordToSchRecords(self, string:str):
        records = []

        for i in string.split(';'):
            if i.strip() != HOLIDAY_STR:
                split_rec = i.split(maxsplit=1)
                b, e = split_rec[0].split('-')
                
                records.append(ScheduleRecord(b, e, split_rec[1]))
            else:
                records.append(HOLIDAY_STR)
        
        return records   
    
    def getByDay(self, day:int) -> str:
        day = numToWeekDayStr(day)
        return " ; ".join(map(str, self.schedule[day]))
    
    def parse_schedule_file(self, filename:str) -> dict:
        self.schedule = {}
        with open(filename, 'r') as f:
            f.readline() # skipping first line

            for line in f:
                day = line.split(',')
                self.schedule[day[0].strip()] = self.recordToSchRecords(day[1])
        
        return self.schedule
    
    def dump_to_file(self, filename:str) -> None:
        with open(filename, 'w') as f:
            f.write("Day of the week , Schedule\n")
            for k, v in self.schedule.items():
                f.write(k + ' , ')
                for i, r in enumerate(v):
                    f.write(str(r))
                    if i != len(v) - 1:
                        f.write(' ; ')

                f.write('\n')

    def __str__(self):
        str_schedule = ""

        for k, v in self.schedule.items():
                str_schedule += k + "\n"
                for i in v:
                    str_schedule += '\t' + str(i) + '\n'
        
        return str_schedule

    def print(self):
        print(str(self))
