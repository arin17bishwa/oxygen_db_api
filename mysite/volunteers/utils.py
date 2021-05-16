import six

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def send_conf_mail(request,email,*args,**kwargs):
    user=request.user
    current_site = get_current_site(request)
    mail_subject = 'Activate your Coupon_Reseller account.'
    message = render_to_string('volunteers/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    if not settings.DEBUG:
        email.send()
    else:
        print(message)


