from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('signup/confirm/', views.SignupConfirmView.as_view(), name='account_signup_confirm'),
    path('signup/temporary/', views.SignupDoneView.as_view(), name='account_signup_done'),
    path('signup/thanks/<token>/', views.SignupCompleteView.as_view(), name='account_signup_complete'),
    path('mypage/', views.ProfileView.as_view(), name='profile'),
    path('mypage/email_change/', views.EmailChangeView.as_view(), name='email_change'),
    path('mypage/email_change/send/', views.EmailChangeDoneView.as_view(), name='email_change_done'),
    path('mypage/email_change/done/<str:token>/', views.EmailChangeCompleteView.as_view(), name='email_change_complete'),
    path('mypage/password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('mypage/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('mypage/delete/confirm', views.DeleteConfirmView.as_view(), name='delete_confirm'),
    path('mypage/delete/done', views.DeleteCompleteView.as_view(), name='delete_complete'),
    path('mypage/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('login/password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('login/password-reset/send/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('login/password-reset/form/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/password-reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
]