from rest_framework import serializers

from accounts.utils import create_jwt_pair_for_user
from .models import CustomUser , Donor , BloodBank , BloodBankBloods
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

class DonorSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = Donor
        fields = ['username', 'email', 'password1', 'password2','date_of_birth','blood_type','phone_number','gender','address','last_donation_date']
    
    def validate(self,attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords must match.")

        email_exixting=CustomUser.objects.filter(email=attrs["email"]).exists()
        if email_exixting:
            raise ValidationError("Email has already registered. Please login with your crediantails or use another mail to register")
        username_exists=CustomUser.objects.filter(username=attrs["username"]).exists()
        if username_exists:
            raise ValidationError("Username already exists Please use different one")
        return super().validate(attrs)
    
    def create(self,validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        date_of_birth=validated_data.pop('date_of_birth')
        blood_type=validated_data.pop('blood_type')
        phone_number=validated_data.pop('phone_number')
        gender=validated_data.pop('gender')
        address=validated_data.pop('address')
        last_donation_date=validated_data.pop('last_donation_date')
        user = CustomUser(username=username, email=email, is_donor=True)
        user.set_password(password)
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
    
    def to_representation(self, instance):
        data = {
            "username": instance.user.username,
            "email": instance.user.email,
            "tokens": create_jwt_pair_for_user(instance.user)
        }
        return data
    
class BloodBnakSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    user = CustomUser
    class Meta:
        model = Donor
        fields = ['username', 'email', 'password1', 'password2','govt_registration_id','owner_name','phone_number','address']
    
    def validate(self,attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords must match.")

        email_exixting=CustomUser.objects.filter(email=attrs["email"]).exists()
        if email_exixting:
            raise ValidationError("Email has already registered. Please login with your crediantails or use another mail to register")
        username_exists=CustomUser.objects.filter(username=attrs["username"]).exists()
        if username_exists:
            raise ValidationError("Username already exists Please use different one")
        return super().validate(attrs)
    
    def create(self,validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        

        govt_registration_id=validated_data.pop('govt_registration_id')
        owner_name=validated_data.pop('owner_name')
        phone_number=validated_data.pop('phone_number')
        address=validated_data.pop('address')
        
        user = CustomUser(username=username, email=email, is_blood_bank=True)
        user.set_password(password)
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
    def to_representation(self, instance):
        data = {
            "username": instance.user.username,
            "email": instance.user.email,
            "tokens": create_jwt_pair_for_user(instance.user)
        }
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
   