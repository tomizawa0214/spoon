from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ReceiptForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    furigana = forms.CharField(max_length=30, label='フリガナ')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    tel = forms.CharField(min_length=10, max_length=13, label='電話番号')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea())
    captcha = ReCaptchaField(widget=ReCaptchaV3)