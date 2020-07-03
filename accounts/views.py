from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from accounts.forms import ProfileForm, SignupUserForm
from django.shortcuts import render, redirect
from allauth.account import views


class SignupConfirmView(views):
    def post(self, request, *args, **kwargs):
        form = SignupUserForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            furigana = form.cleaned_data['furigana']
            tel = form.cleaned_data['tel']
            gender = form.cleaned_data['gender']
            birthday = form.cleaned_data['birthday']
            # return redirect('account_signup_confirm')
            return render(request, 'accounts/signup_confirm.html', {
                'name': name,
                'furigana': furigana,
                'tel': tel,
                'gender': gender,
                'birthday': birthday,
            })

        return render(request, 'accounts/signup.html', {
            'form': form,
        })


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm

    # def post(self, request, *args, **kwargs):
    #     form = SignupUserForm(request.POST or None)

    #     if form.is_valid():
    #         name = form.cleaned_data['name']
    #         # furigana = form.cleaned_data['furigana']
    #         # tel = form.cleaned_data['tel']
    #         # gender = form.cleaned_data['gender']
    #         # birthday = form.cleaned_data['birthday']
    #         # return redirect('account_signup_confirm')
    #         return render(request, 'accounts/signup_confirm.html', {
    #             'name': name,
    #             # 'furigana': furigana,
    #             # 'tel': tel,
    #             # 'gender': gender,
    #             # 'birthday': birthday,
    #         })

    #     return render(request, 'accounts/signup.html', {
    #         'form': form,
    #     })


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