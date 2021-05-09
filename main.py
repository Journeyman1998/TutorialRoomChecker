from datetime import datetime
import os

import scraper, config, cache_init, query

def init_program():
    """
    Initialise the lookup dictionary for query.
    
    If the data is outdated (checks by last updated time) or the lookup dictionary file does not exist locally,
    the scraper and cache_init is called to create the lookup file.
    """
    data_updated, acad_year, semester = config.check_data_valid()

    # if data outdated or data not scraped yet
    if not data_updated or not os.path.exists("lookup.json"):
        scraper.scrape(acad_year, semester) # Download and parse html data
        cache_init.init_lookup() # Convert parsed html into lookup dictionary for query
    
    lookup = cache_init.load_lookup() # Loads the lookup dictionary from file
    print(lookup.keys())
    return lookup

def ask_start_time():
    """Asks the user for start time. Used to filter the available tutorial rooms."""
    
    userinput = input("Enter start time (HH:MM), 'NIL' for any start time: ")
    try:
        if userinput.lower() == 'nil': # if user has no preferred start time
            return None
        else:
            time = datetime.strptime(userinput, "%H:%M").time() # try to create the datetime object
            return time
    except:
        print("Invalid start time!")
        return -1
    
def ask_day():
    """Asks the user for the day. Used to filter the available tutorial rooms"""
    
    DAY = {'1': 'MON', '2':'TUE', '3':'WED', '4':'THU', '5':'FRI', '6':'SAT', '7':'SUN'}
    userinput = input("Enter day (MON - 1, SUN - 7): ")
    try:
        day = DAY[userinput]
        return day
    except:
        print("Invalid day value!")
        return -1

def ask_duration():
    """Asks the user for the duration. Used to filter the available tutorial rooms."""
    
    userinput = input("Enter duration (in hours): ")
    try:
        duration = float(userinput)
        duration = int(duration * 10) / 10 # Round off to one decimal place
        return duration
    except:
        print("Invalid duration!")
        return -1
  
def display(results):
    if not results:
        return
    
    for result in results:
        location = result[2]
        time = result[1]
        print(f'{location} - {time}')
  
def start():
    lookup = init_program()

    while True: 
        print("\n\n")
        print("Tutorial Room Availability Checker")
        print("----------------------------------")
        
        duration = -1
        day = -1
        start_time = -1
        while duration == -1:
            duration = ask_duration()
        
        while day == -1:
            day = ask_day()
        
        while start_time == -1:
            start_time = ask_start_time()
        
        results = query.query(lookup, duration, day, start_time)
        display(results)
        
        quit_program = input("Exit program? (Y - yes): ")
        if quit_program == 'Y' or quit_program == 'y':
            break
    
    print("See you!")

if __name__ == "__main__":
    start()