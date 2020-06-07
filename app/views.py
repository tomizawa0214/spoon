from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Item
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap

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
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        if form.is_valid():
            size = orders['size'][form.cleaned_data['size']]
            flavor = ','.join([orders['flavor'][key] for key in form.cleaned_data['flavor']])
            option = ','.join([orders['option'][key] for key in form.cleaned_data['option']])

        return render(request, 'app/order_confirm.html', {
            'size': size,
            'flavor': flavor,
            'option': option,
        })

class OrderSendView(View):
    def get(self, request, *args, **kwargs):
        size = self.kwargs['size']
        flavor = self.kwargs['flavor']
        option = self.kwargs['option']
        subject = 'ご注文ありがとうございます。'
        content = textwrap.dedent('''
            ■サイズ
            {size}
            
            ■フレーバー
            {flavor}
            
            ■オプション
            {option}
            --------------------
            ''').format(
                size=size,
                flavor=flavor,
                option=option
            )

        # to_list = [email]
        to_list = [settings.EMAIL_HOST_USER]

        try:
            # message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
            message = EmailMessage(subject=subject, body=content, to=to_list)
            message.send()
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

        return redirect('index')
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'app/product_detail.html'

class IndexView(ListView):
    model = Item
    template_name = 'app/index.html'