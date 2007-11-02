from westom import settings

def default(request):
    """
    Returns some default context variables
    """
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'URL_HOST': settings.URL_HOST,
    }