from django import forms
from django.contrib.auth import get_user_model
from .models import Donor, BloodBank, BloodBankBloods 

User = get_user_model()

class DonorSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)
    
    date_of_birth=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    blood_type=forms.CharField(max_length=10)
    phone_number=forms.CharField(max_length=13) 
    gender=forms.CharField(max_length=10)
    address=forms.CharField(widget=forms.Textarea)
    last_donation_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    def clean(self):
        cleaned_data=super().clean()
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Passwords must match. Entered Passeords didn't matched")
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.Login to your account or create account with new email")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.Use different username to proceed")
        return cleaned_data
    
    def save(self, commit=True):
        cleaned = self.cleaned_data
        username = cleaned['username']
        email = cleaned['email']
        password = cleaned['password1']
        date_of_birth = cleaned['date_of_birth']
        blood_type = cleaned['blood_type']
        phone_number = cleaned['phone_number']
        gender = cleaned['gender']
        address = cleaned['address']
        last_donation_date=cleaned['last_donation_date']
        
        user = User(username=username, email=email, is_donor=True)
        user.set_password(password)
        if commit:
            user.save()
            Donor.objects.create(
                user=user,
                date_of_birth=date_of_birth,
                blood_type=blood_type,
                phone_number=phone_number,
                gender=gender,
                address=address,
                last_donation_date=last_donation_date
            )
        return user
    
    

class BloodBankSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)
    
    govt_registration_id=forms.CharField(max_length=20)
    owner_name=forms.CharField(max_length=100) 
    phone_number=forms.CharField(max_length=13)
    address=forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Passwords must match.Entered Passeords didn't matched")
        
        email = cleaned_data.get('email') 
        username = cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.Login to your account or create account with new email")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.Use different username to proceed")
        return cleaned_data
    
    def save(self, commit=True):
        cleaned = self.cleaned_data
        username = cleaned['username']
        email = cleaned['email']
        password = cleaned['password1']
        govt_registration_id = cleaned['govt_registration_id']
        owner_name = cleaned['owner_name']
        phone_number = cleaned['phone_number']
        address = cleaned['address']
        
        user = User(username=username, email=email, is_blood_bank=True)
        user.set_password(password)
        if commit:
            user.save()
            bloodbank=BloodBank.objects.create(
                user=user,
                govt_registration_id=govt_registration_id,
                owner_name=owner_name,
                phone_number=phone_number,
                address=address
            )
            
            BloodBankBloods.objects.create(
                bloodbank=bloodbank,
                a_positive = 0,
                a_negative = 0,
                b_positive = 0,
                b_negative = 0,
                o_positive = 0,
                o_negative = 0,
                ab_positive = 0,
                ab_negative = 0
            )
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class BloodBankForm(forms.ModelForm):
    class Meta:
        model = BloodBankBloods
        fields = ['a_positive', 'a_negative', 'b_positive', 'b_negative', 'o_positive', 'o_negative', 'ab_positive', 'ab_negative']
        widgets = {
            'a_positive': forms.NumberInput(attrs={'class': 'blood-input'}),
            'a_negative': forms.NumberInput(attrs={'class': 'blood-input'}),
            'b_positive': forms.NumberInput(attrs={'class': 'blood-input'}),
            'b_negative': forms.NumberInput(attrs={'class': 'blood-input'}),
            'o_positive': forms.NumberInput(attrs={'class': 'blood-input'}),
            'o_negative': forms.NumberInput(attrs={'class': 'blood-input'}),
            'ab_positive': forms.NumberInput(attrs={'class': 'blood-input'}),
            'ab_negative': forms.NumberInput(attrs={'class': 'blood-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        blood_fields = ['a_positive', 'a_negative', 'b_positive', 'b_negative', 'o_positive', 'o_negative', 'ab_positive', 'ab_negative']
        for field in blood_fields:
            value = cleaned_data.get(field)
            if value < 0:
                raise forms.ValidationError(field, "Blood quantity cannot be negative.")
        return cleaned_data