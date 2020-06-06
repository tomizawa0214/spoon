from django.urls import path
from app import views

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('product_detail/<slug>/', views.ItemDetailView.as_view(), name='product_detail'),
  path('order/', views.OrderView.as_view(), name='order'),
  path('order_confirm/', views.OrderConfirmView.as_view(), name='order_confirm'),
  path('order_send/<size>/<flavor>/<option>/', views.OrderSendView.as_view(), name='order_send'),
  # path('order_send/', views.OrderSendView.as_view(), name='order_send'),
]