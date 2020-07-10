from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import ReceiptForm
from .models import OrderItem, Order, SizeItem, FlavorItem, OptionItem
from accounts.models import CustomUser
from accounts.forms import ProfileForm
# from django.conf import settings
# from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
# import textwrap


# class OrderThanksView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'app/order_thanks.html')

#     def post(self, request, *args, **kwargs):
#         # OrderHistoryへ注文履歴として保管
#         for cart in Cart.objects.all():
#             order_history = OrderHistory(
#                 size_title=cart.size_title,
#                 size_price=cart.size_price,
#                 flavor_title=cart.flavor_title,
#                 flavor_title_2=cart.flavor_title_2,
#                 option_title=cart.option_title,
#                 option_price=cart.option_price,
#                 option_title_2=cart.option_title_2,
#                 option_price_2=cart.option_price_2,
#                 total_price=cart.total_price
#             )
#             order_history.save()
        
#         order = Order()
#         order.name = request.POST.get('name')
#         order.furigana = request.POST.get('furigana')
#         order.email = request.POST.get('email')
#         order.tel = request.POST.get('tel')
#         order.receipt = request.POST.get('receipt')
#         order.save()

#         # ログインユーザーのカートを削除
#         cart = Cart.objects.get(user=request.user)
#         cart.delete()

#         return redirect('order_thanks')


# class OrderConfirmView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         # ログインユーザーの注文内容をすべて取得
#         cart_data = Cart.objects.get(user=request.user)
#         # 注文合計金額を取得
#         get_total_price = Cart.objects.order_by("id").last().total_price

#         return render(request, 'app/order_confirm.html', {
#             'cart_data': cart_data,
#             'get_total_price': get_total_price,
#         })

#     def post(self, request, *args, **kwargs):
#         profile_form = ProfileForm(request.POST or None)
#         receipt_form = ReceiptForm(request.POST or None)

#         if profile_form.is_valid() and receipt_form.is_valid():
#             name = profile_form.cleaned_data['name']
#             furigana = profile_form.cleaned_data['furigana']
#             email = profile_form.cleaned_data['email']
#             tel = profile_form.cleaned_data['tel']
#             date = receipt_form.cleaned_data['date']
#             time = receipt_form.cleaned_data['time']

#             # 注文内容をすべて取得
#             cart_data = Cart.objects.all()
#             # 注文合計金額を取得
#             get_total_price = Cart.objects.order_by("id").last().total_price

#             return render(request, 'app/order_confirm.html', {
#                 'name': name,
#                 'furigana': furigana,
#                 'email': email,
#                 'tel': tel,
#                 'date': date,
#                 'time': time,
#                 'cart_data': cart_data,
#                 'get_total_price': get_total_price,
#             })

#         return render(request, 'app/order_user.html', {
#             'profile_form': profile_form,
#             'receipt_form': receipt_form,
#         })


# class OrderUserView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         # ログインユーザーと紐づける
#         user_data = CustomUser.objects.get(id=request.user.id)
#         profile_form = ProfileForm(
#             request.POST or None,
#             initial={
#                 'name': user_data.name,
#                 'furigana': user_data.furigana,
#                 'email': user_data.email,
#                 'tel': user_data.tel
#             }
#         )
#         receipt_form = ReceiptForm(request.POST or None)

#         return render(request, 'app/order_user.html', {
#             'profile_form': profile_form,
#             'receipt_form': receipt_form,
#         })


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        size_item = SizeItem.objects.all()
        flavor_item = FlavorItem.objects.filter(is_active=True)
        option_item = OptionItem.objects.all()

        return render(request, 'app/order.html', {
            'size_item': size_item,
            'flavor_item': flavor_item,
            'option_item': option_item,
        })


# class OrderView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         cart_data = Cart.objects.all()
#         # 最新の合計金額を取得。初期値は0
#         if cart_data.exists():
#             get_total_price = Cart.objects.order_by("id").last().total_price
#         else:
#             get_total_price = 0
        
