from django.urls import path
from app import views

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('product_detail/<slug>', views.ItemDetailView.as_view(), name='product_detail'),
  # path('order/', views.OrderView.as_view(), name='order'),
  path('order/', views.OrderView.as_view(), name='order'),
]