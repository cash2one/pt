# coding: utf-8
from __future__ import unicode_literals
import re
import json
import functools
import decimal
from math import ceil
from operator import itemgetter
from django.http import HttpResponse
from cms.settings import CMS_CHECK_ON
import logging
from django.db.models import Q

from common.const import get_2array_value, item_modules, get_nav_text, CheckStatu, check_status
from common.views import channels_status, vers_status, is_submitted, checked_results, get_relate_channel_list, \
    CheckManager, filter_none
from main.models import CmsChannelsType, CmsChannelsAppVersion, CmsChannels, CmsScene, CmsActions, PtCityGroup, \
    PtYellowCitylist, CmsNaviCategory, CmsViewGroupCategory, getCVT, CmsCheck

log = logging.getLogger('config.app')
show_style_list = [[1, "列表"], [2, "卡片"]]


def add_main_var(f):
    @functools.wraps(f)
    def _(*args, **kwargs):
        result = f(*args, **kwargs)
        types = CmsChannelsType.objects.all()
        items = []
        for type in types:
            items.append("['%s', '%s']" % (type.id, type.name))
        types_str = "[%s]" % ",".join(items)
        vars = {
            "user": args[0].user.username,
            "types": types_str,
            'install_type': str(int(CMS_CHECK_ON))
        }
        for key in vars:
            result.content = result.content.replace(("{_cms_begin_%s_end_}" % key).encode("utf8"),
                                                    vars[key].encode("utf8"))
        return result

    return _


def get_ver_channels(type_id):
    """
    根据应用获取版本渠道
    :param type_id: 应用id，APP、IOS、H5、黄页等
    :return:[
        [ver, [channels],ver_status],
        [ver, [channels],ver_status],
        ...
    ]
    """
    vers = CmsChannelsAppVersion.objects.filter(type_id=type_id)
    result = []
    for ver in vers:
        channels = CmsChannels.objects.filter(app_version__id=ver.id).values_list('channel_no', 'order', 'id')
        result.append([ver.app_version, list(channels)])
    return result


# def get_type_ver_channels():
#     result = []
#     types = CmsChannelsType.objects.all()
#     for type in types:
#         vers = []
#         ver_objs = CmsChannelsAppVersion.objects.filter(type_id=type.id)
#         for ver_obj in ver_objs:
#             channels = CmsChannels.objects.filter(app_version__id=ver_obj.id).values_list('id', 'channel_no')
#             ver_status,new_channels = is_ver_channel_submitted(ver_obj,channels)
#             ver = {"name": ver_obj.app_version, "channels": new_channels,"status":ver_status}
#             vers.append(ver)
#         t = {"name": type.name, "vers": vers}
#         result.append(t)
#     return result



# 针对渠道关联和复制的渠道列表，只有审核过的才能进行使用
# def get_type_ver_channels():
#     """
#     :return:
#     [
#         #第一个型号
#         {
#             name: typename,
#             vers: [
#                 #第一个版本
#                 {
#                     name: version,
#                     channels: [[id1, name1,status,can_change], [id2, name2,status,can_change] ...]
#                     status:[status,can_change]
#                 },
#                 #第二个版本
#                 {
#                 },
#                 ...
#             ]
#
#         },
#         #第二个型号
#         ...
#     ]
#     """
#     result = []
#     types = CmsChannelsType.objects.all()
#     for type in types:
#         vers = []
#         ver_objs = CmsChannelsAppVersion.objects.filter(type_id=type.id)
#         for ver_obj in ver_objs:
#             channels = CmsChannels.objects.filter(app_version__id=ver_obj.id).values_list('id', 'channel_no')
#             new_channels=[]
#             for channel in channels:
#                 if is_channel_checked(channel[0]):
#                     new_channels.append(channel)
#             if not CmsCheck.objects.filter(~Q(status=CheckStatu.PASS),table_name="CmsChannelsAppVersion",data_id=ver_obj.id):
#                 ver = {"name": ver_obj.app_version, "channels": new_channels}
#                 vers.append(ver)
#         t = {"name": type.name, "vers": vers}
#         result.append(t)
#     return result
#
#
def get_type_vers():
    """
    :return:
    [
        #第一个型号
        {
            name: typename,
            vers: [
                #第一个版本
                {
                    name: version,
                    id: id,
                },
                #第二个版本
                {
                },
                ...
            ]
        },
        #第二个型号
        ...
    ]
    """
    result = []
    types = CmsChannelsType.objects.all()
    for type in types:
        vers = []
        ver_objs = CmsChannelsAppVersion.objects.filter(type_id=type.id)
        for ver_obj in ver_objs:
            ver = {"name": ver_obj.app_version, "id": ver_obj.id}
            vers.append(ver)
        t = {"name": type.name, "vers": vers}
        result.append(t)
    return result


