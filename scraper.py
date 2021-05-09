import re
import requests
import json
import time
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup

def download(year, semester):
    request = {}

    ### Course data
    request['r_search_type'] = 'F'
    request['boption'] = 'Search'
    request['acadsem'] = f'{year};{semester}'
    request['r_subj_code'] = ''
    request['staff_access'] = 'false'

    print("Downloading schedule html file. It might take a while...")
    response = requests.post("https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1", data=request)
    print("HTML file downloaded.")

    with open('raw_data.html', 'w') as f:
        f.write(response.text)
        
    return response.text

def normalise(raw_data):
    # Converts/removes redundant tags
    raw_data = raw_data.replace("<HR SIZE=2>", "")
    raw_data = raw_data.replace("<HR>", "")
    raw_data = raw_data.replace("<hr>", "")
    raw_data = raw_data.replace("<BR>", "")
    raw_data = raw_data.replace("<br>", "")
    raw_data = raw_data.replace("<br />", "")
    raw_data = raw_data.replace("<P>", "")
    raw_data = raw_data.replace("<p>", "")
    raw_data = raw_data.replace("&nbsp", "")
    raw_data = raw_data.replace("^", "")
    raw_data = raw_data.replace("</FORM>", "")
    raw_data = raw_data.replace("</form>", "")
    raw_data = raw_data.replace("<CENTER><FONT SIZE=4 FACE=\"Arial\">", "<FONT SIZE=4 FACE=\"Arial\">")
    raw_data = raw_data.replace("<CENTER>", "")
    raw_data = raw_data.replace("</CENTER>", "")
    raw_data = raw_data.replace("</center>", "")

    raw_data = raw_data.replace("COLOR=#0000FF", "")
    raw_data = raw_data.replace("COLOR=#FF00FF", "")
    raw_data = raw_data.replace("SIZE=2", "")
    raw_data = raw_data.replace("SIZE=4", "")
    raw_data = raw_data.replace("COLOR=black", "")
    raw_data = raw_data.replace("</FONT></B></B>", "</FONT></B></CENTER></B>")
    raw_data = re.sub(r'/&(?!#?[a-z0-9]+)/', '&amp', raw_data)

    raw_data = raw_data.replace("<body>", "<BODY>")
    raw_data = raw_data.replace("</body>", "</BODY>")
    raw_data = raw_data.replace("<TABLE  border>", "<TABLE>")
    raw_data = raw_data.replace("<table  border>", "<TABLE>")
    raw_data = raw_data.replace("<table >", "<TABLE>")
    raw_data = raw_data.replace("</table>", "</TABLE>")
    raw_data = raw_data.replace("<tr>", "<TR>")
    raw_data = raw_data.replace("</tr>", "</TR>")
    raw_data = raw_data.replace("<td>", "<TD>")
    raw_data = raw_data.replace("</td>", "</TD>")
    raw_data = raw_data.replace("</b>", "</B>")
    raw_data = raw_data.replace("<b>", "<B>")

    raw_data = re.sub(r"/ +/", " ", raw_data)
    raw_data = raw_data.replace('\n', ' ').replace('\r', '')
    
    return raw_data

def read_value(cell):
    # Facilitates reading of empty cells
    if cell.b != None:
        return cell.b.contents[0]
    else:
        return None

def parse(raw_data):
    print("Parsing raw HTML data...")
    time.sleep(1) # Makes it look like it is loading
    
    soup = BeautifulSoup(raw_data, 'html.parser')
    all_tables = soup.find_all('table')
    
    course_tables = all_tables[0::2] # Every odd table is a course info table
    schedule_tables = all_tables[1::2] # Every even table is a schedule table
    
    
    # Initialise course information
    course_info = []
    
    for course_info_table in course_tables:
        course_info_rows = course_info_table.tr.find_all('td')
        course_code = course_info_rows[0].b.font.contents[0]
        course_name = course_info_rows[1].b.font.contents[0].rstrip('*#')
        
        course_info.append((course_code, course_name))
    
    # Initialise tutorial schedules
    tut_schedule = defaultdict(list)

    for i, schedule_table in enumerate(schedule_tables):
        schedule_rows = schedule_table.find_all('tr')[1:] # discard header
        
        for row in schedule_rows:
            schedule_cell_values = row.find_all('td')
            if schedule_cell_values[0].b.contents: # found a new index, aka index cell is non-empty
                curr_index = schedule_cell_values[0].b.contents[0]
            
            # then/else reads the lessons for the current index
            class_type = read_value(schedule_cell_values[1])
            if class_type == 'TUT' or class_type == 'SEM':
                day = read_value(schedule_cell_values[3])
                class_time = read_value(schedule_cell_values[4])
                venue = read_value(schedule_cell_values[5])
                
                # if any of these cells are empty or venue is online, we ignore that index
                if (not day) or (not class_time) or (not venue) or (venue.lower() == 'online'):
                    continue
                
                course_code = course_info[i][0]
                
                # saving redundant data as tut_schedule might be used for other purposes later
                tut_schedule[venue].append((day, class_time, course_code, curr_index, class_type))
    
    print("HTML data parsed.")
                 
    with open(r"tut.json", "w") as output_file:
        json.dump(tut_schedule, output_file, indent=4)
        print("All tutorial schedules stored as tut.json.")
    
    with open(r"config", "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d")) # Change the last updated time
        print("Updated config file.")

# A facade method
def scrape(year, semester):
    raw_data = download(year, semester)
    raw_data = normalise(raw_data)
    parse(raw_data)
    print("Scraping completed.")