#         # 最新レコードのidを取得
#         cart_id = Cart.objects.values_list('id', flat=True).last()

#         return render(request, 'app/order.html', {
#             'cart_data': cart_data,
#             'get_total_price': get_total_price,
#             'cart_id': cart_id,
#         })


# class AddOrderView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         size_title = request.POST.get('size_title')
#         size_price = request.POST.get('size_price')
#         flavor_title = request.POST.get('flavor_title')
#         flavor_title_2 = request.POST.get('flavor_title_2')
#         option_title = request.POST.get('option_title')
#         option_price = request.POST.get('option_price')
#         option_title_2 = request.POST.get('option_title_2')
#         option_price_2 = request.POST.get('option_price_2')
#         total_price = request.POST.get('total_price')

#         # 合計値のカンマを除いて整数値に変換
#         total_price = int(total_price.replace(',', ''))

#         cart = Cart()
#         cart.user = request.user
#         cart.size_title = size_title
#         cart.size_price = size_price
#         cart.flavor_title = flavor_title
#         cart.flavor_title_2 = flavor_title_2
#         cart.option_title = option_title
#         cart.option_price = option_price
#         cart.option_title_2 = option_title_2
#         cart.option_price_2 = option_price_2
#         cart.total_price = total_price
#         cart.save()

#         # 最新の合計金額を取得
#         # get_total_price = Cart.objects.order_by('id').last().total_price
#         get_total_price = Cart.objects.filter(user=request)[0].total_price
#         print(get_total_price)
#         # 最新レコードのidを取得
#         cart_id = Cart.objects.filter(user=request)[0].id
#         print(cart_id)
#         # cart_id = Cart.objects.values_list('id', flat=True).last()

#         data = {
#             'size_title': size_title,
#             'size_price': size_price,
#             'flavor_title': flavor_title,
#             'flavor_title_2': flavor_title_2,
#             'option_title': option_title,
#             'option_price': option_price,
#             'option_title_2': option_title_2,
#             'option_price_2': option_price_2,
#             'total_price': total_price,
#             'get_total_price': get_total_price,
#             'cart_id': cart_id,
#         }
#         return JsonResponse(data)


# class DeleteOrderView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         id_value = request.POST.get('id_value')

#         del_record = Cart.objects.filter(pk=id_value) # 削除するレコードを取得
#         size_price = del_record.values_list('size_price', flat=True)[0] # 削除するレコードのサイズ金額を取得
#         option_price = del_record.values_list('option_price', flat=True)[0]  # 削除するレコードのオプション金額を取得
#         option_price_2 = del_record.values_list('option_price_2', flat=True)[0] # 削除するレコードのオプション金額を取得
        
#         # 削除分の取得金額を整数値に変換。オプション指定が無い場合は0を設定
#         size_price = int(size_price[1:])
#         if option_price == '':
#             option_price = 0
#         else:
#             option_price = int(option_price[1:])
#         if option_price_2 == '':
#             option_price_2 = 0
#         else:
#             option_price_2 = int(option_price_2[1:])


#         # 最新レコードの合計値から削除分の金額を引いて更新
#         cart_latest = Cart.objects.filter(user=request)[0]
#         print(cart_latest)
#         print(cart_latest.total_price)
#         # cart_latest = Cart.objects.order_by("id").last()
#         # get_total_price = cart_latest.total_price
#         cart_latest.total_price = cart_latest.total_price - ( size_price + option_price + option_price_2 )
#         cart_latest.save()

#         # 指定レコードを削除
#         del_record.delete()

#         # 最新レコードの合計値を取得
#         get_total_price = cart_latest.total_price

#         data = {
#             'get_total_price': get_total_price,
#         }
#         return JsonResponse(data)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # item = Item.objects.all()

        return render(request, 'app/index.html', {
            # 'item': item
        })