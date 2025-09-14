# entwickelbar2calendar
import datetime

from bs4 import BeautifulSoup
import requests


__version__ = "0.0.3"


URL = "https://entwickelbar.github.io/"
date = datetime.date(2025, 9, 13)


def beautify_time(time_raw):
    """ Verbessert und standardisiert die Zeitangabe
    für den nächsten Verarbeitungsschritt.""" 
    if "ab " in time_raw:
        # Fälle: 'ab 9:30' - wir vervollständigen für einen 30-Minuten-Slot
        time = time_raw.replace("ab ", "")
        hour, minutes = time.split(":")
        if minutes == "30":
            return f"{hour}:{minutes}-{int(hour) + 1}:00"
        else:
            return f"{hour}:{minutes}-{hour}:30"
    elif " - " in time_raw:
        # Fälle: '10:30 - 11:15' - wir normalisieren
        return time_raw.replace(" - ", "-").strip()
    else:
        # Fälle: '10:00' - wir vervollständigen für einen 30-Minuten-Slot
        hour, minutes = time_raw.split(":")
        if minutes == "00":
            return f"{hour}:{minutes}-{hour}:{30}"
        elif minutes == "30":
            return f"{hour}:{minutes}-{int(hour) + 1}:00"
    return time_raw


def main():

    # 1. Datenstruktur aufbauen und hierzu Daten von der Website holen
    
    events = []

    web = requests.get(URL)
    soup = BeautifulSoup(web.text, "html5lib")

    table = soup.find("table", attrs={"class" : "table table-striped"})
    trs = table.find_all("tr")

    for tr in trs[1:]:
        tds = tr.find_all("td")
        time, description = "", ""
        for i, td in enumerate(tds):
            if i == 0:
                time = beautify_time(td.text)
            elif i == 1:
                description = td.text.strip()
            print(i, td.text)
        events.append([time, description])

    print("*****")
    print(events)

    # 2. Wir erzeugen und speichern eine ics-Datei für die Entwickelbar
    #    Das Modul ics konnte nicht genutzt werden, weil es Zeitzonen nicht unterstützt

    output = []
    output.append("BEGIN:VCALENDAR")
    output.append("VERSION:2.0")
    output.append("CALSCALE:GREGORIAN")
    
    for i, event in enumerate(events):
        time, description = event
        start_hour, start_minute, end_hour, end_minute = time.replace("-",":").split(":")

        output.append("BEGIN:VEVENT")
        output.append(f"UID:{i}@{URL}") 
        output.append(f"DTSTART;TZID=Europe/Berlin:{str(date).replace("-","")}T{int(start_hour):02d}{int(start_minute):02d}00") 
        output.append(f"DTEND;TZID=Europe/Berlin:{str(date).replace("-","")}T{int(end_hour):02d}{int(end_minute):02d}00") 
        output.append(f"SUMMARY:{description}") 
        output.append("END:VEVENT")

    output.append("END:VCALENDAR")

    with open('entwickelbar.ics', 'w') as f:
        f.writelines("\n".join(output))

    
if __name__ == "__main__":
    main()
