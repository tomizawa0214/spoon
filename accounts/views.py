from django.views import View
# from accounts.models import CustomUser
from accounts.forms import ProfileForm, SignupUserForm
from django.shortcuts import render, redirect
from allauth.account import views

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.views import (
#     LoginView, LogoutView
# )
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
# from django.views import generic


User = get_user_model()


class SignupCompleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/signup_complete.html')


class SignupDoneView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/signup_done.html')


class SignupConfirmView(View):
    def post(self, request, *args, **kwargs):
        user = User()
        user.name = request.POST.get('name')
        user.furigana = request.POST.get('furigana')
        user.email = request.POST.get('email')
        user.tel = request.POST.get('tel')
        user.gender = request.POST.get('gender')

        if request.POST.get('birthday') == 'None':
            user.birthday = None
        else:
            user.birthday = request.POST.get('birthday')
            
        user.password = request.POST.get('password')
        user.is_active = False
        user.save()
        
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('accounts/mail_template/create_subject.txt', context)
        message = render_to_string('accounts/mail_template/create_message.txt', context)

        user.email_user(subject, message)
        return redirect('account_signup_done')


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm

    def post(self, request, *args, **kwargs):
        form = SignupUserForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            furigana = form.cleaned_data['furigana']
            email = form.cleaned_data['email']
            tel = form.cleaned_data['tel']
            gender = form.cleaned_data['gender']
            birthday = form.cleaned_data['birthday']
            password = form.cleaned_data['password1']

            return render(request, 'accounts/signup_confirm.html', {
                'name': name,
                'furigana': furigana,
                'email': email,
                'tel': tel,
                'gender': gender,
                'birthday': birthday,
                'password': password,
            })

        return render(request, 'accounts/signup.html', {
            'form': form,
        })


class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'name': user_data.name,
                'furigana': user_data.furigana,
                'email': user_data.email,
                'tel': user_data.tel
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'user_data': user_data,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.name = form.cleaned_data['name']
            user_data.furigana = form.cleaned_data['furigana']
            user_data.email = form.cleaned_data['email']
            user_data.tel = form.cleaned_data['tel']
            user_data.save()
            return redirect('profile')

        return render(request, 'accounts/profile_edit.html', {
            'form': form,
        })


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })