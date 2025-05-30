from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('bloodbanks/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.landing_view, name='landingpage'),
    path('signup/donor/', views.donor_signup_view, name='donor_signup'),
    path('signup/bloodbank/', views.bloodbank_signup_view, name='bloodbank_signup'),
    # JWT endpoints for API usage
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('bloodbank/<int:bloodbank_id>/', views.bloodbank_detail_view, name='bloodbank_detail'),
    # path('bloodbank/update/<int:bloodbank_id>/', views.bloodbank_update_view, name='bloodbank_update'),
    path('bloodbank/<int:pk>/', views.bloodbank_detail_view, name='bloodbank_detail'),
    path('bloodbank/update/<int:bloodbank_id>/', views.bloodbank_update_view, name='bloodbank_update'),
]