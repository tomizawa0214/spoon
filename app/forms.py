from django import forms
# from datetime import datetime, timedelta
# from datetime import datetime, date, timedelta
# import datetime
# import locale

# # 現在日時を取得
# dt = datetime.datetime.now()
# # dt = datetime.datetime(2019, 2, 26, 14, 9)
# # 日本語表記の曜日名・月名
# locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

# DATE_CHOICES = []
# def get_weeks(start_day, box):
#     for i in range(7):
#         if i == 0:
#             box.append(
#                 (days[i].strftime("%B%-d日(%a)") + start_day, days[i].strftime("%B%-d日(%a)") + start_day)
#             )
#         else:
#             box.append(
#                 (days[i].strftime("%B%-d日(%a)"), days[i].strftime("%B%-d日(%a)"))
#             )

# # 現在時刻～16:30
# if dt.time() < datetime.time(16, 31):
#     # 本日から1週間分を取得
#     days = [dt + timedelta(days=day) for day in range(7)]
#     get_weeks("【本日】", DATE_CHOICES)
# # 現在時刻が16:31以降
# elif dt.time() >= datetime.time(16, 31):
#     # 翌日から1週間分を取得
#     days = [dt + timedelta(days=day+1) for day in range(7)]
#     get_weeks("【明日】", DATE_CHOICES)

# # 当日注文不可指定の場合
# NO_TODAY_CHOICES = []
# days = [dt + timedelta(days=day+1) for day in range(7)]
# get_weeks("【明日】", NO_TODAY_CHOICES)


# # 当日受付用
# TIME_CHOICES = []
# def get_times(start_time):
#     handle_time = start_time
#     # 現在時刻から10分毎の時間を取得
#     while start_time.hour < 17:
#         if handle_time.hour == start_time.hour: 
#             TIME_CHOICES.append((handle_time.strftime('%H:%M'), handle_time.strftime('%H:%M')))
#             next_time = handle_time + timedelta(minutes=10)
#             handle_time = next_time
#         else:
#             break
#     # 17:00まで30分毎の時間を取得
#     while(True):
#         TIME_CHOICES.append((handle_time.strftime('%H:%M'), handle_time.strftime('%H:%M')))
#         next_time = handle_time + timedelta(minutes=30)
#         if next_time.time() < datetime.time(17):
#             handle_time = next_time
#         else:
#             break

# def get_fulltimes(box):
#     handle_time = datetime.datetime.combine(datetime.date.today(), datetime.time(11, 30))
#     while(True):
#         box.append((handle_time.strftime('%H:%M'), handle_time.strftime('%H:%M')))
#         next_time = handle_time + timedelta(minutes=30)
#         if next_time.time() <= datetime.time(17):
#             handle_time = next_time
#         else:
#             break

# # 現在時刻が11:00～16:30
# if datetime.time(11) <= dt.time() < datetime.time(16, 31):
#     # 現在時刻から30分後を取得
#     after_30 = dt.replace(second=0, microsecond=0) + timedelta(minutes=30)
#     # 30分後の一の位を取得
#     after_30_one = ''.join(list(reversed(str(after_30.minute))))[0]
#     # 10分毎の値に丸める
#     if after_30_one != 0:
#         round_time = 10 - int(after_30_one)
#         after_30 += timedelta(minutes=round_time)
#     # 10分毎のリストを作成
#     get_times(after_30)
# # 現在時刻が16:31～翌10:59
# elif dt.time() >= datetime.time(16, 31) or dt.time() < datetime.time(11):
#     get_fulltimes(TIME_CHOICES)

# FULLTIME_CHOICES = []
# get_fulltimes(FULLTIME_CHOICES)


# class ReceiptForm(forms.Form):
#     date = forms.ChoiceField(widget=forms.Select, choices=DATE_CHOICES, required=False)
#     no_today = forms.ChoiceField(widget=forms.Select, choices=NO_TODAY_CHOICES, required=False)
#     time = forms.ChoiceField(widget=forms.Select, choices=TIME_CHOICES, required=False)
#     fulltime = forms.ChoiceField(widget=forms.Select, choices=FULLTIME_CHOICES, required=False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea())