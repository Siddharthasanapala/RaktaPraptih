from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import date

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    email = models.EmailField(unique=True)
    is_blood_bank=models.BooleanField(default=False)
    is_donor=models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Donor(models.Model):
    groups = models.ManyToManyField(
        Group,
        related_name='donor_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='donor_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=5)
    phone_number=models.CharField(max_length=13)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=300)
    last_donation_date = models.DateField(default=date.today)    

class BloodBank(models.Model):
    groups = models.ManyToManyField(
        Group,
        related_name='bloodbank_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='bloodbank_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    govt_registration_id = models.CharField(max_length=20)
    owner_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=300)

class BloodBankBloods(models.Model):
    groups = models.ManyToManyField(
        Group,
        related_name='bloods_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='bloods_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    bloodbank = models.OneToOneField(BloodBank, on_delete=models.CASCADE, related_name='bloodbankbloods')
    a_positive = models.IntegerField(default=0)
    a_negative = models.IntegerField(default=0)
    b_positive = models.IntegerField(default=0)
    b_negative = models.IntegerField(default=0)
    o_positive = models.IntegerField(default=0)
    o_negative = models.IntegerField(default=0)
    ab_positive = models.IntegerField(default=0)
    ab_negative = models.IntegerField(default=0)