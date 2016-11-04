
from django import forms

from phone_fee.models import CpPhoneFeeProduct


class CpPhoneFeeProductForm(forms.ModelForm):

    class Meta:
        model = CpPhoneFeeProduct
        fields = '__all__'