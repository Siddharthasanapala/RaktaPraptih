import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from accounts.models import Donor
import uuid

@pytest.mark.django_db
class TestAuthAndViews:
    def setup_method(self):
        self.client = Client()
        self.user_data = {
            "username": f"testuser_{uuid.uuid4().hex[:8]}",
            "email": f"testuser_{uuid.uuid4().hex[:8]}@gmail.com",
            "password": "SecurePass123!",
            "date_of_birth": "2000-01-01",
            "blood_type": "B+",
            "phone_number": "9258648276",
            "gender": "Male",
            "address": "HYD",
            "last_donation_date": "2020-10-10",
        }
        self.tokens=None

    def test_donor_signup_form_get(self):
        """Test that the signup form renders correctly on GET request."""
        response = self.client.get(reverse('donor_signup'), follow=True)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert 'form' in response.context, "Form not in response context"
        assert 'donorsignup.html' in [t.name for t in response.templates], "Correct template not used"

    def test_homepage_view_unauthenticated(self):
        """Test that the homepage is accessible to unauthenticated users."""
        response = self.client.get(reverse('home'), follow=True)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_homepage_view_authenticated(self):
        """Test that the homepage is accessible to authenticated users."""
        User = get_user_model()
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password'],
            is_donor=True
        )
        Donor.objects.create(
            user=user,
            date_of_birth=self.user_data['date_of_birth'],
            blood_type=self.user_data['blood_type'],
            phone_number=self.user_data['phone_number'],
            gender=self.user_data['gender'],
            address=self.user_data['address'],
            last_donation_date=self.user_data['last_donation_date']
        )
        self.tokens=self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        assert f'{self.tokens}'
        response = self.client.get(reverse('home'), follow=True)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.wsgi_request.user.is_authenticated, "User is not authenticated"