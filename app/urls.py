from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('addorder/', views.AddOrderView.as_view(), name='add_order'),
    # path('regiorder/', views.RegiOrderView.as_view(), name='regi_order'),
    path('deleteorder/', views.DeleteOrderView.as_view(), name='delete_order'),
    path('orderer/', views.OrdererView.as_view(), name='orderer'),
    path('order/confirm/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('order/thanks/', views.OrderThanksView.as_view(), name='order_thanks'),
]