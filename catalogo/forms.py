from django import forms

from .models import LugarPatrimonial


class LugarForm(forms.ModelForm):
    class Meta:
        model = LugarPatrimonial
        fields = "__all__"
