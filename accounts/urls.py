from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/complete/<token>/', views.SignupCompleteView.as_view(), name='account_signup_complete'),
    path('signup/done/', views.SignupDoneView.as_view(), name='account_signup_done'),
    path('signup/confirm/', views.SignupConfirmView.as_view(), name='account_signup_confirm'),
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('login/', views.LoginView.as_view(), name='account_login'),
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]