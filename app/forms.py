from django import forms

class SizeForm(forms.Form):
  size = forms.ChoiceField (
    choices = (
      ('mini', 'ミニサイズ'),
      ('single', 'シングルサイズ'),
      ('double', 'ダブルサイズ'),
    ),
    widget = forms.RadioSelect, 
    required = True,
  )