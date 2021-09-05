with open('test.py', 'w') as f:
    f.write('from alarm import Alarm\n')
    f.write('import schedule\n')
    f.write('import time\n')
    f.write('import set_alarm\n')
    f.write('\n')
    f.write('def startAlarm():\n')
    f.write('    print("時間です")\n')
    f.write('    Sound()\n')
    f.write('\n')
    f.write('def Sound():\n')
    f.write('    print("音楽再生")\n')
    f.write('\n')
    alarms = Alarm.query.all()

    print(alarms)

    for alarm in alarms:
        repeat_list = [int(x) for x in list(str(alarm.repeat_id))]

        for repeat_id in repeat_list:
            print(repeat_id)
            if repeat_id == 1:
                set_alarm = 'schedule.every().monday.at("%s").do(Alarm)\n' % (alarm.time)
            elif repeat_id == 2:
                set_alarm = 'schedule.every().tuesday.at("%s").do(Alarm)\n' % (alarm.time)
            elif repeat_id == 3:
                set_alarm = 'schedule.every().wednesday.at("%s").do(Alarm)\n' % (alarm.time)
            elif repeat_id == 4:
                set_alarm = 'schedule.every().thursday.at("%s").do(Alarm)\n' % (alarm.time)
            elif repeat_id == 5:
                set_alarm = 'schedule.every().friday.at("%s").do(Alarm)\n' % (alarm.time)
            elif repeat_id == 6:
                set_alarm = 'schedule.every().saturday.at("%s").do(Alarm)\n' % (alarm.time)
            elif repeat_id == 7:
                set_alarm = 'schedule.every().sunday.at("%s").do(Alarm)\n' % (alarm.time)

            f.write(set_alarm)

    f.write('\n')
    f.write('while True:\n')
    f.write('    schedule.run_pending()\n')
    f.write('    time.sleep(1)\n')
