
from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views

from django.contrib import admin
admin.autodiscover()

from contact_form.views import contact_form

urlpatterns = patterns("",    
    url(r"", include("softball.urls")),
    url(r"^accounts/", include("accounts.urls")),
    url(r"^contact/$", contact_form, name="contact_form"),
    url(r"^contact/sent/$", direct_to_template, { "template": "contact_form/contact_form_sent.html" }, name="contact_form_sent"),
	url(r"^admin/chronograph/job/(?P<pk>\d+)/run/$", "django_chronograph.views.job_run", name="admin_chronograph_job_run"),
    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/(.*)", admin.site.root),
)


if settings.DEBUG:
    import os.path
    urlpatterns += patterns("",
        url(r"^media/(.*)$", "django.views.static.serve", kwargs={"document_root": os.path.join(settings.PROJECT_PATH, "media")}),
    )
