#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'putao'
__mtime__ = '2015/9/14'
"""

# from main.models import *
from django import forms
from main.models import CmsAdbeans, CmsAds, CmsOpconfig, CmsStreamcontent, \
    CmsStreamcontentbeans, CmsNavicategories, \
    CmsLikes, CmsActivities, CmsNativeActivity, CmsChoicenessCategory, \
    CmsCategoryItem, CmsScreenads, CmsOpenService, \
    CmsActivityV37, CmsShareCoupon, CmsSecKill


class CmsAdbeansForm(forms.ModelForm):
    """广告表单"""
    city = forms.CharField(required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = CmsAdbeans
        exclude = ['strategy', 'open_cp_id',
                   'open_service_id', 'open_goods_id']


class CmsAdsForm(forms.ModelForm):
    """广告组表单"""
    class Meta:
        model = CmsAds
        fields = '__all__'


class OpconfigForm(forms.ModelForm):
    """运营配置表单"""
    class Meta:
        model = CmsOpconfig
        fields = '__all__'


class StreamcontentForm(forms.ModelForm):
    """内容流组表单"""
    class Meta:
        model = CmsStreamcontent
        fields = '__all__'


class StreamcontentbeansForm(forms.ModelForm):
    """内容流表单"""
    city = forms.CharField(required=True)

    class Meta:
        model = CmsStreamcontentbeans
        exclude = ['strategy', 'open_cp_id',
                   'open_service_id', 'open_goods_id']


class NavicategoriesForm(forms.ModelForm):
    """左边导航栏表单(分类组表)"""
    class Meta:
        model = CmsNavicategories
        fields = '__all__'


class LikesForm(forms.ModelForm):
    """猜你喜欢表单"""
    class Meta:
        model = CmsLikes
        fields = '__all__'


class ActivitiesForm(forms.ModelForm):
    """活动表单"""
    city = forms.CharField(required=True)

    class Meta:
        model = CmsActivities
        # fields = '__all__'
        exclude = ['strategy', 'open_cp_id',
                   'open_service_id', 'open_goods_id']


class CmsNativeActivityForm(forms.ModelForm):
    """本地活动表单"""
    city = forms.CharField(required=True)

    class Meta:
        model = CmsNativeActivity
        exclude = ['strategy', 'open_cp_id',
                   'open_service_id', 'open_goods_id']


class ChoicenessCategoryForm(forms.ModelForm):
    """精品分类表单"""
    img_url = forms.CharField(required=True)
    img_url_d = forms.CharField(required=True)
    city = forms.CharField(required=True)

    class Meta:
        model = CmsChoicenessCategory
        # fields = '__all__'
        exclude = ['strategy', 'status']


class CmsCategoryItemForm(forms.ModelForm):
    """二级分类表单"""
    class Meta:
        model = CmsCategoryItem
        fields = '__all__'


class CmsScreenadsForm(forms.ModelForm):
    """开屏广告表单"""
    class Meta:
        model = CmsScreenads
        fields = '__all__'
        exclude = ['strategy', 'open_cp_id', 'open_service_id',
                   'open_goods_id', 'open_type', 'location']


class CmsOpenServiceForm(forms.ModelForm):
    """开放服务表单"""
    class Meta:
        model = CmsOpenService
        fields = '__all__'


class CmsActivityV37Form(forms.ModelForm):
    """优惠券活动表单"""
    class Meta:
        model = CmsActivityV37
        exclude = ['parent_id', 'cp', 'goods']


class CmsShareCouponForm(forms.ModelForm):
    """分享券"""
    class Meta:
        model = CmsShareCoupon
        fields = '__all__'


class CmsSeckilForm(forms.ModelForm):
    """秒杀配置"""
    class Meta:
        model = CmsSecKill
        fields = '__all__'
