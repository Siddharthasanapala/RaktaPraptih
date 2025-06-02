from itertools import count
from django.shortcuts import render, redirect,get_object_or_404
from .forms import LoginForm, DonorSignupForm, BloodBankSignupForm ,BloodBankForm
from django.contrib.auth import authenticate, login,logout
from rest_framework.permissions import AllowAny
from rest_framework import generics,status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .serializers import DonorSignupSerializer, BloodBnakSignupSerializer
from .utils import create_jwt_pair_for_user
from .forms import DonorSignupForm, BloodBankSignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import random
from sentry_sdk import capture_message
import logging

User = get_user_model()

@method_decorator(never_cache, name='dispatch')
class DonorSignupView(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    serializer_class=DonorSignupSerializer
    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            
            user=serializer.save()
            tokens=create_jwt_pair_for_user(user)
            response={
                "message":"Donor Signup Successful",
                "tokens": tokens,
                "data": serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@method_decorator(never_cache, name='dispatch')
class BloodBankSignupView(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    serializer_class=BloodBnakSignupSerializer
    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            user=serializer.save()
            tokens=create_jwt_pair_for_user(user)
            response={
                "message":"BloodBank Signup Successful",
                "tokens": tokens,
                "data": serializer.data,
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
@method_decorator(never_cache, name='dispatch')
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            tokens = create_jwt_pair_for_user(user)
            request.session['username'] = user.username   
            response = {
                "message": "Login successful",
                "tokens": tokens,
                "username": user.username
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@never_cache
@login_required
def home_view(request):
    search_query = request.GET.get('q', '')
    selected_place = request.GET.get('place', '')

    bloodbanks = BloodBank.objects.all().select_related('user').prefetch_related('bloodbankbloods').order_by('owner_name')
    if search_query:
        bloodbanks = bloodbanks.filter(
            Q(owner_name__icontains=search_query) |
            Q(address__icontains=search_query)
            )
    if selected_place:
        bloodbanks = bloodbanks.filter(address__icontains=selected_place)

    paginator = Paginator(bloodbanks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    unique_places = BloodBank.objects.values_list('address', flat=True).distinct()
    blood_fields = [
        'a_positive', 'a_negative', 
        'b_positive', 'b_negative', 
        'o_positive', 'o_negative', 
        'ab_positive', 'ab_negative'
    ]
    context = {
        'page_obj': page_obj,
        'unique_places': unique_places,
        'search_query': search_query,
        'selected_place': selected_place,
        'blood_fields': blood_fields,  
    }
    logger.info(f"User {request.user.username} accessed Homepage")
    return render(request, 'homepage.html', context)

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                tokens = create_jwt_pair_for_user(user)
                login(request, user)
                request.session['username'] = user.username
                response = redirect('home')
                response.set_cookie('access_token', tokens['access'], httponly=True)
                response.set_cookie('refresh_token', tokens['refresh'], httponly=True)
                logger.info(f"User {user.username} Login Successful")
                return response
            else:
                messages.error(request,"Entered wrong Crediantails please try again.")
                logger.error(f"User Entered Wrong Crediantails to signin", exc_info=True)

    else:
        logger.error(f"Login Form Entries are invalid", exc_info=True)
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@never_cache
def donor_signup_view(request):
    if request.method == 'POST':
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_donor = True
            user.save()

            donor = Donor(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                blood_type=form.cleaned_data['blood_type'],
                phone_number=form.cleaned_data['phone_number'],
                gender=form.cleaned_data['gender'],
                address=form.cleaned_data['address'],
                last_donation_date=form.cleaned_data['last_donation_date']
            )
            donor.save()

            tokens = create_jwt_pair_for_user(user)
            messages.success(request, "You have succeessfully registered as Donor.")
            logger.info(f"Donor {user.username} Signup Successful")
            login(request, user)
            request.session['username'] = user.username

            response = redirect('home')
            response.set_cookie('access_token', tokens['access'], httponly=True)
            response.set_cookie('refresh_token', tokens['refresh'], httponly=True)
            return response

    else:
        form = DonorSignupForm()
    return render(request, 'donorsignup.html', {'form': form})

@never_cache
def bloodbank_signup_view(request):
    if request.method == 'POST':
        form = BloodBankSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_blood_bank = True
            user.save()

            blood_bank = BloodBank(
                user=user,
                govt_registration_id=form.cleaned_data['govt_registration_id'],
                owner_name=form.cleaned_data['owner_name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            blood_bank.save()

            blood_bank_bloods = BloodBankBloods(
                bloodbank=blood_bank,
                a_positive=0,
                a_negative=0,
                b_positive=0,
                b_negative=0,
                o_positive=0,
                o_negative=0,
                ab_positive=0,
                ab_negative=0
            )
            blood_bank_bloods.save()
            messages.success(request, "You have succeessfully registered in our Portal.")
            messages.info(request,"Update Blood units available in your Blood Bank from your account")
            logger.info(f"BloodBank {user.username} Signup Successful")
            login(request, user)
            request.session['username'] = user.username

            return redirect('home')
    else:
        form = BloodBankSignupForm()
    return render(request, 'bloodbanksignup.html', {'form': form})

@never_cache
@login_required
def bloodbank_detail_view(request, pk):
    bloodbank = get_object_or_404(BloodBank, id=pk)
    bloods = bloodbank.bloodbankbloods  
    show_update = request.user.is_authenticated and request.user == bloodbank.user  
    form = BloodBankForm(instance=bloods)
    blood_groups = [
        ('a_positive', 'A+'),
        ('a_negative', 'A-'),
        ('b_positive', 'B+'),
        ('b_negative', 'B-'),
        ('o_positive', 'O+'),
        ('o_negative', 'O-'),
        ('ab_positive', 'AB+'),
        ('ab_negative', 'AB-'),
    ]
    context = {
        'bloodbank': bloodbank,
        'bloods': bloods,
        'show_update': show_update,
        'form': form,
        'blood_groups': blood_groups,
    }
    logger.info(f"User {request.user.username} interacted with blood bank {bloodbank.user.username}")
    return render(request, 'bloodbank_details.html', context)

@never_cache
@login_required
def bloodbank_update_view(request, bloodbank_id):
    bloodbank = get_object_or_404(BloodBank, id=bloodbank_id)
    bloods = bloodbank.bloodbankbloods
    if request.method == 'POST':
        form = BloodBankForm(request.POST, instance=bloods)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Blood Units are updated successfully.")
            logger.info(f"User {request.user.username} updated BloodBank Blood Levels successfully")
            return redirect('bloodbank_detail', pk=bloodbank_id)
        else:
            return redirect('bloodbank_detail', pk=bloodbank_id)
    else:
        form = BloodBankForm(instance=bloods)
    blood_groups = [
        ('a_positive', 'A+'),
        ('a_negative', 'A-'),
        ('b_positive', 'B+'),
        ('b_negative', 'B-'),
        ('o_positive', 'O+'),
        ('o_negative', 'O-'),
        ('ab_positive', 'AB+'),
        ('ab_negative', 'AB-'),
    ]
    context = {
        'bloodbank': bloodbank,
        'bloods': bloods,
        'show_update': True,
        'form': form,
        'blood_groups': blood_groups,
    }
    messages.success(request, "Blood units are successfully updated.")
    messages.info(request,"Please keep updating available blood units for users")
    return render(request, 'bloodbank_details.html', context)

@never_cache
@login_required
def logout_view(request):
    logout(request)

    request.session.flush()

    response = redirect('login')  

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    logger.info(f"User {request.user.username} Logged out")
    return response

@never_cache
def landing_view(request):
    six_months_ago = timezone.now() - timedelta(days=6*30) 
    donors_count=Donor.objects.all().select_related('user').count()
    active_donors_count=Donor.objects.filter(last_donation_date__lt=six_months_ago).select_related('user').count()
    bloodbanks_count=BloodBank.objects.all().select_related('user').count()
    print(donors_count,bloodbanks_count,active_donors_count)
    context={
        'donors_count':donors_count,
        'bloodbanks_count':bloodbanks_count,
        'active_donors_count':active_donors_count
    }
    logger.info(f"A User interacted with landing page")
    return render(request, 'landingpage.html',context)