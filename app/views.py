from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import render, redirect
from .forms import OrderForm#テスト
from .models import Item
from django.conf import settings#テスト
from django.core.mail import BadHeaderError, EmailMessage#テスト
from django.http import HttpResponse#テスト
import textwrap#テスト
# from accounts.models import CustomUser
from django.urls import reverse_lazy
# from . import forms

class OrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        return render(request, 'app/order.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)

        if form.is_valid():
            ctx = {'form': form}
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            if self.request.POST.get('next', '') == 'confirm':
                return render(self.request, 'app/order_confirm.html', ctx)
            if self.request.POST.get('next', '') == 'back':
                return render(self.request, 'app/order.html', ctx)
            if self.request.POST.get('next', '') == 'create':
                return super().form_valid(form)
            else:
                return redirect(reverse_lazy('index'))

# class OrderConfirmView(CreateView):
#     def post(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)

#         if form.is_valid():
#             name = dict(form.fields['name'].choices)[name]
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
#             subject = 'お問い合わせありがとうございます。'
#             content = textwrap.dedent('''
#                 ※このメールはシステムからの自動返信です。
                
#                 {name} 様
                
#                 お問い合わせありがとうございました。
#                 以下の内容でお問い合わせを受け付けいたしました。
#                 内容を確認させていただき、ご返信させて頂きますので、少々お待ちください。
                
#                 --------------------
#                 ■お名前
#                 {name}
                
#                 ■メールアドレス
#                 {email}
                
#                 ■メッセージ
#                 {message}
#                 --------------------
#                 ''').format(
#                     name=name,
#                     email=email,
#                     message=message
#                 )

#             to_list = [email]
#             bcc_list = [settings.EMAIL_HOST_USER]

#             try:
#                 message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
#                 message.send()
#             except BadHeaderError:
#                 return HttpResponse("無効なヘッダが検出されました。")

#             return redirect('index')

#         return render(request, 'app/order.html', {
#             'form': form
#         })

# class OrderView(CreateView):
#   template_name = 'app/order.html'
#   success_url = reverse_lazy('index')

#   def get(self, request, *args, **kwargs):
#     form = forms.OrderForm(request.POST or None)

#     return render(request, 'app/order.html', {
#       'form': form
#     })

  # def post(self, request, *args, **kwargs):
  #   form = forms.OrderForm(request.POST or None)

    # if form.is_valid():
    #   size = form.cleaned_data['size']
    #   flavor = form.cleaned_data['flavor']
    #   option = form.cleaned_data['option']
    #   return redirect(reverse_lazy('index'))
    # else:
    #   return render(request, 'app/order.html', {
    #   'form': form
    #   })

  # def form_valid(self, form):
  #   ctx = {'form': form}
  #   if self.request.POST.get('next', '') == 'confirm':
  #     return render(self.request, 'app/order_confirm.html', ctx)
  #   if self.request.POST.get('next', '') == 'back':
  #     return render(self.request, 'app/order.html', ctx)
  #   if self.request.POST.get('next', '') == 'create':
  #     return super().form_valid(form)
  #   else:
  #     return redirect(reverse_lazy('index'))
    
class ItemDetailView(DetailView):
  model = Item
  template_name = 'app/product_detail.html'

class IndexView(ListView):
  model = Item
  template_name = 'app/index.html'