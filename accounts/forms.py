from django import forms
from allauth.account.forms import SignupForm
import datetime

class SignupUserForm(SignupForm):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(
            ('1', '女性'),
            ('2', '男性'),
        ),
        required=False,
        label='性別'
    )
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(
            years=[y for y in range(datetime.datetime.now().year - 100, datetime.datetime.now().year)],
            months={1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12},
        ),
        required=False,
        label='誕生日'
    )
    # def save(self, request):
    #     user = super(SignupUserForm, self).save(request)
    #     user.name = self.cleaned_data['name']
    #     user.furigana = self.cleaned_data['furigana']
    #     user.tel = self.cleaned_data['tel']
    #     user.gender = self.cleaned_data['gender']
    #     user.birthday = self.cleaned_data['birthday']
    #     user.save()
    #     return user


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')