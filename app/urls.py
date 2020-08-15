from django.urls import path
from app import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('concept/', views.AboutView.as_view(), name='about'),
    path('order-guide/', views.OrderGuideView.as_view(), name='order_guide'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('addorder/', views.AddOrderView.as_view(), name='add_order'),
    path('deleteorder/', views.DeleteOrderView.as_view(), name='delete_order'),
    path('order/user/', views.OrderUserView.as_view(), name='order_user'),
    path('order/confirm/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('order/thanks/', views.OrderThanksView.as_view(), name='order_thanks'),
    path('access/', views.AccessView.as_view(), name='access'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/thanks', views.ContactThanksView.as_view(), name='contact_thanks'),
    path('sctl/', views.SctlView.as_view(), name='sctl'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('company/', views.CompanyView.as_view(), name='company'),
]