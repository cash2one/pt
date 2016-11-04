#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from main.models import *
from django import forms

from main.models import CmsActions, CmsChannelsAppVersion, CmsChannels, PtCityGroup, CmsGoods, CmsServices, \
    CmsNaviCategory, CmsCoupon, CmsSpecialTopic, CmsCategoryItembean, CmsCPCategory, CmsCP, CmsCpdisplay, \
    CmsCategoryGroup, CmsProblem
from man.models import AuthUser

class ActionForm(forms.ModelForm):
    type = forms.IntegerField()
    pt_h5 = forms.IntegerField()
    class Meta:
        model = CmsActions
        fields = '__all__'


class NewVerForm(forms.ModelForm):
    type_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = CmsChannelsAppVersion
        fields = '__all__'


class NewChannelForm(forms.Form):
    channel_type_id = forms.IntegerField(widget=forms.HiddenInput)
    input_app_version = forms.CharField(widget=forms.HiddenInput)
    channel_no = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': '请输入渠道号'}))
    order = forms.BooleanField(required=False)

    def clean_channel_no(self):
        """
        验证版本渠道有没有重复
        :return:
        """
        channel_no = self.cleaned_data["channel_no"]
        if CmsChannels.objects.filter(app_version__app_version=self.cleaned_data["input_app_version"], channel_no=channel_no):
            raise forms.ValidationError("渠道号%s重复" % self.cleaned_data["channel_no"])
        return channel_no



class CityGroupForm(forms.ModelForm):
    city = forms.CharField()
    class Meta:
        model = PtCityGroup
        fields = '__all__'


class GoodsForm(forms.ModelForm):
    city = forms.CharField()
    class Meta:
        model = CmsGoods
        exclude = ['mobile', 'parent_id']

    def clean_location(self):
        """
        小于128的整数
        :return:
        """
        location = self.cleaned_data["location"]
        if location not in range(0, 128):
            raise forms.ValidationError("排序的值范围为0到127")
        return location


class ServiceForm(forms.ModelForm):
    city = forms.CharField()
    class Meta:
        model = CmsServices
        exclude = ['source_id', 'mobile']

    def clean_location(self):
        """
        小于128的整数
        :return:
        """
        location = self.cleaned_data["location"]
        if location not in range(0, 128):
            raise forms.ValidationError("排序的值范围为0-127")
        return location


#分类表表单
class NaviCategoryForm(forms.ModelForm):
    class Meta:
        model = CmsNaviCategory
        exclude = ['strategy', 'used_by_op']


#优惠券表单
class CouponsForm(forms.ModelForm):
    city = forms.CharField()
    class Meta:
        model = CmsCoupon
        fields = '__all__'


#专题表 表单
class SpecialTopicForm(forms.ModelForm):
    city = forms.CharField(required=True)
    class Meta:
        model = CmsSpecialTopic
        exclude = ['create_time','update_time']


#静态数据商户数据表单
class CmsCategoryItembeanForm(forms.ModelForm):
    city = forms.CharField(required=True)
    class Meta:
        model = CmsCategoryItembean
        exclude=['strategy','parent_id']


#用户数据表单
class AuthUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    is_staff = forms.IntegerField(required=True)
    class Meta:
        model = AuthUser
        exclude=['last_login','is_superuser','first_name','last_name','is_active','date_joined']


#品牌分类表单
class CmsCPCategoryForm(forms.ModelForm):
    class Meta:
        model = CmsCPCategory
        fields = '__all__'


#品牌表单
class CmsCPForm(forms.ModelForm):
    location2 = forms.IntegerField(required=True)
    class Meta:
        model = CmsCP
        fields = '__all__'


#品牌展示表单
class CmsCpdisplayForm(forms.ModelForm):
    class Meta:
        model = CmsCpdisplay
        fields = '__all__'


#服务类别组表单
class CmsCategoryGroupForm(forms.ModelForm):
    class Meta:
        model = CmsCategoryGroup
        fields = '__all__'

#常见问题
class CmsProblemForm(forms.ModelForm):
    class Meta:
        model = CmsProblem
        fields = '__all__'