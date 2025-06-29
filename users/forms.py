from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """Base registration form for all user types"""
    profile_picture = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture',
                  'address_line1', 'city', 'state', 'pincode', 'password1', 'password2']
    
    def clean_first_name(self):
        """Validate first name is not empty"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError("First name is required.")
        return first_name
    
    def clean_last_name(self):
        """Validate last name is not empty"""
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError("Last name is required.")
        return last_name
    
    def clean_email(self):
        """Validate email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def clean_pincode(self):
        """Validate pincode format"""
        pincode = self.cleaned_data.get('pincode')
        if pincode:
            if not re.match(r'^\d{6}$', pincode):
                raise ValidationError("Pincode must be 6 digits.")
        return pincode
        
    def clean(self):
        """Ensure password validation"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')
        
        # Additional password strength validation
        if password1:
            # Check for at least 8 characters
            if len(password1) < 8:
                self.add_error('password1', 'Password must be at least 8 characters long')
            
            # Check for at least one uppercase, one lowercase, and one digit
            if not any(char.isupper() for char in password1):
                self.add_error('password1', 'Password must contain at least one uppercase letter')
            
            if not any(char.islower() for char in password1):
                self.add_error('password1', 'Password must contain at least one lowercase letter')
            
            if not any(char.isdigit() for char in password1):
                self.add_error('password1', 'Password must contain at least one digit')
            
        return cleaned_data


class PatientRegistrationForm(UserRegistrationForm):
    """Form for patient registration"""
    
    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'patient'
        if commit:
            user.save()
        return user


class DoctorRegistrationForm(UserRegistrationForm):
    """Form for doctor registration"""
    
    class Meta(UserRegistrationForm.Meta):
        model = User
        fields = UserRegistrationForm.Meta.fields
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        if commit:
            user.save()
        return user 