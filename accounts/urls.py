from django.urls import path
from accounts import views

urlpatterns = [
    path('account-signup/', views.SignupView.as_view(), name='account_signup'),
    path('account-signup/confirm/', views.SignupConfirmView.as_view(), name='account_signup_confirm'),
    path('account-signup/temporary/', views.SignupDoneView.as_view(), name='account_signup_done'),
    path('account-signup/thanks/<token>/', views.SignupCompleteView.as_view(), name='account_signup_complete'),
    path('account-mypage/', views.ProfileView.as_view(), name='profile'),
    path('account-mypage/email_change/', views.EmailChangeView.as_view(), name='email_change'),
    path('account-mypage/email_change/send/', views.EmailChangeDoneView.as_view(), name='email_change_done'),
    path('account-mypage/email_change/done/<str:token>/', views.EmailChangeCompleteView.as_view(), name='email_change_complete'),
    path('account-mypage/password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('account-mypage/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('account-mypage/delete/confirm', views.DeleteConfirmView.as_view(), name='delete_confirm'),
    path('account-mypage/delete/done', views.DeleteCompleteView.as_view(), name='delete_complete'),
    path('account-mypage/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('account-login/', views.LoginView.as_view(), name='account_login'),
    path('account-login/password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('account-login/password-reset/send/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account-login/password-reset/form/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account-login/password-reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('account-logout/', views.LogoutView.as_view(), name='account_logout'),
]