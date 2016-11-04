# coding: utf-8

from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from common.views import add_common_var, report_render


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
            return HttpResponseRedirect(request.GET.get("next", u"/"))
    else:
        form = PwdForm()
    return report_render(request,template_name, {
        "errors": form.errors
    }, context_instance=RequestContext(request))
