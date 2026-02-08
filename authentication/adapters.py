# authentication/adapters.py (or wherever your User model lives)
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # Extract username from email prefix (kvinay21505@gmail.com → kvinay21505)
        if user.email:
            proposed_username = user.email.split('@')[0]  # Gets email prefix
            
            # Make unique if needed (add numbers)
            base_username = proposed_username[:30]  # Django username max length
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exclude(pk=user.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user.username = username
        
        return user
    

    
    


    
