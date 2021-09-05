from alarm import Alarm
import schedule
import time


def startAlarm():
    print("時間です")
    Sound()


def Sound():
    print("音楽再生")


schedule.every().monday.at("01:00").do(Alarm)
schedule.every().tuesday.at("01:00").do(Alarm)

while True:
    schedule.run_pending()
    time.sleep(1)
