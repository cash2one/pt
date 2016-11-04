# coding: utf-8
from main.views.main_pub import add_main_var
from main.models import CmsOpenVersion, CmsOpenChannel
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
@add_main_var
def activity_list(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def invite_gift(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def new_invite(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def coupons_list(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def new_coupons(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def grant_coupons(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def generate_code(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))


@login_required
@add_main_var
def pcard_list(request, template_name):
    ver_channels = []
    vers = CmsOpenVersion.objects.all()
    for ver in vers:
        ver_channels.append([ver.name, CmsOpenChannel.objects.filter(
            app_version=ver).values_list("name", "id")])
    return render_to_response(template_name, {
        "ver_channels": ver_channels
    }, context_instance=RequestContext(request))
