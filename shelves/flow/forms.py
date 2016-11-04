from flow.models import CpPhoneFlowProduct
from django import forms



class CpPhoneFlowProductForm(forms.ModelForm):

    class Meta:
        model = CpPhoneFlowProduct
        fields = '__all__'