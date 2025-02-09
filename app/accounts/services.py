from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.text import slugify

from deep_translator import GoogleTranslator

class GetLoginResponseService:
    @staticmethod
    def get_login_response(user, request):
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return data
    
class AccountsService:
    @staticmethod
    def add_slug(title):
        translated = GoogleTranslator(source='auto', target='en').translate(title)

        slug = slugify(translated)

        return slug