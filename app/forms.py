from django import forms

class OrderForm(forms.Form):
    size = forms.ChoiceField (
        choices = (
            ('1', 'ミニサイズ'),
            ('2', 'シングルサイズ'),
            ('3', 'ダブルサイズ'),
        ),
        widget = forms.RadioSelect,
    )

    flavor = forms.MultipleChoiceField (
        choices = (
            ('1', 'バニラ'),
            ('2', 'オレンジ'),
            ('3', 'マンゴー'),
        ),
        widget = forms.CheckboxSelectMultiple,
    )

    option = forms.MultipleChoiceField (
        choices = (
            ('1', 'コーン'),
        ),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    name = forms.CharField (
        max_length=30,
    )

    email = forms.EmailField (
        max_length=30,
    )

    phone = forms.RegexField (
        regex = r'^0\d{2,3}-\d{1,4}-\d{4}$',
        error_messages = {'required': 'Phone number required'},
        widget = forms.TextInput,
    )