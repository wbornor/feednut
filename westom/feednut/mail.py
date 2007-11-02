from django.core.mail import send_mail


def send_welcome_email(user):
    """ sends an email to the user welcoming them to FeedNut """
    
    subject = 'Welcome to FeedNut'
    message = """Thanks for signing up for a free account at www.feednut.com!

Now you can quickly organize and read the news YOU want to read by subscribing to news feeds that interest you!
At account creation, we signed you up for some of the top feeds on FeedNut, just to get you started. Feel free to unsubscribe from them if you wish.

Since FeedNut is a community system, you can also see what other people are reading, share articles with friends, and link into several other social sites, such as www.del.icio.us and www.reddit.com.

Have fun staying on top of the news!

Your username: %s
Your homepage: http://www.feednut.com/%s/

Thanks again!
The FeedNut Team
(Tom and Wes)""" % (user.username, user.username)
    
    return send_mail(subject, message, None, [user.email], fail_silently=False)



def send_suggested_link(from_user, to_email, url, title=None, message=None):
    """ the from_user wants to send a link/article to an email """

    subject = 'FeedNut.com link%s' % (title and ': %s' % title or '')
    message = """A user at www.feednut.com (%s), saw this link and thought you might like it:

%s



After reading the article, check out www.feednut.com for yourself! FeedNut is FREE to use, and lets you stay on top of the news you want to read!

- or -

Check out %s's FeedNut homepage at www.feednut.com/%s/


The FeedNut Team
(Tom and Wes)""" % (from_user.username, url, from_user.username, from_user.username)
    
    return send_mail(subject, message, None, [to_email], fail_silently=False)



def send_password_reset(email, hash):
    """ an email to let users reset their password """

    subject = 'FeedNut.com Password Reset Request'
    message = """Oh No! You forgot your password! It's ok though. We know you've got a lot on your mind.

Please visit the URL below in order to reset your password.

http://www.feednut.com/login/reset/?id=%s


The FeedNut Team
(Tom and Wes)""" % (hash,)
    
    return send_mail(subject, message, None, [email], fail_silently=False)
