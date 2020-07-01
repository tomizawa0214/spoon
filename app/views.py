from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import OrderUserForm
from .models import Cart, Size, Flavor, Option, Item
# from django.conf import settings
# from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
# import textwrap

class OrderView(View):
    def get(self, request, *args, **kwargs):
        cart_data = Cart.objects.all()
        # 最新の合計金額を取得。初期値は0
        if cart_data.exists():
            get_total_price = Cart.objects.order_by("id").last().total_price
        else:
            get_total_price = 0
        
        # 最新レコードのidを取得
        cart_id = Cart.objects.values_list('id', flat=True).last()

        return render(request, 'app/order.html', {
            'cart_data': cart_data,
            'get_total_price': get_total_price,
            'cart_id': cart_id,
        })

class AddOrderView(View):
    def post(self, request, *args, **kwargs):
        size_title = request.POST.get('size_title')
        size_price = request.POST.get('size_price')
        flavor_title = request.POST.get('flavor_title')
        flavor_title_2 = request.POST.get('flavor_title_2')
        option_title = request.POST.get('option_title')
        option_price = request.POST.get('option_price')
        option_title_2 = request.POST.get('option_title_2')
        option_price_2 = request.POST.get('option_price_2')
        total_price = request.POST.get('total_price')

        # 合計値のカンマを除いて整数値に変換
        total_price = int(total_price.replace(',', ''))

        cart = Cart()
        cart.size_title = size_title
        cart.size_price = size_price
        cart.flavor_title = flavor_title
        cart.flavor_title_2 = flavor_title_2
        cart.option_title = option_title
        cart.option_price = option_price
        cart.option_title_2 = option_title_2
        cart.option_price_2 = option_price_2
        cart.total_price = total_price
        cart.save()

        # 最新の合計金額を取得
        get_total_price = Cart.objects.order_by('id').last().total_price
        # 最新レコードのidを取得
        cart_id = Cart.objects.values_list('id', flat=True).last()

        data = {
            'size_title': size_title,
            'size_price': size_price,
            'flavor_title': flavor_title,
            'flavor_title_2': flavor_title_2,
            'option_title': option_title,
            'option_price': option_price,
            'option_title_2': option_title_2,
            'option_price_2': option_price_2,
            'total_price': total_price,
            'get_total_price': get_total_price,
            'cart_id': cart_id,
        }
        return JsonResponse(data)


class DeleteOrderView(View):
    def post(self, request, *args, **kwargs):
        id_value = request.POST.get('id_value')

        del_record = Cart.objects.filter(pk=id_value) # 削除するレコードを取得
        size_price = del_record.values_list('size_price', flat=True)[0] # 削除するレコードのサイズ金額を取得
        option_price = del_record.values_list('option_price', flat=True)[0]  # 削除するレコードのオプション金額を取得
        option_price_2 = del_record.values_list('option_price_2', flat=True)[0] # 削除するレコードのオプション金額を取得
        
        # 削除分の取得金額を整数値に変換。オプション指定が無い場合は0を設定
        size_price = int(size_price[1:])
        if option_price == '':
            option_price = 0
        else:
            option_price = int(option_price[1:])
        if option_price_2 == '':
            option_price_2 = 0
        else:
            option_price_2 = int(option_price_2[1:])


        # 最新レコードの合計値から削除分の金額を引いて更新
        cart_latest = Cart.objects.order_by("id").last()
        get_total_price = cart_latest.total_price
        cart_latest.total_price = cart_latest.total_price - ( size_price + option_price + option_price_2 )
        cart_latest.save()

        # 指定レコードを削除
        del_record.delete()

        # 最新レコードの合計値を取得
        get_total_price = cart_latest.total_price

        data = {
            'get_total_price': get_total_price,
        }
        return JsonResponse(data)


class OrderUserView(View):
    def get(self, request, *args, **kwargs):
        form = OrderUserForm(request.POST or None)

        return render(request, 'app/order_user.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = OrderUserForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            datetime = form.cleaned_data['datetime']

            return redirect('order_confirm')

        return render(request, 'app/order_user.html', {
            'form': form
        })


# class OrderView(View):
#     def get(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)

#         return render(request, 'app/order.html', {
#             'form': form
#         })

#     def post(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)

#         if form.is_valid():
#             size = form.cleaned_data['size']
#             # flavor = "・".join(form.cleaned_data['flavor'])
#             # option = "・".join(form.cleaned_data['option'])
#             return render(request, 'app/order_confirm.html', {
#                 'size': size,
#                 # 'flavor': flavor,
#                 # 'option': option,
#             })

#         return render(request, 'app/order.html', {
#             'form': form
#         })

class OrderConfirmView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/order_confirm.html', {
            # 'size': size,
            # 'flavor': flavor,
            # 'option': option,
        })

class OrderThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/order_thanks.html')

# orders = { 'size':{ '1':'ミニサイズ', '2':'シングルサイズ', '3':'ダブルサイズ' },
#             'flavor':{ '1':'バニラ', '2':'オレンジ', '3':'マンゴー' },
#             'option':{ '1':'コーン' }
#             }

# class OrderView(View):
#     def get(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)

#         return render(request, 'app/order.html', {
#             'form': form
#         })
    
#     def post(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)

#         return render(request, 'app/order_confirm.html', {
#             'form': form
#         })
            
# class OrderConfirmView(View):
#     def post(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)

#         if form.is_valid():
#             size = orders['size'][form.cleaned_data['size']]
#             flavor = ','.join([orders['flavor'][key] for key in form.cleaned_data['flavor']])
#             option = ','.join([orders['option'][key] for key in form.cleaned_data['option']])
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             phone = form.cleaned_data['phone']

#         return render(request, 'app/order_confirm.html', {
#             'size': size,
#             'flavor': flavor,
#             'option': option,
#             'name': name,
#             'email': email,
#             'phone': phone,
#         })

# class OrderSendView(View):
#     def get(self, request, *args, **kwargs):
#         size = self.kwargs['size']
#         flavor = self.kwargs['flavor']
#         option = self.kwargs['option']
#         name = self.kwargs['name']
#         email = self.kwargs['email']
#         phone = self.kwargs['phone']
#         # name = self.request['name']
#         # email = self.request['email']
#         # phone = self.request['phone']
#         subject = 'ご注文ありがとうございます。'
#         content = textwrap.dedent('''
#             ※このメールはシステムからの自動返信です。
            
#             {name} 様
            
#             ご注文ありがとうございます。
#             以下の内容で受け付けいたしました。
#             店頭にてお待ちしております。
            
#             --------------------
#             ■お名前
#             {name}様

#             ■メールアドレス
#             {email}

#             ■電話番号
#             {phone}

#             ■サイズ
#             {size}
            
#             ■フレーバー
#             {flavor}
            
#             ■オプション
#             {option}
#             --------------------
#             ''').format(
#                 size=size,
#                 flavor=flavor,
#                 option=option,
#                 name=name,
#                 email=email,
#                 phone=phone,
#             )

#         to_list = [email]
#         bcc_list = [settings.EMAIL_HOST_USER]

#         try:
#             message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
#             message.send()
#         except BadHeaderError:
#             return HttpResponse("無効なヘッダが検出されました。")

#         return redirect('order_thanks')
    
# class ItemDetailView(DetailView):
#     model = Item
#     template_name = 'app/product_detail.html'

class IndexView(View):
    def get(self, request, *args, **kwargs):
        item = Item.objects.all()

        return render(request, 'app/index.html', {
            'item': item
        })