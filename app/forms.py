from django import forms
from datetime import datetime, date, timedelta
import datetime

# 現在の月を取得
month = date.today().month
# 現在の日を取得
day = date.today().day
# 現在の曜日を取得
weekday_flag = date.today().weekday()
flag = {0:'月', 1:'火', 2:'水', 3:'木', 4:'金', 5:'土', 6:'日'}
weekday = flag[weekday_flag]
# 現在の時間を取得
hour = datetime.datetime.now().hour
# 現在の分を取得
minute = datetime.datetime.now().minute

DATE_CHOICES = []
# 現在時刻が00:00～17:29の場合
if hour <  17 or ( hour == 17 and minute < 30 ):
    # 本日から1週間分を取得
    days = [date.today() + timedelta(days=day) for day in range(7)]
    for i in range(7):
        if i == 0:
            DATE_CHOICES.append(
                (str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")" + "【本日】",
                str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")" + "【本日】")
            )
        else:
            DATE_CHOICES.append(
                (str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")",
                str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")")
            )
# 現在時刻が17:30以降の場合
elif hour > 17 or ( hour == 17 and minute > 29 ):
    # 翌日から1週間分を取得
    days = [date.today() + timedelta(days=day) for day in range(8)]
    for i in range(1, 8):
        if i == 1:
            DATE_CHOICES.append(
                (str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")" + "【明日】",
                str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")" + "【明日】")
            )
        else:
            DATE_CHOICES.append(
                (str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")",
                str(days[i].month) + "月" + str(days[i].day) + "日" + "(" + str(flag[days[i].weekday()]) + ")")
            )

TIME_CHOICES = []
# 現在時刻が00:00～17:29の場合
if hour <  17 or ( hour == 17 and minute < 30 ):
    # 現在時刻から30分後
    today_30 = datetime.timedelta.now() + datetime.timedelta(minute=30)
    # 30分後の分単位が30より小さい場合
    if today_30.minute < 30:
        for j in range(today_30.hour, 19):
            if j != today_30.hour:
                TIME_CHOICES.append(
                    (str(j) + ":" + "00",str(j) + ":" + "00")
                )
            if j < 18:
                TIME_CHOICES.append(
                    (str(j) + ":" + "30",str(j) + ":" + "30")
                )
    # 30分後の分単位が30より大きい場合
    if today_30.minute > 29:
        for j in range(today_30.hour, 19):
            if j != today_30.hour:
                TIME_CHOICES.append(
                    (str(j) + ":" + "00",str(j) + ":" + "00")
                )
            if j < 18:
                TIME_CHOICES.append(
                    (str(j) + ":" + "30",str(j) + ":" + "30")
                )
# 現在時刻が17:30以降の場合
elif hour > 17 or ( hour == 17 and minute > 29 ):
    for j in range(11, 19):
        if j != 11:
            TIME_CHOICES.append(
                (str(j) + ":" + "00",str(j) + ":" + "00")
            )
        if j < 18:
            TIME_CHOICES.append(
                (str(j) + ":" + "30",str(j) + ":" + "30")
            )

class ReceiptForm(forms.Form):
    date = forms.ChoiceField(
        widget=forms.Select,
        choices=DATE_CHOICES,
    )
    time = forms.ChoiceField(
        widget=forms.Select,
        choices=TIME_CHOICES,
    )