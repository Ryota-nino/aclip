import pygame.mixer
import schedule
import time
import set_alarm

# アラーム処理

# アラームが追加削除されるごとにいちいち行を追加したり削除したりする的な？
# set_alarm.pyにschedule.every()とかを格納してこっちで実行する


def Alarm():
    print("時間です")
#   print("\007")  #ビープ音
    # Sound()
    # exit()  # これがないと無限ループになるので注意

    # 音再生処理


# def Sound():
#     pygame.mixer.init()  # 初期化
#     pygame.mixer.music.load('alerm1.mp3')  # 読み込み
#     pygame.mixer.music.play(-1)  # ループ再生（引数を1にすると1回のみ再生）
#     input()
#     pygame.mixer.music.stop()  # 終了


# alarm = Alarm.query.get(id)

# アラーム時間設定

# 曜日指定
# schedule.every().monday.at(alarm.time).do(Alarm)
# schedule.every().tuesday.at(alarm.time).do(Alarm)
# schedule.every().wednesday.at(alarm.time).do(Alarm)
# schedule.every().thursday.at(alarm.time).do(Alarm)
# schedule.every().friday.at(alarm.time).do(Alarm)
# schedule.every().saturday.at(alarm.time).do(Alarm)
# schedule.every().sunday.at(alarm.time).do(Alarm)
# 毎日
# schedule.every().day.at(alarm.time).do(Alarm)
job = schedule.every().day.at("15:06").do(Alarm)
# job = schedule.every().day.at("15:07").do(Alarm)
# schedule.cancel_job(job)

set_alarm.setAlarm()

# アラーム待ち
while True:
    schedule.run_pending()
    time.sleep(1)
