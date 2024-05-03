from django import forms
#review
class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required= False, initial=False, widget=forms.HiddenInput)
    
    