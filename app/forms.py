from django import forms

class ImageSelect(forms.widgets.RadioSelect):
  template_name = 'widgets/size_radio.html'
  option_template_name = 'widgets/size_radio_option.html'

class SizeForm(forms.Form):
  size = forms.ChoiceField (
    choices = (
      ('mini', 'ミニサイズ'),
      ('single', 'シングルサイズ'),
      ('double', 'ダブルサイズ'),
    ),
    widget = ImageSelect, 
    required = True,
  )