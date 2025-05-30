from rest_framework import viewsets
from .models import Donor , BloodBank
from .serializers import DonorSerializer, BloodBankSerializer
from .permissions import IsDonor , IsBloodBank
from rest_framework.permissions import IsAuthenticated

class BloodBankViewSet(viewsets.ModelViewSet):
    queryset = BloodBank.objects.all()
    serializer_class = BloodBankSerializer
    permission_classes = [IsAuthenticated, IsBloodBank]

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsDonor]
