from django.shortcuts import render,get_object_or_404,redirect
from accounts.models import *
from .forms import DonorUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.decorators import api_view, throttle_classes
from RaktaPraptih.throttles import DonorRequestRateThrottle

import os
from twilio.rest import Client

@never_cache
@login_required
def donors_view(request):
    search_query = request.GET.get('q','')
    selected_place=request.GET.get('place','')
    donors=Donor.objects.all().select_related('user')
    for donor in donors:
        can_donate_after_date = donor.last_donation_date + timedelta(days=182)
        donor.is_eligible = can_donate_after_date <= timezone.now().date()
    if search_query:
        donors = donors.filter(
            Q(user__username__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    if selected_place:
        donors = donors.filter(address__icontains=selected_place)
    paginator = Paginator(donors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    unique_places = Donor.objects.values_list('address', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'unique_places': unique_places,
        'search_query': search_query,
        'selected_place': selected_place,
        'donors':donors,
    }
    return render(request, 'donors_page.html', context)
    
    
@never_cache
@login_required
def donor_details_view(request, donor_id):
    donor = get_object_or_404(Donor, id=donor_id)
    today = timezone.now().date()
    last_donation_date=donor.last_donation_date
    show_update = donor.user.is_authenticated and request.user == donor.user
    
    if request.method == 'POST':
        form = DonorUpdateForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Your details have been updated successfully!")
            
            if last_donation_date!=donor.last_donation_date:
                if last_donation_date+timedelta(days=182) > donor.last_donation_date:
                    messages.warning(request,"Ensure 6 months gap beyween your successive donations for your better health.")
                else:
                    can_donate_after_date=donor.last_donation_date+timedelta(days=182)
                    messages.success(request,"You can donate blood after "+str(can_donate_after_date))
                
            age = today.year - donor.date_of_birth.year - ((today.month, today.day) < (donor.date_of_birth.month, donor.date_of_birth.day))
            if age>60:
                messages.warning(request,"You crossed age 60 Take doctor's advice before you donate blood next time.")
            return redirect('donors_view')
    else:
        form = DonorUpdateForm(instance=donor)

    context = {
        'donor': donor,
        'show_update': show_update,
        'form': form,
    }
    return render(request, 'donor_details.html', context)

@never_cache
@login_required
@throttle_classes([DonorRequestRateThrottle])
def donor_request_view(request,donor_id):
    donor=get_object_or_404(Donor,id=donor_id)
    show_update=donor.user.is_authenticated and request.user!=donor.user
    form = DonorUpdateForm(instance=donor)
    fields=[('username','User Name'),('date_of_birth','Date of Birth'),('blood_type','Blood Group'),('gender','Gender'),('address','Address'),('last_donation_date','Last Donated Date')]
    if request.method == 'POST':
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        donor_phone_number="+91"+donor.phone_number
        receiver=get_object_or_404(CustomUser,email=request.user.email)
        if receiver.is_donor:
            receiver=get_object_or_404(Donor,user=receiver)
        else:
            receiver=get_object_or_404(BloodBank,user=receiver)
        receiver_phone_number="+91"+receiver.phone_number
        body="Hello "+donor.user.username+" this is a message from Rakta-Praptih "+request.user.username+" is requesting you to Donate blood if possible. Please contact to +91"+receiver_phone_number+" for more details. Thankyou!"
        # message = client.messages.create(
        #     body=body,
        #     from_=os.environ["SENDER_PHONE_NUMBER"],
        #     to=donor_phone_number,
        # )       
        if donor.last_donation_date+timedelta(days=182) > timezone.now().date():
            messages.info(request, f"{donor.user.username} hasen't completed 6 months from his last donation but request is sent.")
        else:
            messages.success(request, "Your blood request has been sent successfully.")
        return redirect('donors_view') 
    context={
        'donor':donor,
        'show_update':show_update,
        'fields':fields,
        'form':form
    }
    return render(request,'donor_request.html',context)