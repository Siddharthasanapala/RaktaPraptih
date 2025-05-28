from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Donor
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta



class DonorUpdateForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['date_of_birth', 'blood_type', 'phone_number', 'gender', 'address', 'last_donation_date']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'blood_type': forms.Select(choices=[
                ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')
            ]),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('date_of_birth')
        last_donation_date = cleaned_data.get('last_donation_date')
        today = timezone.now().date()

        if dob:
            if dob > today:
                self.add_error('date_of_birth', "Date of birth cannot be in the future.")
            else:
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 18:
                    self.add_error('date_of_birth', "Not eligible: age must be at least 18.")
            
        if last_donation_date:
            if last_donation_date > today:
                self.add_error('last_donation_date', "Last donation date cannot be in the future.")
        

        return cleaned_data