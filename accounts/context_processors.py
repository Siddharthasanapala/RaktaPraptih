from .models import Donor, BloodBank

def user_profile_context(request):
    context = {}
    if request.user.is_authenticated:
        try:
            if request.user.is_donor:
                context['donor_id'] = Donor.objects.get(user=request.user).id
            elif request.user.is_blood_bank:
                context['bloodbank_id'] = BloodBank.objects.get(user=request.user).id
        except (Donor.DoesNotExist, BloodBank.DoesNotExist):
            pass
    return context
