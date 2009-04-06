VERSION = (0, 1, 0, "pre")

def get_version():
    if VERSION[3] != "final":
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])
    else:
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()

PRIORITY_MAPPING = {
    "high": "1",
    "medium": "2",
    "low": "3",
    "deferred": "4",
}

# replacement for django.core.mail.send_mail

def send_mail(subject, message, from_email, recipient_list, priority="medium",
              fail_silently=False, auth_user=None, auth_password=None):
    from django.utils.encoding import force_unicode
    from django_mailer.models import Message
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    priority = PRIORITY_MAPPING[priority]
    for to_address in recipient_list:
        Message(to_address=to_address,
                from_address=from_email,
                subject=subject,
                message_body=message,
                priority=priority).save()

def send_html_mail(subject, message, message_html, from_email, recipient_list, 
                    priority="medium", fail_silently=False, auth_user=None,
                    auth_password=None):
    """
    Function to queue html emails
    """
    from django.utils.encoding import force_unicode
    from django_mailer.models import Message
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    priority = PRIORITY_MAPPING[priority]
    for to_address in recipient_list:
        Message(to_address = to_address,
            from_address = from_email,
            subject = subject,
            message_body = message,
            message_body_html = message_html,
            priority=priority).save()

def mail_admins(subject, message, fail_silently=False, priority="medium"):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from django_mailer.models import Message
    priority = PRIORITY_MAPPING[priority]
    for name, to_address in settings.ADMINS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                message_body=message,
                priority=priority).save()

def mail_managers(subject, message, fail_silently=False, priority="medium"):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from django_mailer.models import Message
    priority = PRIORITY_MAPPING[priority]
    for name, to_address in settings.MANAGERS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                message_body=message,
                priority=priority).save()


# Override the django.contrib.auth.forms.PasswordResetForm save function
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
def password_reset_form_save(self, domain_override=None, email_template_name='registration/password_reset_email.html', use_https=False, token_generator=default_token_generator):
    """
    Generates a one-use only link for resetting password and sends to the user
    """
    from django_mailer import send_mail
    for user in self.users_cache:
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
        }
        send_mail(_("Password reset on %s") % site_name,
            t.render(Context(c)), settings.DEFAULT_FROM_EMAIL, [user.email])

from django.contrib.auth.forms import PasswordResetForm
PasswordResetForm.save = password_reset_form_save
