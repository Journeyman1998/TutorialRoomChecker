import json
import time as t
from datetime import datetime, date
from collections import defaultdict

    
def load_schedule():
    with open("tut.json", "r") as input_file:
        tut_schedule = json.load(input_file)
    print("Tutorial schedule read from tut.json.")
    return tut_schedule

def get_time(time_string):
    return datetime.combine(date.min, datetime.strptime(time_string, '%H%M').time())

def get_duration_hour(time_delta):
    return time_delta.seconds/3600

START_TIME = get_time('0800')
END_TIME = get_time('1900')

def init_lookup():
    tut_schedule = load_schedule()
    print("Converting raw schedule into lookup dictionary...")
    t.sleep(1)
    
    # Consolidate all the lessons that will be held in each tutorial room, organised by days
    tut_day_time = {}
    for room, schedules in tut_schedule.items():
        tut_day_time[room] = defaultdict(set)
        
        for lesson in schedules:
            day = lesson[0]
            time = lesson[1]            
            tut_day_time[room][day].add(time) # Here, redundant information is removed, e.g class index, course code

        for day in tut_day_time[room].keys():
            set_to_list = list(tut_day_time[room][day])
            tut_day_time[room][day] = sorted(set_to_list) # so that the blocks of class time are arranged chronologically
            
    # "Invert" the tutorial schedule. Gets all the free blocks of time (no classes held during those times)
    lookup = defaultdict(list)
    
    for room, days in tut_day_time.items():
        for day, times in days.items():
            curr_time = START_TIME # The earliest possible time for a class
            
            for time in times:
                start = time.split('-')[0]
                end = time.split('-')[1]
                start_time = get_time(start)
                end_time = get_time(end)
                
                if start_time < curr_time:
                    continue
                free_time = get_duration_hour(start_time - curr_time) # free duration between class blocks
                free_time = int(free_time * 10)/10 
                if free_time > 0.0:
                    lookup[free_time].append((day, curr_time.strftime("%H:%M"), room))
                
                curr_time = min(end_time, END_TIME) # Finds the next block
                
            # need to consider the block after the last class
            free_time = get_duration_hour(END_TIME - curr_time)
            if free_time > 0.0:
                lookup[free_time].append((day, curr_time.strftime('%H:%M'), room))
                
    
    with open("lookup.json", "w") as f:
        json.dump(lookup, f, indent=4)
        print("Lookup cache file stored as lookup.json.")

def load_lookup():
    with open("lookup.json", "r") as f:
        return json.load(f)
