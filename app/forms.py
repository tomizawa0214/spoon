from django import forms
from django.utils import timezone


class OrderUserForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    phone = forms.CharField(min_length=10, max_length=11, label='電話番号')
    datetime = forms.DateTimeField(
        label='受取希望日時',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'value': timezone.datetime.now().strftime('%Y-%m-%dT%H:%M')}),
        input_formats=['%Y-%m-%dT%H:%M']
    )