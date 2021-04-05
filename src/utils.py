import re

def format_time(time:str):
    if not re.match('\d+.\d+.\d+', time):
        return time

    new_time = ''

    for i, v in enumerate(time.split('.')):
        new_time += str(int(v))
        if (i < 2):
            new_time += '-'
    
    return new_time
