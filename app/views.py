from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import ReceiptForm
from .models import Order, Cart, SizeItem, FlavorItem, OptionItem
from accounts.models import CustomUser
from accounts.forms import ProfileForm
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


class OrderThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/order_thanks.html')

    def post(self, request, *args, **kwargs):
        # 注文者情報を登録
        order = Order(user=request.user)
        order.name = request.POST.get('name')
        order.furigana = request.POST.get('furigana')
        order.email = request.POST.get('email')
        order.tel = request.POST.get('tel')
        order.receipt = request.POST.get('receipt')
        order.save()

        # ログインユーザーの注文未完了カートをオーダーに登録
        cart_data = Cart.objects.filter(user=request.user, ordered=False)
        order.cart.set(cart_data)

        # ログインユーザーの注文未完了レコードをすべて完了にする
        for cart in cart_data:
            cart.ordered = True
            cart.save()

        order_latest = Order.objects.filter(user=request.user).last()
        order_id = Order.objects.order_by('id').last()

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

        return render(request, 'app/order_confirm.html', {
            'cart_data': cart_data,
            'get_total_price': get_total_price,
        })

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST or None)
        receipt_form = ReceiptForm(request.POST or None)

        if profile_form.is_valid() and receipt_form.is_valid():
            name = profile_form.cleaned_data['name']
            furigana = profile_form.cleaned_data['furigana']
            email = profile_form.cleaned_data['email']
            tel = profile_form.cleaned_data['tel']
            date = receipt_form.cleaned_data['date']
            time = receipt_form.cleaned_data['time']

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

        return render(request, 'app/order_user.html', {
            'profile_form': profile_form,
            'receipt_form': receipt_form,
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

        return render(request, 'app/order_user.html', {
            'profile_form': profile_form,
            'receipt_form': receipt_form,
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

        cart = Cart()
        cart.user = request.user
        cart.size_title = size_title
        cart.size_price = size_price
        cart.flavor_title = flavor_title
        cart.flavor_price = flavor_price
        cart.flavor2_title = flavor2_title
        cart.flavor2_price = flavor2_price
        cart.option_title = option_title
        cart.option_price = option_price
        cart.option2_title = option2_title
        cart.option2_price = option2_price
        cart.option3_title = option3_title
        cart.option3_price = option3_price
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


class AccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/access.html')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html')