def get_type_ver_channels(type_id=-1):
    # 类型版本渠道列表
    type_ver_channels = []
    # 根据id获取的版本渠道列表
    ver_channels = []
    # 类型版本列表
    type_vers = []
    types = CmsChannelsType.objects.all()
    for type in types:
        type_ver_channels_temp = []
        type_ver_temp = []
        ver_objs = CmsChannelsAppVersion.objects.filter(type_id=type.id)
        for ver_obj in ver_objs:
            channels = CmsChannels.objects.filter(app_version__id=ver_obj.id).values_list('id', 'channel_no', 'order')
            channels, show_channels = channels_status(channels)
            ver_status = vers_status(ver_obj.id)
            if ver_status[0] == "" or ver_status[0] == "审核成功":
                type_ver_channel = {"name": ver_obj.app_version, "channels": show_channels}
                type_ver_channels_temp.append(type_ver_channel)
                type_ver = {"name": ver_obj.app_version, "id": ver_obj.id}
                type_ver_temp.append(type_ver)
            if ver_obj.type_id == type_id:
                ver_channels.append([ver_obj.app_version, list(channels), ver_status])
        if type_ver_channels_temp:
            t = {"name": type.name, "vers": type_ver_channels_temp}
            type_ver_channels.append(t)
        if type_ver_temp:
            t = {"name": type.name, "vers": type_ver_temp}
            type_vers.append(t)
    if type_id == -1:
        return type_ver_channels
    return type_ver_channels, ver_channels, type_vers


def get_scenes():
    """
    获得所有场景
    :return:
    """
    scenes = CmsScene.objects.values_list("id", "name")
    return scenes


def get_actions_select():
    """
    获得动作选择框
    :return:
    """
    actions = CmsActions.objects.all()
    result = []
    result.append([-1, -1, 1])
    for action in actions:
        if not action.memo:
            item = [action.id, "%d" % (action.id)]
        else:
            item = [action.id, "%d(%s)" % (action.id, action.memo)]
        if not is_submitted('CmsActions', action.id):
            result.append(item)
    result.append([0, 0, 1])
    return json.dumps(result)


def slice_actions_select(search_key, page=1, per_page=10):
    if search_key and len(search_key) > 0:
        actions = CmsActions.objects. \
            filter(Q(memo__contains=search_key) | Q(id__contains=search_key)).values_list('id', 'memo').order_by('-id')
    else:
        actions = CmsActions.objects.all().values_list('id', 'memo').order_by('-id')
    total_count = actions.count()
    total_page = ceil(total_count / per_page)
    result = []
    cur = page - 1
    if cur == 0:
        result.append([-1, -1, 1])

    if page <= total_page and cur >= 0:
        for action in actions[cur * per_page:(cur + 1) * per_page]:
            if action[1] is None or len(action[1]) == 0:
                item = [action[0], "%d" % (action[0])]
            else:
                item = [action[0], "%d(%s)" % (action[0], action[1])]
            if not is_submitted('CmsActions', action[0]):
                result.append(item)
        if cur == total_page - 1:
            result.append([0, 0, 1])
    return total_page, result


def get_city_group():
    oPtCityGroup = PtCityGroup.objects.all()
    return oPtCityGroup


