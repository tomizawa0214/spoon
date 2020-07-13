from django.urls import path
from accounts import views

urlpatterns = [
    path('profile/cart_none', views.CartNoneView.as_view(), name='cart_none'),
    path('delete/confirm', views.DeleteConfirmView.as_view(), name='delete_confirm'),
    path('delete/complete', views.DeleteCompleteView.as_view(), name='delete_complete'),
    path('email_change/', views.EmailChangeView.as_view(), name='email_change'),
    path('email_change/done/', views.EmailChangeDoneView.as_view(), name='email_change_done'),
    path('email_change/complete/<str:token>/', views.EmailChangeCompleteView.as_view(), name='email_change_complete'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('signup/complete/<token>/', views.SignupCompleteView.as_view(), name='account_signup_complete'),
    path('signup/done/', views.SignupDoneView.as_view(), name='account_signup_done'),
    path('signup/confirm/', views.SignupConfirmView.as_view(), name='account_signup_confirm'),
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]