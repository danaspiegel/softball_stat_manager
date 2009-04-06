# Copyright (c) 2008-9 Sociable Marketplaces, Inc. All rights reserved.

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from accounts.forms import AccountForm

@login_required
def edit(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            request.user.message_set.create(message='Your account has been updated')
            return HttpResponseRedirect(reverse('account'))
    else:
        form = AccountForm(instance=request.user)
    return render_to_response('account/edit.html', { 'form': form }, context_instance=RequestContext(request))
