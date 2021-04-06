HOLIDAY_STR = ['Holiday', 'Выходной']
DAY_OF_WEEK_MAP_US = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAY_OF_WEEK_MAP_RU = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

def numToWeekDayStr(num:int):
    return DAY_OF_WEEK_MAP_RU[num]

class ScheduleRecord:
    def __init__(self, b_time:str, e_time:str, subject_a:str, subject_b:str=None):
        self.b_time  = str(b_time)
        self.e_time  = str(e_time)

        self.subject_a = str(subject_a)
        self.subject_b = str(subject_b)

        if self.subject_a.startswith('&&'):
            self.subject_b = self.subject_a[2:] # deleting &&
            self.subject_a = self.subject_a[2:]

#================================    
    def setBeginTime(self, b_time:str):
        self.b_time = str(b_time)
    
    def setEndTime(self, e_time:str):
        self.e_time = str(e_time)
    
    def setSubjectA(self, subject:str):
        self.subject_a = str(subject)
    
    def setSubjectB(self, subject:str):
        self.subject_b = str(subject)
#================================
    def beginTime(self):
        return self.b_time
    
    def endTime(self):
        return self.e_time
    
    def subjectA(self):
        return self.subject_a
    
    def subjectB(self):
        return self.subject_b
#================================
    
    def __str__(self):
        sa = self.subject_a
        sb = self.subject_b

        if self.subject_a == 'None':
            sa = '   '
        
        if self.subject_b == 'None':
            sb = '   '

        sa = sa.strip()
        sb = sb.strip()

        return f'{self.b_time:>5}-{self.e_time:<5} {sa:70}\t{sb:50}'

class Schedule:
    def __init__(self):
        pass

    def recordToSchRecords(self, string:str):
        records = []

        for i in string.split(';'):
            if i.strip() not in HOLIDAY_STR:
                split_rec = i.split(maxsplit=1)
                b, e = split_rec[0].split('-')
                subjects = split_rec[1].split('|')

                if len(subjects) == 1:
                    subjects.append('None')
                
                records.append(ScheduleRecord(b, e, subjects[0], subjects[1]))
            else:
                records.append(HOLIDAY_STR[1])
        
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
        str_schedule = "\tГруппа А\t\t\t\t\t\t\t\t\t\tГруппа Б\n\n"

        for k, v in self.schedule.items():
                str_schedule += k + "\n"
                for i in v:
                    str_schedule += '\t' + str(i) + '\n'
        
        return str_schedule

    def print(self):
        print(str(self))
