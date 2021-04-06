from datetime import date


HOLIDAY_STR = ['Holiday', 'Выходной']
DAY_OF_WEEK_MAP_US = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday']
DAY_OF_WEEK_MAP_RU = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье']
TIME_MAP = {
    "8:30-10:00": 0,
    "10:10-11:40": 1,
    "11:50-13:20": 2,
    "14:00-15:30": 3,
    "15:40-17:10": 4,
    "17:20-18:50": 5}

LESSON_TIME = [
    "08:30-10:00",
    "10:10-11:40",
    "11:50-13:20",
    "14:00-15:30",
    "15:40-17:10",
    "17:20-18:50"
]

STRING_NUM_WEEKDAY = {
    'Понедельник': 0,
    'Вторник': 1,
    'Среда': 2,
    'Четверг': 3,
    'Пятница': 4,
    'Суббота': 5,
    'Воскресенье': 6}

WEEK_DAY_LOCALE = DAY_OF_WEEK_MAP_RU
HOLIDAY_LOCATE = HOLIDAY_STR[1]


def numToWeekDayStr(num: int):
    return DAY_OF_WEEK_MAP_RU[num]


def timeToNum(time: str):
    return TIME_MAP[time]


class ScheduleException(Exception):
    pass


class SubjectAlreadyExists(ScheduleException):
    def __init__(self, expression, message):
        self.message = message
        self.expression = expression


class Subject:
    def __init__(self, subject: str, tutor: str = None, classroom: int = None):
        self.subject = str(subject).strip().capitalize()
        self.tutor = None
        self.classroom = None


        if tutor is not None:
            self.tutor = str(tutor).strip().capitalize()

            if len(self.tutor) <= 1:
                self.tutor = None

        if classroom is not None:
            self.classroom = int(classroom)

    def __str__(self):
        tutor = self.tutor
        classroom = self.classroom

        if tutor == None:
            tutor = ''

        if classroom == None:
            classroom = ''

        return f'{self.subject} {tutor} {classroom}'.strip()


class DaySchedule:
    def __init__(self):
        self.day_schedule = {
            LESSON_TIME[0]: None,
            LESSON_TIME[1]: None,
            LESSON_TIME[2]: None,
            LESSON_TIME[3]: None,
            LESSON_TIME[4]: None,
            LESSON_TIME[5]: None
        }

    def set_subject(self, subject: Subject, lesson_num: int) -> None:
        self.day_schedule[LESSON_TIME[lesson_num]] = subject

    def get_subject(self, lesson_num: int) -> Subject:
        return self.day_schedule[LESSON_TIME[lesson_num]]

    def __str__(self):
        string = ''
        for i, v in self.day_schedule.items():
            if v is not None:
                string += f'\t{i} {v}\n'

        return string


class GroupSchedule:
    def __init__(self, group_name: str, subgroup: int):
        self.group_name = str(group_name)
        self.subgroup = int(subgroup)
        self.schedule = {
            WEEK_DAY_LOCALE[0]: None,
            WEEK_DAY_LOCALE[1]: None,
            WEEK_DAY_LOCALE[2]: None,
            WEEK_DAY_LOCALE[3]: None,
            WEEK_DAY_LOCALE[4]: None,
            WEEK_DAY_LOCALE[5]: '\t' + HOLIDAY_LOCATE + '\n',
            WEEK_DAY_LOCALE[6]: '\t' + HOLIDAY_LOCATE + '\n',
        }

        self.print_holidays = False

    def set_day_at(self, day_schedule: DaySchedule, dayn: int):
        self.schedule[WEEK_DAY_LOCALE[dayn]] = day_schedule

    def get_day_at(self, dayn: int) -> DaySchedule:
        return self.schedule[WEEK_DAY_LOCALE[dayn]]
    
    def get_today(self) -> DaySchedule:
        return self.get_day_at(date.today().weekday())
    
    def delete_day_at(self, dayn):
        self.set_day_at(None, dayn)

    def __str__(self):
        string = ''
        for i, v in self.schedule.items():
            if v is not None:
                if i in (WEEK_DAY_LOCALE[5], WEEK_DAY_LOCALE[6]) and not self.print_holidays:
                    break

                string += i + '\n'
                string += str(v)

        return string

    def get_from_file(self, filename: str):
        with open(filename, 'r') as f:
            f.readline()  # skipping header

            for i in f:
                d, sch = i.split(',')

                day = DaySchedule()

                for j in sch.split(';'):
                    # 8:30-10:00 SUBJECT { | TUTOR | CLASSROOM} ; ... {} -- means optional
                    time, sub_part = j.split(maxsplit=1)
                    sub_part = sub_part.split("|")

                    sub_part_list = [None, None, None]
                    for i, v, in enumerate(sub_part):
                        sub_part_list[i] = v.strip()

                    subject = Subject(
                        sub_part_list[0], sub_part_list[1], sub_part_list[2])

                    day.set_subject(subject, TIME_MAP[time.strip()])

                self.set_day_at(
                    day, STRING_NUM_WEEKDAY[d.strip().capitalize()])

        return self
    
    def print(self):
        print(str(self))
