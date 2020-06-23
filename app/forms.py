from django import forms
# from .models import SIZE_CHOICES, FLAVOR_CHOICES, OPTION_CHOICES
# from .models import Size

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Size
#         widgets = {
#             'title': forms.RadioSelect()
#         }
#         fields = ('title',)

# class OrderForm(forms.Form):
#     size = forms.ChoiceField (
#         widget=forms.RadioSelect,
#         choices=SIZE_CHOICES,
#         required=True
#     )
#     flavor = forms.MultipleChoiceField (
#         widget=forms.CheckboxSelectMultiple,
#         choices=FLAVOR_CHOICES,
#         required=True
#     )
#     option = forms.MultipleChoiceField (
#         widget=forms.CheckboxSelectMultiple,
#         choices=OPTION_CHOICES,
#         required=False
#     )

    # name = forms.CharField (
    #     max_length=30,
    # )

    # email = forms.EmailField (
    #     max_length=30,
    # )

    # phone = forms.RegexField (
    #     regex = r'^0\d{2,3}-\d{1,4}-\d{4}$',
    #     error_messages = {'required': 'Phone number required'},
    #     widget = forms.TextInput,
    # )