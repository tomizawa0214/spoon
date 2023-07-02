from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import ReceiptForm, ContactForm
from .models import PickUp, WhatsNew, TodayOrder, Order, Cart, SizeItem, FlavorItem, OptionItem
from accounts.models import CustomUser
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from datetime import datetime, date, timedelta
import datetime
import locale
import re

class OrderThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/order_thanks.html')

    def post(self, request, *args, **kwargs):
        # ログインユーザーの注文未完了カートをオーダーに登録。カートが無い間違い注文は除外
        cart_data = Cart.objects.filter(user=request.user, ordered=False)
        if cart_data.exists():
            # ログインユーザーの注文未完了レコードをすべて完了にする
            for cart in cart_data:
                cart.ordered = True
                cart.save()

            # 注文者情報を登録
            order = Order(user=request.user)
            order.name = request.POST.get('name')
            order.furigana = request.POST.get('furigana')
            order.email = request.POST.get('email')
            order.tel = request.POST.get('tel')
            receipt = request.POST.get('receipt')
            receipt_date = make_aware(datetime.datetime.strptime(receipt, '%Y-%m-%d %H:%M'))
            order.receipt = receipt_date

            # 注文日を登録
            order_day = receipt_date.day
            order.order_day = order_day

            # クーポン使用有無を登録
            coupon_price = int(request.POST.get('coupon'))
            if coupon_price > 0:
                order.coupon_use = True
                order.coupon_price = coupon_price

            # 注文番号を登録
            x = 1
            while Order.objects.filter(order_day=order_day, count=x, flag=False).exists():
                x += 1
            order.count = x
            order.save()

            # カートを登録
            order.cart.set(cart_data)

            # ログインユーザーの最新の注文を取得
            order_latest = Order.objects.filter(user=request.user).last()
            # 注文番号を作成
            order_id = str(order_latest.order_day) + str(order_latest.count)

            context = {
                'order_latest': order_latest,
                'order_id': order_id,
                'coupon_price': coupon_price
            }

            subject = render_to_string('app/mail_template/order_subject.txt', context)
            message = render_to_string('app/mail_template/order_message.txt', context)
            to_list = [order.email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=message, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")

        return JsonResponse({'data': 'data'})


class OrderConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
        # 上記レコードの各合計値をリストで取得
        total_price = [i.get_total_item_price() for i in cart_data]
        # 総合計値を取得
        get_total_price = sum(total_price)

        # 現在日時を取得
        dt = datetime.datetime.now()
        # 今年のクーポン利用を確認
        if not Order.objects.filter(user=request.user, coupon_use=True, coupon_day__contains=dt.year).exists():
            # 誕生月を取得
            birthmonth = 0
            user_data = CustomUser.objects.get(id=request.user.id)
            birthday = user_data.birthday
            if birthday != None:
                birthmonth = birthday.month
            # 現在月と誕生月を確認
            if dt.month == birthmonth:
                coupon = 'get'
            else:
                coupon = 'no'
        else:
            coupon = 'no'

        # シングルサイズを取得
        single_size_data = SizeItem.objects.filter(title='シングルサイズ')[0]
        single_price = single_size_data.price

        return render(request, 'app/order_confirm.html', {
            'cart_data': cart_data,
            'single_price': single_price,
            'get_total_price': get_total_price,
            'coupon': coupon
        })

    def post(self, request, *args, **kwargs):
        form = ReceiptForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            furigana = form.cleaned_data['furigana']
            email = form.cleaned_data['email']
            tel = form.cleaned_data['tel']
            date = request.POST.get('date')
            if '本日' in date or '明日' in date:
                time = request.POST.get('time')
            else:
                time = request.POST.get('fulltime')

            # ログインユーザーの注文未完了レコードをすべて取得
            cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
            # 上記レコードの各合計値をリストで取得
            total_price = [i.get_total_item_price() for i in cart_data]
            # 総合計値を取得
            get_total_price = sum(total_price)

            # 現在日時を取得
            dt = datetime.datetime.now()
            # 今年のクーポン利用を確認
            if not Order.objects.filter(user=request.user, coupon_use=True, coupon_day__contains=dt.year).exists():
                # 誕生月を取得
                birthmonth = 0
                user_data = CustomUser.objects.get(id=request.user.id)
                birthday = user_data.birthday
                if birthday != None:
                    birthmonth = birthday.month
                # 現在月と誕生月を確認
                if dt.month == birthmonth:
                    coupon = 'get'
                else:
                    coupon = 'no'
            else:
                coupon = 'no'

            # カートにシングルサイズを含むか確認
            if cart_data.filter(size_title='シングルサイズ').exists() and coupon == 'get':
                use_coupon = 'valid'
            else:
                use_coupon = 'invalid'

            # シングルサイズを取得
            single_size_data = SizeItem.objects.filter(title='シングルサイズ')[0]
            single_price = single_size_data.price

            return render(request, 'app/order_confirm.html', {
                'name': name,
                'furigana': furigana,
                'email': email,
                'tel': tel,
                'date': date,
                'time': time,
                'cart_data': cart_data,
                'single_price': single_price,
                'get_total_price': get_total_price,
                'coupon': coupon,
                'use_coupon': use_coupon
            })

        # 当日受付の有無
        if TodayOrder.objects.filter(is_active=True).exists():
            today_order = True
        else:
            today_order = False

        # 現在日時を取得
        dt = datetime.datetime.now()
        # dt = datetime.datetime(2021, 8, 2, 12, 10)
        # 日本語表記の曜日名・月名
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

        date_list = []
        def get_weeks(start_day):
            for i in range(10):
                if i == 0:
                    date_list.append(days[i].strftime('%B%-d日(%a)') + start_day)
                else:
                    date_list.append(days[i].strftime('%B%-d日(%a)'))

        # 現在時刻～16:30
        if dt.time() < datetime.time(16, 31) and today_order == True:
            # 本日から1週間分を取得
            days = [dt + timedelta(days=day) for day in range(10)]
            get_weeks("【本日】")
        # 現在時刻が16:31以降
        elif dt.time() >= datetime.time(16, 31) or today_order == False:
            # 翌日から1週間分を取得
            days = [dt + timedelta(days=day+1) for day in range(10)]
            get_weeks("【明日】")

        # 7月の休業日
        date_list = [
            j for j in date_list if \
            '7月3日' not in j and \
            '7月4日' not in j and \
            '7月10日' not in j and \
            '7月11日' not in j and \
            '7月18日' not in j and \
            '7月24日' not in j and \
            '7月25日' not in j and \
            '7月31日' not in j
        ]

        # 7月の火曜日は【明日】追加
        if (
            (dt.month == 7 and dt.day == 4) or \
            (dt.month == 7 and dt.day == 11) or \
            (dt.month == 7 and dt.day == 18) or \
            (dt.month == 7 and dt.day == 25)
        ) and dt.time() < datetime.time(16, 31) and today_order == True:
            date_list[0] += '【明日】'

        # 当日受付用
        time_list = []
        def get_times(start_time):
            handle_time = start_time
            # 現在時刻から10分毎の時間を取得
            while start_time.hour < 17:
                if handle_time.hour == start_time.hour: 
                    time_list.append(handle_time.strftime('%H:%M'))
                    next_time = handle_time + timedelta(minutes=10)
                    handle_time = next_time
                else:
                    break
            # 17:00まで30分毎の時間を取得
            while(True):
                time_list.append(handle_time.strftime('%H:%M'))
                next_time = handle_time + timedelta(minutes=30)
                if next_time.time() <= datetime.time(17):
                    handle_time = next_time
                else:
                    break

        def get_fulltimes(box, hour, minute):
            handle_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour, minute))
            while(True):
                box.append(handle_time.strftime('%H:%M'))
                next_time = handle_time + timedelta(minutes=30)
                if next_time.time() <= datetime.time(17):
                    handle_time = next_time
                else:
                    break

        # 休業日は明日以降の予約
        if (
            (dt.month == 7 and dt.day == 3) or \
            (dt.month == 7 and dt.day == 4) or \
            (dt.month == 7 and dt.day == 10) or \
            (dt.month == 7 and dt.day == 11) or \
            (dt.month == 7 and dt.day == 18) or \
            (dt.month == 7 and dt.day == 24) or \
            (dt.month == 7 and dt.day == 25) or \
            (dt.month == 7 and dt.day == 31)
        ):
            get_fulltimes(time_list)
        else:
            # 現在時刻が12:30～16:30
            if datetime.time(12, 30) <= dt.time() < datetime.time(16, 31) and today_order == True:
                # 現在時刻から30分後を取得
                after_30 = dt.replace(second=0, microsecond=0) + timedelta(minutes=30)
                # 30分後の一の位を取得
                after_30_one = ''.join(list(reversed(str(after_30.minute))))[0]
                # 10分毎の値に丸める
                if after_30_one != "0":
                    round_time = 10 - int(after_30_one)
                    after_30 += timedelta(minutes=round_time)
                # 10分毎のリストを作成
                get_times(after_30)
            # 現在時刻が16:31～翌10:59
            elif dt.time() >= datetime.time(16, 31) or dt.time() < datetime.time(12, 30) or today_order == False:
                get_fulltimes(time_list)

        fulltime_list = []
        get_fulltimes(fulltime_list)

        return render(request, 'app/order_user.html', {
            'form': form,
            'date_list': date_list,
            'time_list': time_list,
            'fulltime_list': fulltime_list
        })


class OrderUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ログインユーザーと紐づける
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ReceiptForm(
            request.POST or None,
            initial={
                'name': user_data.name,
                'furigana': user_data.furigana,
                'email': user_data.email,
                'tel': user_data.tel
            }
        )

        # 当日受付の有無
        if TodayOrder.objects.filter(is_active=True).exists():
            today_order = True
        else:
            today_order = False

        # 現在日時を取得
        dt = datetime.datetime.now()
        # dt = datetime.datetime(2023, 6, 6, 12, 20)
        # 日本語表記の曜日名・月名
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

        date_list = []
        def get_weeks(start_day):
            for i in range(10):
                if i == 0:
                    date_list.append(days[i].strftime('%B%-d日(%a)') + start_day)
                else:
                    date_list.append(days[i].strftime('%B%-d日(%a)'))

        # 現在時刻～16:30
        if dt.time() < datetime.time(16, 31) and today_order == True:
            # 本日から1週間分を取得
            days = [dt + timedelta(days=day) for day in range(10)]
            get_weeks("【本日】")
        # 現在時刻が16:31以降
        elif dt.time() >= datetime.time(16, 31) or today_order == False:
            # 翌日から1週間分を取得
            days = [dt + timedelta(days=day+1) for day in range(10)]
            get_weeks("【明日】")

        # 7月の休業日
        date_list = [
            j for j in date_list if \
            '7月3日' not in j and \
            '7月4日' not in j and \
            '7月10日' not in j and \
            '7月11日' not in j and \
            '7月18日' not in j and \
            '7月24日' not in j and \
            '7月25日' not in j and \
            '7月31日' not in j
        ]

        # 7月の火曜日は【明日】追加
        if (
            (dt.month == 7 and dt.day == 4) or \
            (dt.month == 7 and dt.day == 11) or \
            (dt.month == 7 and dt.day == 18) or \
            (dt.month == 7 and dt.day == 25)
        ) and dt.time() < datetime.time(16, 31) and today_order == True:
            date_list[0] += '【明日】'

        # 当日受付用
        time_list = []
        def get_times(start_time):
            handle_time = start_time
            # 現在時刻から10分毎の時間を取得
            while start_time.hour < 17:
                if handle_time.hour == start_time.hour: 
                    time_list.append(handle_time.strftime('%H:%M'))
                    next_time = handle_time + timedelta(minutes=10)
                    handle_time = next_time
                else:
                    break
            # 17:00まで30分毎の時間を取得
            while(True):
                time_list.append(handle_time.strftime('%H:%M'))
                next_time = handle_time + timedelta(minutes=30)
                if next_time.time() <= datetime.time(17):
                    handle_time = next_time
                else:
                    break

        def get_fulltimes(box):
            handle_time = datetime.datetime.combine(datetime.date.today(), datetime.time(13, 00))
            while(True):
                box.append(handle_time.strftime('%H:%M'))
                next_time = handle_time + timedelta(minutes=30)
                if next_time.time() <= datetime.time(17):
                    handle_time = next_time
                else:
                    break
            
        # 休業日は明日以降の予約
        if (
            (dt.month == 7 and dt.day == 3) or \
            (dt.month == 7 and dt.day == 4) or \
            (dt.month == 7 and dt.day == 10) or \
            (dt.month == 7 and dt.day == 11) or \
            (dt.month == 7 and dt.day == 18) or \
            (dt.month == 7 and dt.day == 24) or \
            (dt.month == 7 and dt.day == 25) or \
            (dt.month == 7 and dt.day == 31)
        ):
            get_fulltimes(time_list)
        else:
            # 現在時刻が12:30～16:30
            if datetime.time(12, 30) <= dt.time() < datetime.time(16, 31) and today_order == True:
                # 現在時刻から30分後を取得
                after_30 = dt.replace(second=0, microsecond=0) + timedelta(minutes=30)
                # 30分後の一の位を取得
                after_30_one = ''.join(list(reversed(str(after_30.minute))))[0]
                # 10分毎の値に丸める
                if after_30_one != "0":
                    round_time = 10 - int(after_30_one)
                    after_30 += timedelta(minutes=round_time)
                # 10分毎のリストを作成
                get_times(after_30)
            # 現在時刻が16:31～翌10:59
            elif dt.time() >= datetime.time(16, 31) or dt.time() < datetime.time(12, 30) or today_order == False:
                get_fulltimes(time_list)

        fulltime_list = []
        get_fulltimes(fulltime_list)
        print(time_list)
        print(fulltime_list)

        return render(request, 'app/order_user.html', {
            'form': form,
            'date_list': date_list,
            'time_list': time_list,
            'fulltime_list': fulltime_list
        })


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        size_item = SizeItem.objects.order_by('id')
        flavor_item = FlavorItem.objects.filter(web_only=False, is_active=True).order_by('sort')
        flavor_web = FlavorItem.objects.filter(web_only=True, is_active=True).order_by('sort')
        option_item = OptionItem.objects.order_by('id')

        # 再注文を受けてデータベース登録が無い場合の処理
        msg = ''
        if 'msg' in request.GET:
            msg = request.GET['msg']

        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
        # 上記レコードの各合計値をリストで取得
        total_price = [i.get_total_item_price() for i in cart_data]
        # 総合計値を取得
        get_total_price = sum(total_price)

        return render(request, 'app/order.html', {
            'size_item': size_item,
            'flavor_item': flavor_item,
            'flavor_web': flavor_web,
            'option_item': option_item,
            'cart_data': cart_data,
            'get_total_price': get_total_price,
            'msg': msg
        })


class AddOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        size_title = request.POST.get('size_title')
        size_price = request.POST.get('size_price')
        flavor_title = request.POST.get('flavor_title')
        flavor_price = request.POST.get('flavor_price')
        flavor2_title = request.POST.get('flavor2_title')
        flavor2_price = request.POST.get('flavor2_price')
        option_title = request.POST.get('option_title')
        option_price = request.POST.get('option_price')
        option2_title = request.POST.get('option2_title')
        option2_price = request.POST.get('option2_price')
        option3_title = request.POST.get('option3_title')
        option3_price = request.POST.get('option3_price')
        option4_title = request.POST.get('option4_title')
        option4_price = request.POST.get('option4_price')

        cart = Cart()
        cart.user = request.user
        cart.size_title = size_title
        cart.size_price = size_price
        cart.size_image = SizeItem.objects.get(title=size_title).image
        cart.flavor_title = flavor_title
        cart.flavor_price = flavor_price
        cart.flavor_image = FlavorItem.objects.get(title=flavor_title).image
        cart.flavor2_title = flavor2_title
        cart.flavor2_price = flavor2_price
        if flavor2_title != '':
            cart.flavor2_image = FlavorItem.objects.get(title=flavor2_title).image
        cart.option_title = option_title
        if option_title != '':
            cart.option_image = OptionItem.objects.get(title=option_title).image
        cart.option_price = option_price
        cart.option2_title = option2_title
        cart.option2_price = option2_price
        if option2_title != '':
            cart.option2_image = OptionItem.objects.get(title=option2_title).image
        cart.option3_title = option3_title
        cart.option3_price = option3_price
        if option3_title != '':
            cart.option3_image = OptionItem.objects.get(title=option3_title).image
        cart.option4_title = option4_title
        cart.option4_price = option4_price
        if option4_title != '':
            cart.option4_image = OptionItem.objects.get(title=option4_title).image
        cart.save()

        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
        # 上記レコードの各合計値をリストで取得
        total_price = [i.get_total_item_price() for i in cart_data]
        # 総合計値を取得
        get_total_price = sum(total_price)
        # 最新レコードのidを取得
        cart_id = cart_data.last().id
        # カート件数を取得
        count = cart_data.count()

        data = {
            'size_title': size_title,
            'size_price': size_price,
            'flavor_title': flavor_title,
            'flavor_price': flavor_price,
            'flavor2_title': flavor2_title,
            'flavor2_price': flavor2_price,
            'option_title': option_title,
            'option_price': option_price,
            'option2_title': option2_title,
            'option2_price': option2_price,
            'option3_title': option3_title,
            'option3_price': option3_price,
            'option4_title': option4_title,
            'option4_price': option4_price,
            'get_total_price': get_total_price,
            'cart_id': cart_id,
            'count': count
        }
        return JsonResponse(data)


class DeleteOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_value = request.POST.get('id_value')

        # 該当レコードを削除
        del_record = Cart.objects.filter(user=request.user, pk=id_value)
        del_record.delete()

        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
        # 上記レコードの各合計値をリストで取得
        total_price = [i.get_total_item_price() for i in cart_data]
        # 総合計値を取得
        get_total_price = sum(total_price)
        # カート件数を取得
        count = Cart.objects.filter(user=request.user, ordered=False).count()

        data = {
            'get_total_price': get_total_price,
            'count': count
        }
        return JsonResponse(data)


class MenuView(View):
    def get(self, request, *args, **kwargs):
        flavor_item = FlavorItem.objects.filter(web_only=False, is_active=True).order_by('sort')
        flavor_web = FlavorItem.objects.filter(web_only=True, is_active=True).order_by('sort')
        size_item = SizeItem.objects.order_by('id')

        return render(request, 'app/menu.html', {
            'flavor_item': flavor_item,
            'flavor_web': flavor_web,
            'size_item': size_item,
        })


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/about.html')


class OrderGuideView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/order_guide.html')


class AccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/access.html')


class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        return render(request, 'app/contact.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            context = {
                'name': name,
                'email': email,
                'message': message,
            }

            subject = render_to_string('app/mail_template/contact_subject.txt', context)
            body = render_to_string('app/mail_template/contact_message.txt', context)
            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=body, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")

            return redirect('contact_thanks')

        return render(request, 'app/contact.html', {
            'form': form
        })


class ContactThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/contact_thanks.html')


class SctlView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/sctl.html')


class PrivacyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/privacy.html')


class CompanyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/company.html')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # 前日日付分の注文フラグを完了にする
        yesterday = datetime.datetime.now() - timedelta(days=1)
        if Order.objects.filter(order_day=yesterday.day, flag=False).exists():
            order_yesterday = Order.objects.filter(order_day=yesterday.day, flag=False)
            for order in order_yesterday:
                order.flag = True
                order.save()
        else:
            pass

        # 最新7件を取得
        news_data = WhatsNew.objects.all().order_by('-id')[0:7]
        # 最新2件を取得
        pick_data = PickUp.objects.all().order_by('-id')[0:2]

        # 現在日時を取得
        dt = datetime.datetime.now()
        # 今年のクーポン利用を確認
        if CustomUser.objects.filter(id=request.user.id).exists():
            if not Order.objects.filter(user=request.user, coupon_use=True, coupon_day__contains=dt.year).exists():
                # 誕生月を取得
                birthmonth = 0
                user_data = CustomUser.objects.get(id=request.user.id)
                birthday = user_data.birthday
                if birthday != None:
                    birthmonth = birthday.month
                # 現在月と誕生月を確認
                if dt.month == birthmonth:
                    coupon = 'get'
                else:
                    coupon = 'no'
            else:
                coupon = 'no'
        else:
            coupon = 'no'

        return render(request, 'app/index.html', {
            'news_data': news_data,
            'pick_data': pick_data,
            'coupon': coupon
        })