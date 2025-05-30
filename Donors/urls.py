from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('request/<int:donor_id>/', views.donor_request_view, name='request_donor'),
    path('', views.donors_view, name='donors_view'),
    path('<int:donor_id>/', views.donor_details_view, name='donor_details'),
]