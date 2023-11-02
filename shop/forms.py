from django import forms
from .models import Shop

class ShopProfielForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = (
        'shop_name',
        'email',
        'bank_name',
        'branch_name',
        'account_number',
        'account_holder_name',
        )
