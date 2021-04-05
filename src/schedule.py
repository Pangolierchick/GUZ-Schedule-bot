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
            time, subject = i.split()
            b, e = time.split('-')
            
            records.append(ScheduleRecord(b, e, subject))
    
    def parse_schedule_file(self, filename:str) -> dict:
        self.schedule = {}
        with open(filename, 'r') as f:
            f.readline() # skipping first line

            for line in f:
                day = line.split(',')
                self.schedule[day[0].strip()] = day[1].split(';')
        
        return self.schedule
    
    def dump_to_file(self, filename:str) -> None:
        with open(filename, 'w') as f:
            f.write("Day of the week , Schedule\n")
            for k, v in self.schedule.items():
                f.write(k + ' , ' + ' ; '.join(v))
    
    def __str__(self):
        str_schedule = ""

        for k, v in self.schedule.items():
            str_schedule += k + "\n"
            for i in v:
                str_schedule += f"\t{i.strip()}\n"
        
        return str_schedule

    def print(self):
        print(str(self))

schedule = Schedule()
schedule.parse_schedule_file('../data/default.csv')
schedule.print()
# schedule.dump_to_file('../data/test1.csv')

