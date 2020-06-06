from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import render, redirect
from .forms import OrderForm#テスト
from .models import Item
from django.conf import settings#テスト
from django.core.mail import BadHeaderError, EmailMessage#テスト
from django.http import HttpResponse#テスト
import textwrap#テスト

orders = { 'size':{ '1':'ミニサイズ', '2':'シングルサイズ', '3':'ダブルサイズ' },
            'flavor':{ '1':'バニラ', '2':'オレンジ', '3':'マンゴー' },
            'option':{ '1':'コーン' }
            }

class OrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        return render(request, 'app/order.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        return render(request, 'app/order_confirm.html', {
            'form': form
        })
            
class OrderConfirmView(View):
    # def get(self, request, *args, **kwargs):

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        if form.is_valid():
            # size = form.cleaned_data['size']
            size = orders['size'][form.cleaned_data['size']]
            # flavor = form.cleaned_data['flavor']
            flavor = ','.join([orders['flavor'][key] for key in form.cleaned_data['flavor']])
            # option = form.cleaned_data['option']
            option = ','.join([orders['option'][key] for key in form.cleaned_data['option']])

            size_url = '1'
            flavor_url = '2,3,4'
            option_url = '0'

        return render(request, 'app/order_confirm.html', {
            'size': size,
            'flavor': flavor,
            'option': option,
            'size_url': size_url,
            'flavor_url': flavor_url,
            'option_url': option_url
        })

class OrderSendView(View):
    def get(self, request, *args, **kwargs):
        size = self.kwargs['size']
        flavor = self.kwargs['flavor']
        option = self.kwargs['option']
        print(size)
        print(flavor)
        print(option)
        # size = form.cleaned_data['size']
        # flavor = form.cleaned_data['flavor']
        # option = form.cleaned_data['option']
        # subject = 'ご注文ありがとうございます。'
        # content = textwrap.dedent('''
        #     ■サイズ
        #     {size}
            
        #     ■フレーバー
        #     {flavor}
            
        #     ■オプション
        #     {option}
        #     --------------------
        #     ''').format(
        #         size=1,
        #         flavor='test',
        #         option='test'
        #     )

        # # to_list = [email]
        # bcc_list = [settings.EMAIL_HOST_USER]

        # try:
        #     # message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
        #     message = EmailMessage(subject=subject, body=content, bcc=bcc_list)
        #     message.send()
        # except BadHeaderError:
        #     return HttpResponse("無効なヘッダが検出されました。")

        return redirect('index')
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'app/product_detail.html'

class IndexView(ListView):
    model = Item
    template_name = 'app/index.html'