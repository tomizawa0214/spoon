from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import ReceiptForm
from .models import Order, Cart, SizeItem, FlavorItem, OptionItem
from accounts.models import CustomUser
from accounts.forms import ProfileForm
# from django.conf import settings
# from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
# import textwrap


class OrderThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/order_thanks.html')

    def post(self, request, *args, **kwargs):
        # OrderHistoryへ注文履歴として保管
        for cart in Cart.objects.all():
            order_history = OrderHistory(
                size_title=cart.size_title,
                size_price=cart.size_price,
                flavor_title=cart.flavor_title,
                flavor_title_2=cart.flavor_title_2,
                option_title=cart.option_title,
                option_price=cart.option_price,
                option_title_2=cart.option_title_2,
                option_price_2=cart.option_price_2,
                total_price=cart.total_price
            )
            order_history.save()
        
        order = Order()
        order.name = request.POST.get('name')
        order.furigana = request.POST.get('furigana')
        order.email = request.POST.get('email')
        order.tel = request.POST.get('tel')
        order.receipt = request.POST.get('receipt')
        order.save()

        # ログインユーザーのカートを削除
        cart = Cart.objects.get(user=request.user)
        cart.delete()

        return redirect('order_thanks')


class OrderConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # ログインユーザーの注文内容をすべて取得
        cart_data = Cart.objects.get(user=request.user)
        # 注文合計金額を取得
        get_total_price = Cart.objects.order_by("id").last().total_price

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

            # 注文内容をすべて取得
            cart_data = Cart.objects.all()
            # 注文合計金額を取得
            get_total_price = Cart.objects.order_by("id").last().total_price

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

        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False)

        # 最新の合計金額を取得。初期値は0
        if cart_data.exists():
            get_total_price = cart_data.order_by('id').last().total_price
        else:
            get_total_price = 0
        
        # 最新レコードのidを取得
        cart_id = cart_data.values_list('id', flat=True).last()

        return render(request, 'app/order.html', {
            'size_item': size_item,
            'flavor_item': flavor_item,
            'option_item': option_item,
            'cart_data': cart_data,
            'get_total_price': get_total_price,
            'cart_id': cart_id,
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
        total_price = request.POST.get('total_price')

        # 合計値のカンマを除いて整数値に変換
        total_price = int(total_price.replace(',', ''))

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
        cart.total_price = total_price
        cart.save()

        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False)
        # 最新の合計金額を取得
        get_total_price = cart_data.order_by('id').last().total_price
        # 最新レコードのidを取得
        cart_id = cart_data.values_list('id', flat=True).last()

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
            'total_price': total_price,
            'get_total_price': get_total_price,
            'cart_id': cart_id,
        }
        return JsonResponse(data)


class DeleteOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_value = request.POST.get('id_value')

        del_record = Cart.objects.filter(user=request.user, pk=id_value) # 削除するレコードを取得
        size_price = del_record.values_list('size_price', flat=True)[0] # 削除するレコードのサイズ金額を取得
        flavor_price = del_record.values_list('flavor_price', flat=True)[0] # 削除するレコードのフレーバー金額を取得
        flavor2_price = del_record.values_list('flavor2_price', flat=True)[0] # 削除するレコードのフレーバー金額を取得
        option_price = del_record.values_list('option_price', flat=True)[0]  # 削除するレコードのオプション金額を取得
        option2_price = del_record.values_list('option2_price', flat=True)[0] # 削除するレコードのオプション金額を取得
        option3_price = del_record.values_list('option3_price', flat=True)[0] # 削除するレコードのオプション金額を取得

        # ログインユーザーの注文未完了レコードをすべて取得
        cart_data = Cart.objects.filter(user=request.user, ordered=False)
        # 最新レコードの合計値から削除分の金額を引いて更新
        cart_latest = cart_data.order_by('id').last()
        cart_latest.total_price = cart_latest.total_price - (
                size_price + flavor_price + flavor2_price + option_price + option2_price + option3_price
            )
        cart_latest.save()

        # 指定レコードを削除
        del_record.delete()

        # 最新レコードの合計値を取得
        get_total_price = cart_latest.total_price

        data = {
            'get_total_price': get_total_price,
        }
        return JsonResponse(data)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html')