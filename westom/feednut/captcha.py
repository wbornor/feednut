from django.core.exceptions import ObjectDoesNotExist, ViewDoesNotExist
from westom.settings import SITE_ID
from django.core import urlresolvers
from django.http import Http404, HttpResponse, HttpResponseRedirect

from Captcha.Visual import Tests
import Captcha
import tempfile

def _getFactory( id ):
    return Captcha.PersistentFactory(tempfile.gettempdir() + "/pycaptcha_%d" % id )

def image( request ):
    """
    Generate the image to show users with the magic word embedded inside
    """
    if request.GET:
        id = request.GET["id"]
        test = _getFactory(SITE_ID).get(id)
        if test is not None:
            response =  HttpResponse(mimetype="image/jpeg")
            test.render().save(response, "JPEG")
            return response

    raise Http404("not found")

def verify( request, forward_to, *arguments, **keywords):
    """
    verify the captcha and then forward the request 
    TBD: redirect to the original form with a validation error
    """

    captcha_error = []

    if request.POST:
        id = request.POST["captcha_id"]
        word = request.POST["captcha_word"]
        test = _getFactory(SITE_ID).get(id)
        if not test:
            captcha_error.append('Invalid captcha id.')
        if not test.valid:
            captcha_error.append('Test invalidated, try again.')
        elif not test.testSolutions([word]):
            captcha_error.append('Invalid word.')

    mod_name, func_name = urlresolvers.get_mod_func(forward_to)

    try:
        func, ignore = getattr(__import__(mod_name, '', '', ['']), func_name), {}
        return func(request, captcha_error, *arguments, **keywords)
    except (ImportError, AttributeError), e:
        raise ViewDoesNotExist, "Tried %s. Error was: %s" % (forward_to, str(e))

def verify_anon( request, forward_to, *arguments, **keywords):
    """
    verify the captcha and then forward the request  for anonymous users only
    TBD: redirect to the original form with a validation error
    """

    captcha_error = []

    if request.POST and request.user.is_authenticated():
        id = request.POST["captcha_id"]
        word = request.POST["captcha_word"]
        test = _getFactory(SITE_ID).get(id)
        if not test:
            captcha_error.append('Invalid captcha id.')
        if not test.valid:
            captcha_error.append('Test invalidated, try again.')
        elif not test.testSolutions([word]):
            captcha_error.append('Invalid word.')

    mod_name, func_name = urlresolvers.get_mod_func(forward_to)

    try:
        func, ignore = getattr(__import__(mod_name, '', '', ['']), func_name), {}
        return func( request, captcha_error, *arguments, **keywords) 

    except (ImportError, AttributeError), e:
        raise ViewDoesNotExist, "Tried %s. Error was: %s" % (forward_to, str(e))


