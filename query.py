def filter_day(day):
    def f(time):
        return time[0] == day
    return f

def filter_start_time(start_time):
    def f(time):
        return start_time == None or time[1] == start_time
    return f

def query(lookup, duration, day, start_time=None):
    duration_key = str(duration) #convert from float to string
    if start_time != None:
        start_time = start_time.strftime("%H:%M") #convert from datetime.time to string
    all_time = []
    for key in lookup.keys():
        if key >= duration_key:
            all_time.extend(lookup[key])
    
    all_time = filter(filter_day(day), all_time)
    all_time = filter(filter_start_time(start_time), all_time)
            
    return sorted(list(all_time), key=lambda l: (l[1], l[2]))