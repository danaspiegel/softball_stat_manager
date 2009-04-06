# Copyright (c) 2008-9 Sociable Marketplaces, Inc. All rights reserved.


import datetime
from django.forms import *
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django.forms import fields, widgets
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

class AccountForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
