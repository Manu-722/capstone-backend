from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class NoSignupAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # ✅ Auto-create user during Google login without asking for extra info
        return True