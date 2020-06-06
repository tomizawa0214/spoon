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