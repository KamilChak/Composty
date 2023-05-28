from django import forms
from .models import Composter
import re

class ComposterForm(forms.ModelForm):
    class Meta:
        model = Composter
        fields = ('OrganizationName', 'CommunityName', 'Email', 'password', 'PhoneNumber', 'Location')
        widgets = {
            'OrganizationName': forms.TextInput(attrs={'class': 'form-control', 'id': 'organization-name'}),
            'CommunityName': forms.TextInput(attrs={'class': 'form-control', 'id': 'community-name'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}),
            'PhoneNumber': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone-number'}),
            'Location': forms.HiddenInput(attrs={'class': 'form-control', 'id': 'location'}),
        }

        labels = {
            'OrganizationName': 'Organization name',
            'CommunityName': 'Community name',
            'Email': 'Email',
            'password': 'Password',
            'PhoneNumber': 'Phone number',
            'Location': 'Location',
        }

    def clean_OrganizationName(self):
        organization_name = self.cleaned_data.get('OrganizationName')
        if not re.match(r'^[a-zA-Z\s]+$', organization_name):
            raise forms.ValidationError("Organization name must contain only letters and cannot be less than 2 letters")
        return organization_name

    def clean_CommunityName(self):
        community_name = self.cleaned_data.get('CommunityName')
        if not re.match(r'^[a-zA-Z\s]+$', community_name):
            raise forms.ValidationError("Community name must contain only letters cannot be less than 2 letters")
        return community_name
    
    def clean_PhoneNumber(self):
        phone_number = self.cleaned_data.get('PhoneNumber')
        if not re.match(r'^(2\d{7}|3\d{7}|5\d{7}|7\d{7}|9\d{7})$', phone_number):
            raise forms.ValidationError("Phone number is invalid")
        return phone_number
    
class ComposterLoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Password'}))