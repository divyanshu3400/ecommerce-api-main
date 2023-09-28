from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from ecommerce_app.models import OTPToken

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, otp=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            otp_token = OTPToken.objects.filter(user=user, token=otp).order_by('-created_at').first()

        except User.DoesNotExist:
            return None

        if password is not None and user.check_password(password):
            return user
        
        if otp is not None and otp_token is not None and str(otp) == otp_token.token:
            return user

        # Return None if neither password nor OTP authentication is successful
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
