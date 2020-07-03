from django import forms
from allauth.account.forms import SignupForm


GENDER_CHOICES = (
    ('1', '女性'),
    ('2', '男性'),
)
class SignupUserForm(SignupForm):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, required=False, label='性別')
    birthday = forms.DateField(input_formats=['%Y/%m/%d'], required=False, label='誕生日')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.furigana = self.cleaned_data['furigana']
        user.tel = self.cleaned_data['tel']
        user.gender = self.cleaned_data['gender']
        user.birthday = self.cleaned_data['birthday']
        user.save()
        return user


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')