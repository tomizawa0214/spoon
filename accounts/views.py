from django.views import View
from accounts.forms import ProfileForm, SignupUserForm, EmailChangeForm
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from app.models import Cart, Order
from allauth.account import views
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, send_mail, EmailMessage
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
User = get_user_model()


class DeleteCompleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        subject = render_to_string('accounts/mail_template/delete_subject.txt', {'user': user})
        message = render_to_string('accounts/mail_template/delete_message.txt', {'user': user})

        try:
            send_mail(subject, message, None, [user.email])
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

        # ログインしている現在のユーザーを削除
        user.delete()

        return render(request, 'accounts/delete_complete.html')


class DeleteConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/delete_confirm.html')


class EmailChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EmailChangeForm(request.POST or None)

        return render(request, 'accounts/email_change.html', {
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = EmailChangeForm(request.POST or None)

        if form.is_valid():
            user = self.request.user
            new_email = form.cleaned_data['email']
            
            # current_site = get_current_site(self.request)
            # domain = current_site.domain
            domain = '127.0.0.1:8000'
            context = {
                'protocol': 'https' if self.request.is_secure() else 'http',
                'domain': domain,
                'token': dumps(new_email),
                'user': user,
            }

            subject = render_to_string('accounts/mail_template/email_change_subject.txt', context)
            message = render_to_string('accounts/mail_template/email_change_message.txt', context)

            try:
                send_mail(subject, message, None, [new_email])
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")
            
            return redirect('email_change_done')
        
        return render(request, 'accounts/email_change.html', {
            'form': form,
        })


class EmailChangeDoneView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/email_change_done.html')


class EmailChangeCompleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # メール内URLアクセス後のユーザー本登録 60*60*24=1分×60×24=一日
        timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
        # tokenが正しければ本登録
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=timeout_seconds)

        # 期限切れの場合
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている場合
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題ない場合
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
        
        return render(request, 'accounts/email_change_complete.html')

class PasswordResetView(PasswordResetView):
    subject_template_name = 'accounts/mail_template/password_reset_subject.txt'
    email_template_name = 'accounts/mail_template/password_reset_message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class SignupCompleteView(View):
    def get(self, request, *args, **kwargs):
        # メール内URLアクセス後のユーザー本登録 60*60*24=1分×60×24=一日
        timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
        # tokenが正しければ本登録
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=timeout_seconds)

        # 期限切れの場合
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている場合
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題ない場合
        else:
            try:
                user = User.objects.get(pk=user_pk)
            # ユーザーが存在しない場合
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録
                    user.is_active = True
                    user.save()
        
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

        user.set_password(request.POST.get('password'))
        user.is_active = False
        user.save()
        
        # current_site = get_current_site(self.request)
        # domain = current_site.domain
        domain = '127.0.0.1:8000'
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('accounts/mail_template/signup_subject.txt', context)
        message = render_to_string('accounts/mail_template/signup_message.txt', context)

        try:
            user.email_user(subject, message)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

        return redirect('account_signup_done')


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm

    def post(self, request, *args, **kwargs):
        form = SignupUserForm(request.POST or None)

        # 同じメールアドレスで仮登録段階のアカウントは削除（本登録忘れや入力間違いに対応）
        email = form.data['email']
        User.objects.filter(email=email, is_active=False).delete()

        if form.is_valid():
            name = form.cleaned_data['name']
            furigana = form.cleaned_data['furigana']
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
        order_data = Order.objects.filter(user=request.user)

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'order_data': order_data,
        })

    def post(self, request, *args, **kwargs):
        id_value = request.POST.get('id_value')

        # 再注文のオーダーを取得
        same_order = Order.objects.filter(user=request.user, pk=id_value)

        # 再注文のオーダーからカートを登録
        for order in same_order:
            for same_cart in order.cart.all():
                cart = Cart()
                cart.user = request.user
                cart.size_title = same_cart.size_title
                cart.size_price = same_cart.size_price
                cart.flavor_title = same_cart.flavor_title
                cart.flavor_price = same_cart.flavor_price
                cart.flavor2_title = same_cart.flavor2_title
                cart.flavor2_price = same_cart.flavor2_price
                cart.option_title = same_cart.option_title
                cart.option_price = same_cart.option_price
                cart.option2_title = same_cart.option2_title
                cart.option2_price = same_cart.option2_price
                cart.option3_title = same_cart.option3_title
                cart.option3_price = same_cart.option3_price
                cart.save()

        return redirect('order_user')