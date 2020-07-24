from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import ReceiptForm, ContactForm
from .models import PickUp, WhatsNew, TodayOrder, Order, Cart, SizeItem, FlavorItem, OptionItem
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from datetime import timedelta
import datetime
import re

class OrderThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 未注文のカート件数を取得
        count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/order_thanks.html', {
            'count': count
        })

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
            order.receipt = receipt

            # 注文日を登録
            if receipt[-12] == '月':
                order_day = int(receipt[-11])
            else:
                order_day = int(receipt[-12:-10])
            order.order_day = order_day

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

        return redirect('order_thanks')


class OrderConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
        # 上記レコードの各合計値をリストで取得
        total_price = [i.get_total_item_price() for i in cart_data]
        # 総合計値を取得
        get_total_price = sum(total_price)

        # 未注文のカート件数を取得
        count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/order_confirm.html', {
            'cart_data': cart_data,
            'get_total_price': get_total_price,
            'count': count
        })

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST or None)
        receipt_form = ReceiptForm(request.POST or None)

        if profile_form.is_valid() and receipt_form.is_valid():
            name = profile_form.cleaned_data['name']
            furigana = profile_form.cleaned_data['furigana']
            email = profile_form.cleaned_data['email']
            tel = profile_form.cleaned_data['tel']

            if receipt_form.cleaned_data['date'] != '':
                date = receipt_form.cleaned_data['date']
            else:
                date = receipt_form.cleaned_data['no_today']
            if '本日' in date:
                time = receipt_form.cleaned_data['time']
            else:
                time = receipt_form.cleaned_data['fulltime']

            # ログインユーザーの注文未完了レコードをすべて取得
            cart_data = Cart.objects.filter(user=request.user, ordered=False).order_by('id')
            # 上記レコードの各合計値をリストで取得
            total_price = [i.get_total_item_price() for i in cart_data]
            # 総合計値を取得
            get_total_price = sum(total_price)

            return render(request, 'app/order_confirm.html', {
                'name': name,
                'furigana': furigana,
                'email': email,
                'tel': tel,
                'date': date,
                'time': time,
                'cart_data': cart_data,
                'get_total_price': get_total_price,
            })

        # 当日受付の有無
        if TodayOrder.objects.filter(is_active=True).exists():
            today_order = True
        else:
            today_order = False

        return render(request, 'app/order_user.html', {
            'profile_form': profile_form,
            'receipt_form': receipt_form,
            'today_order': today_order,
        })


class OrderUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ログインユーザーと紐づける
        user_data = CustomUser.objects.get(id=request.user.id)
        profile_form = ProfileForm(
            request.POST or None,
            initial={
                'name': user_data.name,
                'furigana': user_data.furigana,
                'email': user_data.email,
                'tel': user_data.tel
            }
        )
        receipt_form = ReceiptForm(request.POST or None)

        # 当日受付の有無
        if TodayOrder.objects.filter(is_active=True).exists():
            today_order = True
        else:
            today_order = False

        # 未注文のカート件数を取得
        count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/order_user.html', {
            'profile_form': profile_form,
            'receipt_form': receipt_form,
            'today_order': today_order,
            'count': count
        })


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        size_item = SizeItem.objects.all()
        flavor_item = FlavorItem.objects.filter(is_active=True)
        option_item = OptionItem.objects.all()

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
            'option_item': option_item,
            'cart_data': cart_data,
            'get_total_price': get_total_price,
            'msg': msg,
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

        data = {
            'get_total_price': get_total_price,
        }
        return JsonResponse(data)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        # 未注文のカート件数を取得
        count = None
        if request.user.is_authenticated:
            count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/about.html', {
            'count': count
        })


class AccessView(View):
    def get(self, request, *args, **kwargs):
        # 未注文のカート件数を取得
        count = None
        if request.user.is_authenticated:
            count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/access.html', {
            'count': count
        })


class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        # 未注文のカート件数を取得
        count = None
        if request.user.is_authenticated:
            count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/contact.html', {
            'form': form,
            'count': count
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
                # ひらがなを含む場合のみメール送信
                if re.search('[ぁ-ん]', message) != None:
                    message = EmailMessage(subject=subject, body=body, to=to_list, bcc=bcc_list)
                    message.send()
                else:
                    return HttpResponse("メッセージ内容に問題が発生したため、送信がキャンセルされました。")
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")

            return redirect('contact_thanks')

        return render(request, 'app/contact.html', {
            'form': form
        })


class ContactThanksView(View):
    def get(self, request, *args, **kwargs):
        # 未注文のカート件数を取得
        count = None
        if request.user.is_authenticated:
            count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/contact_thanks.html', {
            'count': count
        })


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
        # 未注文のカート件数を取得
        count = None
        if request.user.is_authenticated:
            count = Cart.objects.filter(user=request.user, ordered=False).count()

        return render(request, 'app/index.html', {
            'news_data': news_data,
            'pick_data': pick_data,
            'count': count
        })