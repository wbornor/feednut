from django import template
from westom.settings import SITE_ID
import Captcha
from Captcha.Visual import Tests
import tempfile

def _getFactory(id):
    return Captcha.PersistentFactory(tempfile.gettempdir() + "/pycaptcha_%d" % id )

class captcha_class(template.Node):
    """ generate a captcha image and specify the related input box parameters.

    Basically you have the following context variables:
        captcha_image: the url to the captcha image
        captcha_input_name: the input box name to submit the captcha word
        captcha_hidden_input_name: the hidden input box name to submit the captcha id
        captcha_id: captcha id, for the hidden input box's content
    You will need to submit both the captcha word and the captcha id
    in your form for validation. Sample code:
        <div id='captcha'>
            {% trans "Please enter the word you see in the picture" %}
            <input type="text" name="{{captcha_input_name}}"/>
            <input type="hidden" name="{{captcha_hidden_input_name}}"
                value="{{captcha_id}}"/><input type="submit" name="submit" value="{%
                trans 'submit' %}" /><br />
            <img src={{captcha_image}} width=150 height=60 />
        </div>
     """
    def __init__(self, anon_users_only):
        self.anon_users_only = anon_users_only
    def render(self, context):
        if self.anon_users_only:
            user = context.get('user', None)
            if not user.is_authenticated():
                return ""
        name = Tests.__all__[0]
        test = _getFactory(SITE_ID).new(getattr(Tests, name))

        context['captcha_image'] = '/captcha/i/?id=%s' % test.id
        context['captcha_input_name'] = "captcha_word"
        context['captcha_hidden_input_name'] = "captcha_id"
        context['captcha_id'] = test.id
        return '' 

def captcha(parser, token):
    """
    {% captcha %} 
    """
    return captcha_class(False)

def captcha_anon(parser, token):
    """
    {% captcha_anon %} 
    """
    return captcha_class(True)


register = template.Library()
register.tag('captcha', captcha)
register.tag('captcha_anon', captcha_anon)
