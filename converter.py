import urllib.request as urllib
import json
from datetime import datetime,timedelta
import re


output="/tmp/muell.ics"
idx="termins"
city_id="71186"
area_id="71186"
#alert_lead_time_sec=21600
alert_length_time_sec=3600
url = "https://mymuell.jumomind.com/webservice.php?idx="+idx+"&city_id="+city_id+"&area_id="+area_id
#import_garbage_type=["EICH_BIO", "LK_EICH_PAP", "LK_EICH_REST", "LK_EICH_GELB3","LK_EICH_GELB2","LK_EICH_GELB1"]
import_garbage_type=["EICH_BIO", "LK_EICH_PAP", "LK_EICH_REST", "LK_EICH_GELB2"]
import_translation = {
'EICH_BIO': 'Grünzeug',
'LK_EICH_PAP': 'Pappzeug',
'LK_EICH_REST': 'Restzeug',
'LK_EICH_GELB3': 'Plastikzeug'}


def create_ical(cal_id, cal_garbage_type, cal_date_start, cal_date_end, cal_date_created):          
    return  "PRODID:peppisLittleHelper\r\n" \
            "METHOD:PUBLISH\r\n" \
            "BEGIN:VEVENT\r\n" \
            "UID:"+cal_id + "\r\n"\
            "LOCATION:Strasse\r\n" \
            "SUMMARY:"+cal_garbage_type + "\r\n" \
            "DESCRIPTION:"+cal_garbage_type + "\r\n" \
            "CLASS:PUBLIC\r\n" \
            "DTSTART;VALUE=DATE:" + datetime.strftime(cal_date_start,"%Y%m%d") + "\r\n" \
            "DTEND;VALUE=DATE:" + datetime.strftime(cal_date_end,"%Y%m%d") + "\r\n" \
            "DTSTAMP:" + datetime.strftime(cal_date_created,"%Y%m%dT%H%M%SZ") + "\r\n" \
            "END:VEVENT\r\n\r\n"  \
   

def multipleReplace(text, wordDict):
    """
    take a text and replace words that match the key in a dictionary
    with the associated value, return the changed text
    """
    for key in wordDict:
        text = text.replace(key, wordDict[key])
    return text

json_object = urllib.urlopen(url)
data = json.loads(json_object.read().decode())
f = open(output, "a")
f.write("BEGIN:VCALENDAR\r\n" \
"VERSION:2.0\r\n" )

for item in data:
    _data=(item["_data"])
    for _item in _data:
        if _item["cal_garbage_type"] in import_garbage_type:
            cal_id=_item["cal_id"]
            cal_date=_item["cal_date"]
            cal_date_normal=_item["cal_date_normal"]
            cal_garbage_type=_item["cal_garbage_type"]
            cal_comment=_item["cal_comment"]
            
            #convert string to datetime
            cal_date = datetime.strptime(cal_date, "%Y-%m-%d")
            
            #calc the cal_date_start & cal_date_end
            #cal_date_start=cal_date - timedelta(seconds=alert_lead_time_sec)
            #cal_date_end=cal_date - timedelta(seconds=alert_lead_time_sec) + timedelta(seconds=alert_length_time_sec)
            cal_date_start=cal_date 
            cal_date_end=cal_date + timedelta(seconds=alert_length_time_sec)
            
            cal_date_created = datetime.now()
            #replace the strings
            cal_garbage_type = multipleReplace(cal_garbage_type,import_translation)

            ical= create_ical(_item["cal_id"], cal_garbage_type, cal_date_start, cal_date_end, cal_date_created)

            f.write(ical)
f.write("END:VCALENDAR")
f.close()
