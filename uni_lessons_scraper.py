import requests as r
from ics import Calendar
from datetime import datetime, date
import re
import json
import pytz
from notion_lessons import add_lesson

timezone = pytz.timezone('Europe/Rome')


class Event:
    def __init__(self, title, start_time, end_time, isFlutter):
        self.subject = self.get_subject(title)
        if isFlutter:
            self.date = start_time.strftime('%Y-%m-%d')
            self.start_time = start_time.strftime('%Y-%m-%d-%H:%M')
            self.end_time = end_time.strftime('%Y-%m-%d-%H:%M')
        else:
            self.date = start_time.isoformat()
            self.start_time = start_time.isoformat()
            self.end_time = end_time.isoformat()
        self.teacher = self.get_teacher(title)
        self.classroom = self.get_classroom(title)

    def get_teacher(self, title):
        teachers = ["Scolozzi Donato", "Pulimeno Marco", "Surano Paolo"]
        for i in range(len(teachers)):
            if teachers[i] in title:
                return teachers[i]
        return "Unknown"

    def get_subject(self, title):
        subjects = ["INFORMATICA", "INGLESE", "ANALISI"]
        for i in range(len(subjects)):
            if subjects[i] in title:
                return subjects[i]
            elif "FEST" in title or "Sospensione" in title:
                return None
        return "Unknown"

    def get_classroom(self, title):
        pattern = rf"(?<={self.teacher.split()[-1]})(.*?)(?=\[)"
        match = re.search(pattern, title)
        if match:
            return match.group().strip()
        
        return None


def get_lessons(isFlutter):
    response = r.get(
        "https://logistica.unisalento.it/PortaleStudenti/export/ec_download_ical_list.php?view=easycourse&form-type=corso&include=corso&txtcurr=&anno=2024&corso=LB55&anno2%5B%5D=999%7C1&visualizzazione_orario=cal&date=22-10-2024&periodo_didattico=S1&_lang=it&list=1&week_grid_type=-1&ar_codes_=&ar_select_=&col_cells=0&empty_box=0&only_grid=0&highlighted_date=0&all_events=0&faculty_group=0&_lang=it&ar_codes_=ECING_LB55_999_1_ER|ECING_LB55_999_1_PULIM|ECING_LB55_999_1_ER-143|ECING_LB55_999_1_ER-144&ar_select_=true|true|true|true&txtaa=2024/2025&txtcorso=INGEGNERIA%20INFORMATICA%20(Laurea)&txtanno=&docente=&attivita=&txtdocente=&txtattivita="
    )

    if response.status_code == 200:
        with open("lezioni.ics", "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return []

    with open("lezioni.ics", "r") as f:
        calendar = Calendar(f.read())

    events = []
    for event in calendar.events:
        if event.begin.date() >= date.today():
            start_time = event.begin
            end_time = event.end
            event_instance = Event(
                event.name,
                start_time,
                end_time,
                isFlutter
            )
            events.append(event_instance)

    events_data = [event.__dict__ for event in events]
    with open('classes.json', "w") as json_file:
        json.dump(events_data, json_file, indent=4)
        
    return events
