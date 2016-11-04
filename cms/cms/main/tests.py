# coding: utf-8
import os

from cms.settings import INSTALL_TYPE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")
import django
import requests
import json
import random

# from cms.settings import *

if django.VERSION >= (1, 7):
    django.setup()

from main.models import CmsNaviCategory, CmsCpdisplay


def main():
    # categories = CmsNaviCategory.objects.filter(fatherid=0)
    # for category in categories:
    #     #有二级分类
    #     category.type = random.choice([0,1])
    #     category.save()
    try:
        ins = CmsCpdisplay.objects.get(meta_id=13, parent_id=0)
        print(ins)
    except Exception as ex:
        print(ex)
        # goods = CmsGoods.objects.get(id=40091)
        # first_category = CmsNaviCategory.objects.get(id=goods.category)
        # sec_category = CmsNaviCategory.objects.get(id=goods.second_category)
        # send_data = {"id":goods.goods_id,"cateory":first_category.id, "category_name":first_category.name,"second_category":sec_category.id,"second_category_name":sec_category.name}
        # data = {"data":json.dumps(send_data)}
        # normal_url = 'http://search1.putao.so/putao3/goods'
        # test_url = 'http://search.test.putao.so/putao3/goods'
        # r = requests.post(test_url,data=data)
        # print(r.status_code)
        # print(r.content)
        # print(data)
        # content = json.loads(str(r.content,encoding='utf-8'))
        # print(content['msg'])
        # oCmsCheck = CmsCheck.objects.get(id=58)
        # print(oCmsCheck.version,oCmsCheck.data_id,oCmsCheck.table_name)
        # ids = CmsGoods.objects.filter(goods_id=160).values_list("id")
        # print(ids)
        # print(12717 in ids)
        # obj = CmsViewFindTopic.objects.get(id=58)
        # obj.id = None
        # obj.save()
        # print(obj.id)
        # goods = CmsGoods.objects.filter(id=572)
        # citylist = GetAllCities()
        # print(citylist)


def sync_search(goods_id, category_id, sec_category_id):
    if INSTALL_TYPE == 3:
        url = 'http://search1.putao.so/putao3/goods'
    else:
        url = 'http://search.test.putao.so/putao3/goods'
    first_category = CmsNaviCategory.objects.get(id=category_id)
    sec_category = CmsNaviCategory.objects.get(id=sec_category_id)
    send_data = {"id": goods_id, "cateory": first_category.id, "category_name": first_category.name,
                 "second_category": sec_category.id, "second_category_name": sec_category.name}
    data = {"data": json.dumps(send_data)}
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.content)
    print(data)
    content = json.loads(str(r.content, encoding='utf-8'))
    print(content['msg'])


if __name__ == '__main__':
    main()