def get_city_list():
    """得到城市列表
        格式如下
    [{'proname': '安徽省', 'pinyin': 'anhuisheng', 'citylist': ['合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市', '阜阳市', '宿州市', '六安市', '亳州市', '池州市', '宣城市']},
    {'proname': '福建省', 'pinyin': 'fujiansheng', 'citylist': ['福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市', '宁德市']},
    {'proname': '甘肃省', 'pinyin': 'gansusheng', 'citylist': ['兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市', '张掖市', '平凉市', '酒泉市', '庆阳市', '定西市', '陇南市', '临夏', '甘南']},
    {'proname': '广东省', 'pinyin': 'guangdongsheng', 'citylist': ['广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市', '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '东莞市', '中山市', '潮州市', '揭阳市', '云浮市']},
    {'proname': '广西壮族自治区', 'pinyin': 'guangxizhuangzuzizhiqu', 'citylist': ['南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市', '贺州市', '河池市', '来宾市', '崇左市']},
    {'proname': '贵州省', 'pinyin': 'guizhousheng', 'citylist': ['贵阳市', '六盘水市', '遵义市', '安顺市', '毕节市', '铜仁市', '黔西南', '黔东南', '黔南']},
    {'proname': '海南省', 'pinyin': 'hainansheng', 'citylist': ['海口市', '三亚市', '三沙市']},
    {'proname': '河北省', 'pinyin': 'hebeisheng', 'citylist': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市']},
    {'proname': '黑龙江省', 'pinyin': 'heilongjiangsheng', 'citylist': ['哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市', '佳木斯市', '七台河市', '牡丹江市', '黑河市', '绥化市', '大兴安岭']},
    {'proname': '河南省', 'pinyin': 'henansheng', 'citylist': ['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '濮阳市', '许昌市', '漯河市', '三门峡市', '南阳市', '商丘市', '信阳市', '周口市', '驻马店市']},
    {'proname': '湖北省', 'pinyin': 'hubeisheng', 'citylist': ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市', '咸宁市', '随州市', '恩施']},
    {'proname': '湖南省', 'pinyin': 'hunansheng', 'citylist': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市', '湘西']},
    {'proname': '江苏省', 'pinyin': 'jiangsusheng', 'citylist': ['南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市']},
    {'proname': '江西省', 'pinyin': 'jiangxisheng', 'citylist': ['南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市', '抚州市', '上饶市']},
    {'proname': '吉林省', 'pinyin': 'jilinsheng', 'citylist': ['长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '松原市', '白城市', '延边']},
    {'proname': '辽宁省', 'pinyin': 'liaoningsheng', 'citylist': ['沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦市', '铁岭市', '朝阳市', '葫芦岛市']},
    {'proname': '内蒙古自治区', 'pinyin': 'neimengguzizhiqu', 'citylist': ['呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市', '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市', '乌兰察布市', '兴安盟', '锡林郭勒', '阿拉善盟']}]
    """
    provinces = PtYellowCitylist.objects.filter(parent_id=0)
    citylist = []
    pattern = re.compile("(\w+)", re.U)
    for province in provinces:
        cities = PtYellowCitylist.objects.filter(parent_id=province.self_id)
        temp = []
        temp_provice = {}
        filter_lst = [u'北京市', u'上海市', u'重庆市', u'天津市', u'全国']
        if province.city_name in filter_lst:
            continue
        for city in cities:
            cityname = city.city_name
            if len(cityname) > 2 and cityname[-1] in [u"市", u"县"]:
                cityname = cityname[:-1]
            temp.append(cityname)
        temp_provice['citylist'] = temp
        temp_provice['pinyin'] = "".join(pattern.findall(province.city_py))
        temp_provice['proname'] = province.city_name
        citylist.append(temp_provice)
    citylist = sorted(citylist, key=itemgetter('pinyin'))
    return json.dumps(citylist)


def GetAllCities():
    result = []
    citylist = get_city_list()
    for item in citylist:
        result += item['citylist']
    return result + ['北京', '上海', '重庆', '天津']


# 传入表单对象
# 返回格式化的field对象和表单错误
def format_form(form):
    try:
        if form.data and len(form.data) > 0:
            fields = form.data
        else:
            fields = form.initial
        for key, value in fields.items():
            if key == 'city' and value != "":
                fields[key] = json.dumps(RemoveShiCity(value))
            elif isinstance(value, decimal.Decimal):
                fields[key] = json.dumps(str(value))
            elif value is None:
                fields[key] = json.dumps("")
            else:
                fields[key] = json.dumps(value)
        errors = {}
        for item in form.errors:
            errors[item] = form.errors[item][0]

        return errors, fields

    except Exception as ex:
        log.error("OVER")
        log.error(ex)


def RemoveShiCity(citystr):
    citylist = citystr.split(",")
    for i in range(len(citylist)):
        city = citylist[i]
        if len(city) > 2 and city[-1] in ["市", "县"]:
            citylist[i] = city[:-1]
    return ",".join(citylist)


def get_first_categories():
    result = []
    first_categories = CmsNaviCategory.objects.filter(fatherid=0).values_list('id', 'name')
    for first_category in first_categories:
        first_category = list(first_category)
        if CmsViewGroupCategory.objects.filter(category_id=first_category[0]):
            group_name = CmsViewGroupCategory.objects.filter(category_id=first_category[0])[0].group.name
            first_category.append(group_name)
            result.append(first_category)
    result = checked_results('CmsNaviCategory', result, 0)
    return result


