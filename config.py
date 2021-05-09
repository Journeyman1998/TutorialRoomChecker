from datetime import datetime

SEMESTER_1 = 8 #aug of year
SEMESTER_2 = 1 #jan of year

def get_year_semester(year, month):
    if month >= SEMESTER_1:
        return year, 1
    else:
        return year-1, 2
        
def get_current_year_semester():
    now = datetime.now()
    return get_year_semester(now.year, now.month)

def check_data_valid():
    with open('config', "r") as f:
        last_updated = f.read()
    last_updated = datetime.strptime(last_updated, "%Y-%m-%d")
    
    data_year = last_updated.year
    data_month = last_updated.month
    data_acad_year, data_semester = get_year_semester(data_year, data_month)
    acad_year, semester = get_current_year_semester()
    
    data_valid = (acad_year == data_acad_year) and (semester == data_semester)

    return data_valid, acad_year, semester