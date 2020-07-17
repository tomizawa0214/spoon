from django import forms
from datetime import datetime, date, timedelta
import datetime
import locale

# 現在日時を取得
dt = datetime.datetime.now()
# dt = datetime.datetime(year=2020, month=7, day=17, hour=18, minute=00)
# 日本語表記の曜日名・月名
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

DATE_CHOICES = []
def get_weeks(start_day, box):
    for i in range(7):
        if i == 0:
            box.append(
                (days[i].strftime("%B%-d日(%a)") + start_day, days[i].strftime("%B%-d日(%a)") + start_day)
            )
        else:
            box.append(
                (days[i].strftime("%B%-d日(%a)"), days[i].strftime("%B%-d日(%a)"))
            )

# 現在時刻が00:00～16:29
if dt.hour <  16 or ( dt.hour == 16 and dt.minute < 30 ):
    # 本日から1週間分を取得
    days = [dt + timedelta(days=day) for day in range(7)]
    get_weeks("【本日】", DATE_CHOICES)
# 現在時刻が16:30以降
elif dt.hour > 16 or ( dt.hour == 16 and dt.minute > 29 ):
    # 翌日から1週間分を取得
    days = [dt + timedelta(days=day+1) for day in range(7)]
    get_weeks("【明日】", DATE_CHOICES)

# 当日注文不可指定の場合
NO_TODAY_CHOICES = []
days = [dt + timedelta(days=day+1) for day in range(7)]
get_weeks("【明日】", NO_TODAY_CHOICES)


TIME_CHOICES = []
def get_times(start_time, box):
    for j in range(start_time, 18):
        if j != start_time:
            box.append(
                (str(j) + ":" + "00",str(j) + ":" + "00")
            )
        if j < 17:
            box.append(
                (str(j) + ":" + "30",str(j) + ":" + "30")
            )

# 現在時刻が11:00～16:29
if 11 <= dt.hour <  16 or ( dt.hour == 16 and dt.minute < 30 ):
    # 現在時刻から30分後
    today_30 = dt + datetime.timedelta(minutes=30)
    # 30分後の分単位が30より小さい場合
    if today_30.minute < 30:
        get_times(today_30.hour, TIME_CHOICES)
    # 30分後の分単位が30より大きい場合
    elif today_30.minute >= 30:
        for j in range(today_30.hour+1, 18):
            TIME_CHOICES.append(
                (str(j) + ":" + "00",str(j) + ":" + "00")
            )
            if j < 17:
                TIME_CHOICES.append(
                    (str(j) + ":" + "30",str(j) + ":" + "30")
                )
        
# 現在時刻が16:30～翌10:59
elif ( dt.hour == 16 and dt.minute >= 30 ) or ( dt.hour >= 17 ) or ( dt.hour < 11 ):
    get_times(11, TIME_CHOICES)

FULLTIME_CHOICES = []
get_times(11, FULLTIME_CHOICES)


class ReceiptForm(forms.Form):
    date = forms.ChoiceField(widget=forms.Select, choices=DATE_CHOICES, required=False)
    no_today = forms.ChoiceField(widget=forms.Select, choices=NO_TODAY_CHOICES, required=False)
    time = forms.ChoiceField(widget=forms.Select, choices=TIME_CHOICES, required=False)
    fulltime = forms.ChoiceField(widget=forms.Select, choices=FULLTIME_CHOICES, required=False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea())