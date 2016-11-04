# coding: utf-8
from __future__ import unicode_literals
import json
# import time
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass


class CategoryGroupType:
    daojia = u"到家服务"
    live = u"功能服务"


class JPUSH:
    SWITCH = True
    DEFAULT_CHANNELNO = "putao_live_01"
    DEFAULT_VERSION = "3.3.0"


class CheckOpType:
    """
    审核，操作类型
    """
    NEW = "1"
    EDIT = "2"
    DELETE = "3"


class CheckStatu:
    """审核状态"""
    # 待提交
    WAIT_SUBMIT = "1"
    # 已提交
    SUBMIT = "2"
    # 已撤销
    REVERT = "3"
    # 审核成功
    PASS = "4"
    # 被驳回
    REJECT = "5"
    # 审核执行失败
    CHECK_ERROR = "6"


check_status = [
    [CheckStatu.WAIT_SUBMIT, u"待提交"],
    [CheckStatu.SUBMIT, u"已提交"],
    [CheckStatu.REVERT, u"已撤销"],
    [CheckStatu.PASS, u"审核成功"],
    [CheckStatu.REJECT, u"被驳回"],
    [CheckStatu.CHECK_ERROR, u"审核执行失败"]
]


class AuthCodeName:
    # 应用名称
    APP_LABEL = "man"
    # 账号管理
    MAN = "man"
    # 审核权限
    CHECK = "check"
    # 配置权限
    CONFIG = "config"


class MainConst:
    # 默认每页显示行数
    PER_PAGE = 20


class CONFIG_ITEMS:
    ACTIVITY = "1"  # 活动
    AD = "2"  # 广告
    CATEGORY_PAGE_SERVICES = "3"  # 分类页服务
    CHOICENESS_CATEGORY = "4"  # 精品分类
    COMMON_SERVICES = "5"  # 常用服务
    CONFIG_OPERATION = "6"  # 运营配置
    COUPONS = "7"  # 优惠券
    FOUNDPAGE = "8"  # 发现页
    HOMEPAGE = "9"  # 首页
    LIKES = "10"  # 猜你喜欢
    STREAMS = "11"  # 内容流
    SECOND_CATEGORY = "12"  # 二级分类
    SCREEN_AD = "13"  # 开屏广告
    NATIVE_ACTIVITY = "14"  # Native活动
    CP = "15"  # 品牌
    COUPON_ACTIVITY = "16"  # 业务活动
    SHARE_COUPON = "17"  # 分享券
    SECKILLS = "18"  # 秒杀活动


class CmsModule:
    MAIN_SERVICE = u"内容库-服务"
    MAIN_GOODS = u"内容库-商品"
    MAIN_IMAGE = u"内容库-图库"
    MAIN_ACTION = u"内容库-动作"
    MAIN_CITYGROUP = u"内容库-城市分组"
    MAIN_CATEGORY = u"内容库-分类"
    MAIN_COUPON = u"内容库-优惠券"
    MAIN_TOPIC = u"内容库-专题"
    MAIN_SHOP = u"内容库-商家"
    MAIN_CHANNEL = u"内容库-渠道"

    CONFIG_AD = u"配置-广告"
    CONFIG_COMMON_SERVICES = u"配置-常用服务"
    CONFIG_PAGE = u"配置-分类页服务"
    CONFIG_HOMEPAGE = u"配置-首页专题"
    CONFIG_FOUNDPAGE = u"配置-发现页专题"
    CONFIG_STREAM = u"配置-内容流"
    CONFIG_OPERATION = u"配置-运营配置"
    CONFIG_LIKE = u"配置-猜你喜欢"
    CONFIG_ACTIVITY = u"配置-活动"
    CONFIG_CHOICENESS = u"配置-精品分类"
    CONFIG_COUPON = u"配置-优惠券"
    CONFIG_SECOND_CATEGORY = u"配置-二级分类"
    CONFIG_SCREEN_AD = u"配置-开屏广告"
    CONFIG_NATIVE_ACTIVITY = u"配置-Native活动"

    CONFIG_SHARE_COUPON = u"配置-分享券"
    CONFIG_SECKILLS = u"配置-秒杀"


item_modules = [
    [CmsModule.CONFIG_AD, CONFIG_ITEMS.AD],
    [CmsModule.CONFIG_COMMON_SERVICES, CONFIG_ITEMS.COMMON_SERVICES],
    [CmsModule.CONFIG_PAGE, CONFIG_ITEMS.CATEGORY_PAGE_SERVICES],
    [CmsModule.CONFIG_HOMEPAGE, CONFIG_ITEMS.HOMEPAGE],
    [CmsModule.CONFIG_FOUNDPAGE, CONFIG_ITEMS.FOUNDPAGE],
    [CmsModule.CONFIG_STREAM, CONFIG_ITEMS.STREAMS],
    [CmsModule.CONFIG_OPERATION, CONFIG_ITEMS.CONFIG_OPERATION],
    [CmsModule.CONFIG_LIKE, CONFIG_ITEMS.LIKES],
    [CmsModule.CONFIG_ACTIVITY, CONFIG_ITEMS.ACTIVITY],
    [CmsModule.CONFIG_CHOICENESS, CONFIG_ITEMS.CHOICENESS_CATEGORY],
    [CmsModule.CONFIG_COUPON, CONFIG_ITEMS.COUPONS],
    [CmsModule.CONFIG_SECOND_CATEGORY, CONFIG_ITEMS.SECOND_CATEGORY],
    [CmsModule.CONFIG_SCREEN_AD, CONFIG_ITEMS.SCREEN_AD],
    [CmsModule.CONFIG_NATIVE_ACTIVITY, CONFIG_ITEMS.NATIVE_ACTIVITY],
    [CmsModule.CONFIG_SHARE_COUPON, CONFIG_ITEMS.SHARE_COUPON],
    [CmsModule.CONFIG_SECKILLS, CONFIG_ITEMS.SECKILLS],

]

ad_size = [[2, u"半栏"], [1, u"通栏"]]
ad_type = [[2, u"单播"], [1, u"轮播"]]
open_type = [[0, u"服务"], [1, u"商品"]]
streams_type = [[1, u"活动"], [2, u"服务"], [3, u"商品"], [4, u"搜索"]]
screen_ad_times = [[1, u"仅展示一次"], [100, u"每次进入展示"]]

product_types = [
    [3, u"充话费"],
    [4, u"充流量"],
    [6, u"电影票"],
    [18, u"QQ充值"],
    [22, u"游戏充值"],
    [110, u"全托管订单"]
]


def get_2array_value(arr, v):
    for item in arr:
        if v == item[0]:
            return item[1]
    return ""


def get_show_style(v):
    return u"卡片" if v == 2 else u"列表"


class OP_CONFIG:
    PUSH = "push_time"  # 消息推送开关  0是关    1是开
    PUSH_TEXT = u"消息推送开关"
    PUSH_CLOSE = "0"
    PUSH_OPEN = "1"
    PUSH_CLOSE_TEXT = u"关"
    PUSH_OPEN_TEXT = u"开"

    TAB_SHOW = "tab_show"  # TAB打点   0是关    1是开
    TAB_SHOW_TEXT = u"TAB打点"
    TAB_SHOW_CLOSE = "0"
    TAB_SHOW_OPEN = "1"
    TAB_SHOW_CLOSE_TEXT = u"关"
    TAB_SHOW_OPEN_TEXT = u"开"

    PAY_LIST = "pay_list"  # 1-支付宝   2-微信支付  3-联想支付  4-   5-   无[0,1,2]
    PAY_LIST_TEXT = u"支付方式"
    PAY_LIST_ZHIFUBAO = "1"
    PAY_LIST_WEIXIN = "2"
    PAY_LIST_LENOVO = "3"
    PAY_LIST_4 = "4"
    PAY_LIST_5 = "5"
    PAY_LIST_JINLI_ZHIFUBAO = "6"
    PAY_LIST_JINLI_WEIXIN = "7"
    PAY_LIST_NONE = "[0,1,2]"
    PAY_LIST_ZHIFUBAO_TEXT = u"支付宝"
    PAY_LIST_WEIXIN_TEXT = u"微信支付"
    PAY_LIST_LENOVO_TEXT = u"联想支付"
    PAY_LIST_4_TEXT = "4"
    PAY_LIST_5_TEXT = "5"
    PAY_LIST_JINLI_ZHIFUBAO_TEXT = u"金立阿里支付"
    PAY_LIST_JINLI_WEIXIN_TEXT = u"金立微信支付"
    PAY_LIST_NONE_TEXT = u"无"

    @classmethod
    def get_key_text(cls, key):
        """
            根据类型，获取类型对应的中文
        """
        d = {
            cls.PUSH: cls.PUSH_TEXT,
            cls.TAB_SHOW: cls.TAB_SHOW_TEXT,
            cls.PAY_LIST: cls.PAY_LIST_TEXT
        }
        return d.get(key, key)

    @classmethod
    def get_value_text(cls, key, value):
        """
            根据类型和值，获取值对应的中文
            key是pay_list的时候，value是个数组
        """
        d = {
            cls.PUSH: {
                cls.PUSH_CLOSE: cls.PUSH_CLOSE_TEXT,
                cls.PUSH_OPEN: cls.PUSH_OPEN_TEXT
            },
            cls.TAB_SHOW: {
                cls.TAB_SHOW_CLOSE: cls.TAB_SHOW_CLOSE_TEXT,
                cls.TAB_SHOW_OPEN: cls.TAB_SHOW_OPEN_TEXT
            },
            cls.PAY_LIST: {
                cls.PAY_LIST_ZHIFUBAO: cls.PAY_LIST_ZHIFUBAO_TEXT,
                cls.PAY_LIST_WEIXIN: cls.PAY_LIST_WEIXIN_TEXT,
                cls.PAY_LIST_LENOVO: cls.PAY_LIST_LENOVO_TEXT,
                cls.PAY_LIST_4: cls.PAY_LIST_4_TEXT,
                cls.PAY_LIST_5: cls.PAY_LIST_5_TEXT,
                cls.PAY_LIST_JINLI_ZHIFUBAO: cls.PAY_LIST_JINLI_ZHIFUBAO_TEXT,
                cls.PAY_LIST_JINLI_WEIXIN: cls.PAY_LIST_JINLI_WEIXIN_TEXT
            }
        }
        if key == cls.PAY_LIST:
            if value == cls.PAY_LIST_NONE:
                return cls.PAY_LIST_NONE_TEXT
            else:
                return [d[cls.PAY_LIST].get(str(item), item) for item in json.loads(value)]
        else:
            return d.get(key, {}).get(value, value)


def get_nav_text(t):
    d = {
        "1": u"葡萄生活Android版",
        "2": u"生活黄页",
        "4": u"葡萄生活H5版",
        "5": u"葡萄生活iOS版"
    }
    return d.get(str(t), "")


CATE_TYPE = (
    (0, 'old'),
    (1, 'new'),
)
