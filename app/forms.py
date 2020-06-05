from django import forms

class OrderForm(forms.Form):
    size = forms.ChoiceField (
        choices = (
            ('ミニサイズ', 'ミニサイズ'),
            ('シングルサイズ', 'シングルサイズ'),
            ('ダブルサイズ', 'ダブルサイズ'),
        ),
        widget = forms.RadioSelect,
    )

    flavor = forms.MultipleChoiceField (
        choices = (
            ('バニラ', 'バニラ'),
            ('オレンジ', 'オレンジ'),
            ('マンゴー', 'マンゴー'),
        ),
        widget = forms.CheckboxSelectMultiple,
    )

    option = forms.MultipleChoiceField (
        choices = (
            ('コーン', 'コーン'),
        ),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )