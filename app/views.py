from django.views.generic import View
from django.shortcuts import render, redirect
# from .forms import OrderForm
from .models import Cart, Size, Flavor, Option, Item
# from django.conf import settings
# from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse, HttpResponse
# import textwrap

class OrderView(View):
    def get(self, request, *args, **kwargs):
        cart_data = Cart.objects.all()
        # 最新の合計金額を取得。初期値は0
        if Cart.objects.count() == 0:
            get_total_price = 0
        else:
            get_total_price = Cart.objects.order_by("id").last().total_price

        return render(request, 'app/order.html', {
            'cart_data': cart_data,
            'get_total_price': get_total_price,
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

        # 最新の合計金額を取得。初期値は0
        if Cart.objects.count() == 0:
            get_total_price = 0
        else:
            get_total_price = Cart.objects.order_by("id").last().total_price

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
        }
        return JsonResponse(data)



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