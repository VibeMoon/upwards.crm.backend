from django.urls import reverse
from django.conf import settings


def get_full_url(name, request=None, **kwargs):
    relative_url = reverse(name, kwargs=kwargs)
    if request:
        return request.build_absolute_uri(relative_url)
    return f"{settings.SITE_URL}{relative_url}"


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Введите токен в формате: Bearer <ваш_токен>'
        },
    },
    'USE_SESSION_AUTH': False,
}
