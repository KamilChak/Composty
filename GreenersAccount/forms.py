from django import forms
from .models import Greener
import re

class GreenerForm(forms.ModelForm):
    class Meta:
        model = Greener
        fields = ('FirstName', 'LastName', 'Email', 'password', 'PhoneNumber', 'Location', 'composter')
        widgets = {
            'FirstName': forms.TextInput(attrs={'class': 'form-control', 'id': 'first-name'}),
            'LastName': forms.TextInput(attrs={'class': 'form-control', 'id': 'last-name'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}),
            'PhoneNumber': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone-number'}),
            'Location': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'location'}),
            'composter': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'composter'})
        }

        labels = {
            'FirstName': 'First name',
            'LastName': 'Last name',
            'Email': 'Email',
            'Password': 'password',
            'PhoneNumber': 'Phone number',
            'Location': 'Location',
            'composter': 'composter',
        }

    def clean_FirstName(self):
        first_name = self.cleaned_data.get('FirstName')
        if not re.match(r'^[a-zA-Z]{2,}$', first_name):
            raise forms.ValidationError("First name must contain at least 2 letters and cannot contain any special character.")
        return first_name
        
    def clean_LastName(self):
        last_name = self.cleaned_data.get('LastName')
        if not re.match(r'^[a-zA-Z]{2,}$', last_name):
            raise forms.ValidationError("Last name must contain at least 2 letters and cannot contain any special character.")
        return last_name
    
    def clean_PhoneNumber(self):
        phone_number = self.cleaned_data.get('PhoneNumber')
        if not re.match(r'^(2\d{7}|3\d{7}|5\d{7}|7\d{7}|9\d{7})$', phone_number):
            raise forms.ValidationError("Phone number is invalid")
        return phone_number
    

class GreenerLoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Password'}))
    


class CompostOfferForm(forms.Form):
    manure = forms.FloatField(label="Animal Manure", required=True,widget=forms.TextInput(attrs={'class': 'form-control quantities', 'aria-label': 'Sizing example input', 'aria-describedby': 'inputGroup-sizing-lg'}))
    green_material = forms.FloatField(label="Green Material", required=True,widget=forms.TextInput(attrs={'class': 'form-control quantities', 'aria-label': 'Sizing example input', 'aria-describedby': 'inputGroup-sizing-lg'}))
    brown_material = forms.FloatField(label="Brown Material", required=True,widget=forms.TextInput(attrs={'class': 'form-control quantities', 'aria-label': 'Sizing example input', 'aria-describedby': 'inputGroup-sizing-lg'}))
    date_range = forms.CharField(label="Date Range", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Select Date Range'}))

