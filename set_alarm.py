from alarm import Alarm
import schedule

alarms = Alarm.query.all()

for alarm in alarms:
    repeat_list = [int(x) for x in list(str(alarm.repeat_id))]
    set_alarm = "schedule.every().monday.at(${alarm.time}).do(Alarm)"

with open('write_file.py', 'w') as f:
    f.write('this is a test.\n')


def startAlarm():
    print("時間です")


def setAlarm():
    schedule.every().day.at("14:12").do(startAlarm)
