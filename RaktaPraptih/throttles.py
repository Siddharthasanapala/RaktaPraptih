from rest_framework.throttling import UserRateThrottle

class DonorRequestRateThrottle(UserRateThrottle):
    scope="donorrequest"
