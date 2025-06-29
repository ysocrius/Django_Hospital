from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Additional fields - made optional to handle superusers
    address_line1 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, validators=[
        RegexValidator(
            regex=r'^\d{6}$',
            message='Pincode must be 6 digits',
            code='invalid_pincode'
        )
    ], blank=True, null=True)
    
    def __str__(self):
        user_type_display = self.get_user_type_display() if self.user_type else "No Type"
        return f"{self.username} ({user_type_display})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def is_patient(self):
        return self.user_type == 'patient'
    
    def is_doctor(self):
        return self.user_type == 'doctor'


class Address(models.Model):
    """Additional model for structured address storage"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='detailed_address')
    line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    
    def __str__(self):
        return f"{self.line1}, {self.city}, {self.state} - {self.pincode}"
