import myschedule
import os
import logging as log

class SchedulePoolException(Exception):
    pass

class ScheduleFileNotFound(SchedulePoolException):
    def __init__(self, message):
        self.message = message

class ScheduleDirNotFound(SchedulePoolException):
    def __init__(self, message):
        self.message = message

class GroupDirNotFound(SchedulePoolException):
    def __init__(self, message):
        self.message = message


class SchedulePool:
    SCHEDULES_DIR = '../data/schedules'
    
    LOWER = 0
    UPPER  = 1
    
    def __init__(self, week_type:int=0):
        self.pool = {}
        self.week_type = int(week_type)

    def find_schedule_dir(self, schedule_name:str) -> str:
        for dir in os.scandir(SchedulePool.SCHEDULES_DIR):
            if schedule_name == dir.name:
                return dir.path
        
        raise ScheduleDirNotFound(f'Schedule dir not found for {schedule_name}')
    
    def find_group_subdir(self, group_path:str, subgroup:int):
        for dir in os.scandir(group_path):
            if dir.name == str(subgroup):
                return dir.path
        
        raise GroupDirNotFound(f'Group sub dir {subgroup} not found for {group_path}')
    
    def find_schedule_file(self, subgroup_path:str):
        if self.week_type == SchedulePool.LOWER:
            file_suffix = 'L'
        else:
            file_suffix = "U"

        for file in os.scandir(subgroup_path):
            filename = os.path.splitext(file.name)[0]
            if filename[-1] == file_suffix:
                return file.path
        
        raise ScheduleFileNotFound(f'Schedule file with {file_suffix} suffix not found')
    
    def load_schedule(self, groupname:str, subgroup:int) -> myschedule.GroupSchedule:
        schedule_name = groupname + '_' + str(subgroup)
        
        if schedule_name not in self.pool:
            sch_dir = self.find_schedule_dir(groupname)
            subgroup_dir = self.find_group_subdir(sch_dir, subgroup)
            schedule_file_name = self.find_schedule_file(subgroup_dir)

            schedule = myschedule.GroupSchedule(groupname, subgroup)
            schedule.get_from_file(schedule_file_name)

            self.pool[schedule_name] = schedule

            log.info(f"Loaded another schedule. Current len: {len(self.pool)}")

            return schedule
    
    def get_schedule(self, group_name:str, subgroup:int) -> myschedule.GroupSchedule:
        schedule_name = group_name + '_' + str(subgroup)
        log.debug(f'Getting schedule for {schedule_name}. Current week type: {self.week_type}')

        if schedule_name in self.pool:
            return self.pool[schedule_name]
        
        return self.load_schedule(group_name, subgroup)
    
    def reload_pool(self):
        pass
    
    def clean_pool(self):
        self.pool = {}
    
    def set_week_type(self, week_type:int):
        self.week_type = int(week_type)


def poolUpdater(pool:SchedulePool):
    pass
