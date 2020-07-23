from django import forms
from allauth.account.forms import SignupForm
from .models import GENDER_CHOICES
from django.contrib.auth import get_user_model
import datetime
User = get_user_model()


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class SignupUserForm(SignupForm):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')
    gender = forms.ChoiceField(
        widget=forms.Select,
        choices=GENDER_CHOICES + (('', '---'),),
        required=False,
        label='性別'
    )
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(
            years=list(reversed([y for y in range(datetime.datetime.now().year - 100, datetime.datetime.now().year)])),
            months={1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12},
        ),
        required=False,
        label='誕生日'
    )


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')
    gender = forms.ChoiceField(
        widget=forms.Select,
        choices=GENDER_CHOICES + (('', '---'),),
        required=False,
        label='性別'
    )
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(
            years=list(reversed([y for y in range(datetime.datetime.now().year - 100, datetime.datetime.now().year)])),
            months={1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12},
        ),
        required=False,
        label='誕生日'
    )