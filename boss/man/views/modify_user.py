# coding: utf-8


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import json, datetime
from man_pub import *


class PwdForm(forms.Form):
    password = forms.CharField(max_length=128)


@login_required
@add_common_var
def modify_pwd(request, template_name):
    if request.method == 'POST':
        form = PwdForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            return HttpResponseRedirect(request.GET.get("next", "/"))
    else:
        form = PwdForm()
    return render_to_response(template_name, {
        "errors": form.errors
    },context_instance=RequestContext(request))