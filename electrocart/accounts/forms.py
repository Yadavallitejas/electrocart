from django import forms
from .models import account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={
            'placeholder': 'Password',
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
                               attrs={
            'placeholder': 'Confirm Password',
        }
    ))

    class Meta:
        model = account
        fields = ['first_name', 'last_name','phone_number', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'First Name',
        })
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'

            
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
           
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match"
            )
        return cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists. Please use a different phone number.")
        return phone_number
        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")