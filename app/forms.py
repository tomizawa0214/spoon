from django import forms

class OrderForm(forms.Form):
    name = forms.ChoiceField (
      choices = (
        ('mini', 'ミニサイズ'),
        ('single', 'シングルサイズ'),
        ('double', 'ダブルサイズ'),
      ),
      widget = forms.RadioSelect,
    )
    email = forms.EmailField(max_length=30, label='メールアドレス')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea())

# class OrderForm(forms.Form):
#   size = forms.ChoiceField (
#     choices = (
#       ('mini', 'ミニサイズ'),
#       ('single', 'シングルサイズ'),
#       ('double', 'ダブルサイズ'),
#     ),
#     widget = forms.RadioSelect, 
#     required = True,
#   )

#   flavor = forms.MultipleChoiceField (
#     choices = (
#       ('vanilla', 'バニラ'),
#       ('orange', 'オレンジ'),
#       ('mango', 'マンゴー'),
#     ),
#     widget = forms.CheckboxSelectMultiple,
#     required = True,
#   )

#   option = forms.MultipleChoiceField (
#     choices = (
#       ('corn', 'コーン'),
#     ),
#     widget = forms.CheckboxSelectMultiple,
#     required = False,
#   )