# 返回分类列表
def get_second_categories():
    categories = CmsNaviCategory.objects.filter(parent_id=0, fatherid=0, used_by_op=1).order_by("name")
    result = []
    for category in categories:
        children = CmsNaviCategory.objects.filter(parent_id=0, fatherid=category.id, used_by_op=1)
        if children:
            result.append([category.id, category.name, category.memo, 0])
        for c in children:
            result.append([c.id, c.name, c.memo, 1])
    return result


def set_id_into_records(total, record, id):
    for d in total:
        if d["record"] == record:
            d["ids"].append(id)
            return
    total.append({"record": record, "ids": [id]})


def show_cvt(channel_id, module):
    if channel_id:
        try:
            # 不是删除渠道
            m = get_2array_value(item_modules, module)
            relate_channels = get_relate_channel_list(channel_id, m)
            relate_channels.append(channel_id)
            relate_channels.sort()
            types = []
            channel_nos = []
            app_versions = []
            for channel in relate_channels:
                obj = CmsChannels.objects.get(id=channel)
                c, v, t = getCVT(channel)
                types.append(get_nav_text(str(t)))
                app_versions.append(v)
                channel_nos.append(obj.channel_no)
            return "<br />".join(types), "<br />".join(app_versions), "<br />".join(channel_nos)
        except:
            # 删除的是渠道，情况比较特殊
            c, v, t = getCVT(channel_id, 'online')
            return get_nav_text(str(t)), v, c

    else:
        return "内容库", "内容库", "内容库"


def get_record_detail(ids):
    result = []
    for id in ids:
        record = CmsCheck.objects.get(id=id)
        if not record.is_show:
            continue
        result.append(CheckManager.get_record(record))
    return result


def get_record_history():
    records = CmsCheck.objects.filter(
        Q(status=CheckStatu.PASS) | Q(status=CheckStatu.REJECT))  # Q(status=CheckStatu.REVERT) |
    result = []
    for record in records:
        try:
            type, version, channel_no = show_cvt(record.channel_id, record.module)
            data = [
                get_2array_value(check_status, str(record.status)),
                record.submit_person,
                type,
                version,
                channel_no,
                record.module,
                str(record.check_date)
            ]
            set_id_into_records(result, data, record.id)
        except:
            continue
    result.sort(key=lambda o: (o["record"][6]), reverse=True)
    filter_none(result)
    return result


def get_cate2_list():
    viewgroupcates = CmsViewGroupCategory.objects.filter(group__name="到家服务")
    cate2s = []
    for viewgroupcate in viewgroupcates:
        cate2s.append(viewgroupcate.category)
    return cate2s


"""返回分类列表
0---所有分类
1---到家服务
2---功能服务
"""


def get_categories():
    categories = CmsNaviCategory.objects.filter(fatherid=0, used_by_op=1).order_by("name")
    result = []
    for category in categories:
        if CMS_CHECK_ON:
            if CmsCheck.objects.filter(~Q(status=CheckStatu.PASS), table_name='CmsNaviCategory', data_id=category.id):
                continue
        try:
            cate_group_name = CmsViewGroupCategory.objects.get(category=category).group.name
        except:
            cate_group_name = ""
        result.append([category.id, category.name, category.memo, 0, cate_group_name, category.type])
        children = CmsNaviCategory.objects.filter(parent_id=0, fatherid=category.id, used_by_op=1)
        for c in children:
            if CMS_CHECK_ON:
                if not CmsCheck.objects.filter(~Q(status=CheckStatu.PASS), table_name='CmsNaviCategory', data_id=c.id):
                    result.append([c.id, c.name, c.memo, 1, cate_group_name, category.type])
            else:
                result.append([c.id, c.name, c.memo, 1, cate_group_name, category.type])
    return result


def get_v37_categories():
    categories = CmsNaviCategory.objects.filter(fatherid=0, used_by_op=1).order_by("name")
    result = []
    for category in categories:
        if CMS_CHECK_ON:
            if CmsCheck.objects.filter(~Q(status=CheckStatu.PASS), table_name='CmsNaviCategory', data_id=category.id):
                continue
        try:
            cate_group_name = CmsViewGroupCategory.objects.get(category=category).group.name
        except:
            cate_group_name = ""
        result.append([category.id, category.name, category.memo, 0, cate_group_name, category.type])
    return result


def response(code, msg, extra={}):
    result = {'code': code, 'msg': msg, 'extra': extra}
    return HttpResponse(json.dumps(result))
