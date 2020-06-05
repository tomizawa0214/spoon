from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import render, redirect
from .forms import OrderForm#テスト
from .models import Item
from django.conf import settings#テスト
from django.core.mail import BadHeaderError, EmailMessage#テスト
from django.http import HttpResponse#テスト
import textwrap#テスト

class OrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        return render(request, 'app/order.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        if form.is_valid():
            size = form.cleaned_data['size']
            flavor = form.cleaned_data['flavor']
            option = form.cleaned_data['option']
            return render(request, 'app/order_confirm.html', {
                'form': form
            })
            
class OrderConfirmView(View):
    def post(self, request, *args, **kwargs):
        size = form.cleaned_data['size']
        flavor = form.cleaned_data['flavor']
        option = form.cleaned_data['option']
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
        bcc_list = [settings.EMAIL_HOST_USER]

        try:
            # message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
            message = EmailMessage(subject=subject, body=content, bcc=bcc_list)
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