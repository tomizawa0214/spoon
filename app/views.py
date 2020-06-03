from django.views.generic import ListView, DetailView, View
from .models import Item
from django.shortcuts import render
from accounts.models import CustomUser
from . import forms

class OrderView(View):
  def get(self, request):
    form = forms.OrderForm()
    context = {
      'form': form
    }
    return render(request, 'app/order.html', context)

  def post(self, request):
    form = forms.OrderForm()
    if form.is_valid():
      size = form.cleaned_data['size']
      flavor = form.cleaned_data['flavor']
      option = form.cleaned_data['option']
      return redirect('order')

    return render(request, 'app/thanks.html', {
      'form': form
    })

class ItemDetailView(DetailView):
  model = Item
  template_name = 'app/product_detail.html'

class IndexView(ListView):
  model = Item
  template_name = 'app/index.html'