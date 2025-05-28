from django.contrib import admin
from .models import Donor, BloodBank, BloodBankBloods ,CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display=['username','email','password']
   
admin.site.register(CustomUser,CustomUserAdmin)


class DonorUserAdmin(admin.ModelAdmin):
    list_display=['date_of_birth','blood_type','phone_number','gender','address']

admin.site.register(Donor,DonorUserAdmin)

class BloodBankAdmin(admin.ModelAdmin):
    list_display=['govt_registration_id','owner_name','phone_number','address']
   
admin.site.register(BloodBank,BloodBankAdmin)

class BloodBankBloodsAdmin(admin.ModelAdmin):
    list_display=['a_positive','a_negative','b_positive','b_negative','o_positive','o_negative','ab_positive','ab_negative']

admin.site.register(BloodBankBloods,BloodBankBloodsAdmin)

