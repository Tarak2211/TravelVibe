from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return username.lower().replace(' ', '.') if username else username

    def validate_unique(self):
        # Skip model-level unique validation — handled manually in the view
        pass

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'passport_number', 'passport_expiry', 'address', 'aadhar_number']
        widgets = {
            'passport_expiry': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=6, required=True)
