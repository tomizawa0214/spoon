from django import forms
from django.utils import timezone
from datetime import datetime, date, timedelta, time

# default = timezone.datetime.now + timedelta(days=1)
class OrderUserForm(forms.Form):
    name = forms.CharField(max_length=30, label='お名前')
    email = forms.EmailField(min_length=7, max_length=256, label='メールアドレス')
    phone = forms.CharField(min_length=10, max_length=13, label='電話番号')
    receipt = forms.DateTimeField(
        label='受取希望日時',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'value': timezone.datetime.now().strftime('%Y-%m-%dT%H:%M')}),
        # widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'value': default.strftime('%Y-%m-%dT%H:%M')}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    # def default():
    #     return timezone.datetime.now + timezone.timedelta(days=1)

    # def clean_receipt(self):
    #     receipt = self.cleaned_data.get('receipt')
    #     if receipt
    #     return receipt