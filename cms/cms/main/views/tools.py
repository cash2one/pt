# coding: utf-8

# from .main_pub import *
from django.http import HttpResponse

from common.const import AuthCodeName
from common.views import setCpAction
from main.models import CmsScene, AuthGroup, DjangoContentType, AuthPermission, AuthGroupPermissions, AuthUserGroups, \
    AuthUser, CmsCP


def create_scenes(request):
    """
        CREATE TABLE `cms_scene` (
          `id` int(11) NOT NULL,
          `name` varchar(128) NOT NULL,
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    """
    scenes = [
        [0, "首页"],
        [2, "品牌页"],
        [1, "导航页"],
        [7, "三方联系人黄页"],
        [8, "三方服务列表for联系人"],
        [9, "钱包"],
        [10000, "查话费"],
        [10001, "充话费"],
        [10002, "充流量"],
        [10003, "查快递"],
        [10004, "酒店主页"],
        [10008, "酒店订单页"],
        [10009, "添加服务界面"],
        [10010, "火车票"],
        [10011, "电影列表"],
        [10012, "电影院列表"],
        [10013, "公交换乘"],
        [10014, "站点路线"],
        [10015, "水"],
        [10016, "电"],
        [10017, "煤气"],
        [10018, "团购"],
        [10019, "打车"],
        [10020, "美食"],
        [10021, "QQ充值"],
        [10022, "游戏充值"],

    ]
    for scene in scenes:
        a = CmsScene(id=scene[0], name=scene[1])
        a.save()
    return HttpResponse(0)


# 暂时用不到
# def create_city(request):
#     Citylst =[
#         ['*','quan 全 guo 国',0,-1,0,'0000',1]
#     ]
#     for city in Citylst:
#         try:
#             oPtYellowCitylist=PtYellowCitylist(city_name=city[0],city_py=city[1],self_id=city[2],parent_id=city[3],city_type=city[4],city_hot=city[6])
#             oPtYellowCitylist.save()
#         except Exception as ex:
#             print(ex)
#     return HttpResponse(0)

"""
#广告新增广告名
alter TABLE cms_adbeans add COLUMN name varchar(200) DEFAULT null;

#2015-10-23
#广告新增机型
alter TABLE cms_adbeans add COLUMN phone_type varchar(200) DEFAULT null;
"""

"""
#更改运营配置和精品分类
#运营配置表
#2015-10-22
DROP TABLE cms_opconfig;
CREATE TABLE `cms_opconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(128) COLLATE utf8_bin NOT NULL,
  `value` varchar(1024) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
INSERT INTO cms_opconfig(`key`,`value`)  SELECT `key`,`value` from cms_view_opconfig group by `key`,`value`;
rename TABLE cms_view_opconfig TO cms_view_opconfig_copy;
CREATE TABLE `cms_view_opconfig` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `opconfig_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `status` tinyint(1) DEFAULT '0' COMMENT '0:待审核，1：审核中，待发布；2：发布中；3：已发布',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`opconfig_id`,`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
REPLACE into cms_view_opconfig(`opconfig_id`,`channel_id`) SELECT a.id,b.channel_id from cms_opconfig a,cms_view_opconfig_copy b where a.`key`=b.`key` and a.`value`=b.`value`;
#精品分类
CREATE TABLE `cms_view_choiceness_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `choiceness_category_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `status` tinyint(1) DEFAULT '0' COMMENT '0:待审核，1：审核中，待发布；2：发布中；3：已发布',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`choiceness_category_id`,`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
INSERT into cms_view_choiceness_category(`choiceness_category_id`,`channel_id`) SELECT id,channel_id from cms_choiceness_category;
ALTER TABLE cms_choiceness_category DROP COLUMN `channel_id`;

"""

"""
#静态数据商户增加一个字段parent_id
#2015-10-22
ALTER TABLE cms_category_itembean ADD COLUMN parent_id int(11) DEFAULT -1;
"""

"""
#创建渠道关联表
#2015-10-22
CREATE TABLE `pt_cms_db`.`cms_channel_channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id1` int(11) NOT NULL,
  `channel_id2` int(11) NOT NULL,
  `config_items` varchar(128) DEFAULT NULL,
  `op_type` int(4) DEFAULT '0' COMMENT '渠道操作类型 0:关联  1:复制',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

"""
"""
#修改内容流表已售数量sold为非必填
ALTER TABLE cms_streamcontentbeans MODIFY COLUMN `sold` int(11) DEFAULT NULL;
"""
"""
#发现页添加运营标签
ALTER TABLE cms_view_find_topic add column mark_info varchar(200) DEFAULT NULL COMMENT '运营标签';
"""

"""
#新建开屏广告表
CREATE TABLE `cms_screenads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `img_url` varchar(256) NOT NULL,
  `start` int(11) NOT NULL,
  `end` int(11) NOT NULL,
  `location` tinyint(4) NOT NULL,
  `action_id` int(11) NOT NULL,
  `strategy` tinyint(1) DEFAULT '0' COMMENT '0:默认策略 1:覆盖策略',
  `valid_time` varchar(256) DEFAULT '* * * * *',
  `city` text COMMENT '城市',
  `open_cp_id` int(11) NOT NULL,
  `open_service_id` int(11) NOT NULL,
  `open_goods_id` int(11) NOT NULL,
  `open_type` tinyint(4) NOT NULL,
  `action_json` mediumtext,
  `phone_type` varchar(200) DEFAULT NULL,
  `show_times` int(11) DEFAULT NULL COMMENT '展示次数',
  `show_hold` int(11) DEFAULT NULL COMMENT '展示时长 精确到秒',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#开屏广告和渠道关联表
CREATE TABLE `cms_view_screenads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `screenad_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `status` tinyint(1) DEFAULT '0' COMMENT '0:待审核，1：审核中，待发布；2：发布中；3：已发布',
  PRIMARY KEY (`id`),
  UNIQUE KEY `screenad_id` (`screenad_id`,`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

"""
#修改本地活动表，添加活动倒计时开始时间和活动倒计时结束时间
ALTER table cms_native_activity ADD COLUMN open_time int(11) DEFAULT NULL COMMENT '活动倒计时开始时间';
ALTER table cms_native_activity ADD COLUMN close_time int(11) DEFAULT NULL COMMENT '活动倒计时结束时间';

"""

"""
账号管理

"""


def create_permissions(request):
    # auth_group建立两个成员，管理员和运营人员
    groups = ["管理员", "运营人员"]
    for group in groups:
        o = AuthGroup(name=group)
        o.save()

    # django_content_type建立一个成员，id=200
    o = DjangoContentType(id=200, app_label="main", model="main")
    o.save()

    # auth_permission建立一个权限，账户管理权限
    o = AuthPermission(name="man", content_type_id=200, codename=AuthCodeName.MAN)
    o.save()

    # auth_permission建立一个权限，审核权限
    o = AuthPermission(name="man", content_type_id=200, codename=AuthCodeName.CHECK)
    o.save()

    # auth_permission建立一个权限，配置权限
    o = AuthPermission(name="man", content_type_id=200, codename=AuthCodeName.CONFIG)
    o.save()

    # auth_group_permissions建立组-权限关联
    o = AuthGroupPermissions(group=AuthGroup.objects.get(name="管理员"),
                             permission=AuthPermission.objects.get(content_type_id=200, codename="man"))
    o.save()

    # 把超级管理员放到组里去
    o = AuthUserGroups(user=AuthUser.objects.get(id=1), group=AuthGroup.objects.get(name="管理员"))
    o.save()
    return HttpResponse(0)


"""
#2015-11-6
#审核表
CREATE TABLE `cms_check` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL DEFAULT '0' COMMENT '渠道ID',
  `module` varchar(100) DEFAULT NULL COMMENT '模块名',
  `submit_person` varchar(100) DEFAULT NULL COMMENT '提交人',
  `submit_date` datetime DEFAULT NULL COMMENT '提交日期',
  `check_person` varchar(100) DEFAULT NULL COMMENT '审核人',
  `check_date` datetime DEFAULT NULL COMMENT '审核日期',
  `table_name` varchar(256) NOT NULL COMMENT '数据表',
  `data_id` int(11) NOT NULL COMMENT '数据表ID',
  `op_type` int(5) DEFAULT NULL COMMENT '操作类型 1:新增 2:修改 3:删除',
  `status` int(5) DEFAULT NULL COMMENT '审核状态 1:待提交 2:已提交 3:已撤销 4:已审核 5:驳回 6:审核失败',
  `is_show` int(11) DEFAULT NULL COMMENT '是否显示 1表示显示 0 表示不显示',
  `remark` varchar(1024) DEFAULT NULL COMMENT '备注',
  `alter_person` varchar(100) DEFAULT NULL COMMENT '修改人',
  `alter_date` datetime DEFAULT NULL COMMENT '修改日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1118 DEFAULT CHARSET=utf8;

"""

"""
#2015-11-6
#jpush
-- ----------------------------
-- Table structure for cms_channel_jpush
-- ----------------------------
DROP TABLE IF EXISTS `cms_channel_jpush`;
CREATE TABLE `cms_channel_jpush` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_no` varchar(256) DEFAULT NULL COMMENT '渠道号',
  `channel_name` varchar(256) DEFAULT NULL COMMENT '渠道名',
  `app_key` varchar(500) DEFAULT NULL COMMENT '应用标识',
  `master_secret` varchar(500) DEFAULT NULL COMMENT 'master_secret',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;


#正式环境
-- ----------------------------
-- Records of cms_channel_jpush
-- ----------------------------
INSERT INTO `cms_channel_jpush` VALUES ('1', 'putao_live_01', '葡萄生活', '03a1bf5b006a01a692c575b4', '9e38f8e93b405e4542d9feff');
INSERT INTO `cms_channel_jpush` VALUES ('2', 'coolpad_ivvi_live_01', '', '', '');
INSERT INTO `cms_channel_jpush` VALUES ('3', 'coolpad_live_01', '酷派生活', '69fb0924ef453b694a91b57e', '17ce7c8ebf334ddd75c809ee');
INSERT INTO `cms_channel_jpush` VALUES ('4', 'haixin_live_01', '海信生活', '40c53ca22ea3f002abacadbc', '1288878b7d7b42d0a0967e51');
INSERT INTO `cms_channel_jpush` VALUES ('5', 'ivvi_live_01', 'ivvi生活', 'fe3827eff06db7e781a8ab55', 'fe26cdd7257db86aa7962596');
INSERT INTO `cms_channel_jpush` VALUES ('6', 'k_touch_live_01', '天语生活', 'e29dcbecdf989bff2772f763', '58bfd8a09b030a8b062a2726');
INSERT INTO `cms_channel_jpush` VALUES ('7', 'lenovo_live_01', '联想生活', '34d00f6f98093cf7e2de255c', '6e7957f5d417976e0a62b699');
INSERT INTO `cms_channel_jpush` VALUES ('8', 'lewa_live_01', '乐蛙生活', '4c5512a7eb33e4b6927991e1', 'd92cb1f3eb1309d259818b77');
INSERT INTO `cms_channel_jpush` VALUES ('9', 'yusun_live_01', '小辣椒生活', '0fbc82cd1500f382d0bbf2fd', '9d7e3452d794828cb0d4c59a');
INSERT INTO `cms_channel_jpush` VALUES ('10', 'zte_live_01', '中兴生活', 'd49f4253f7b20aa4400e4346', '7b561542fbeebdc1775a1287');

#测试环境
INSERT INTO `cms_channel_jpush` VALUES ('1', 'putao_live_01', '葡萄生活', '5e111aec05ad8a27b651624f', '423462d8a3880ce786765d6b');

"""

"""
#审核历史记录
CREATE TABLE `cms_check_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(45) NOT NULL,
  `check_person` varchar(100) NOT NULL,
  `check_date` varchar(45) NOT NULL,
  `type` varchar(1024) NOT NULL,
  `version` varchar(1024) NOT NULL,
  `channel_no` varchar(1024) NOT NULL,
  `module` varchar(45) NOT NULL,
  `submit_person` varchar(100) NOT NULL,
  `submit_date` varchar(45) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

"""
#2015-12-09
#版本
CREATE TABLE `cms_open_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#渠道
CREATE TABLE `cms_open_channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT '渠道名称',
  `app_version_id` int(11) NOT NULL COMMENT '版本ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`app_version_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;


#开放服务
CREATE TABLE `cms_open_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_id` int(11) NOT NULL,
  `show_name` varchar(256) DEFAULT NULL COMMENT '显示名称',
  `icon` varchar(256) NOT NULL COMMENT '显示图标',
  `city` varchar(256) NOT NULL DEFAULT '*',
  `distribute` int(11) NOT NULL DEFAULT '0' COMMENT '分发条件       0：无条件，1：时间条件，2：地域条件',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#开放服务和渠道的关系
CREATE TABLE `cms_view_open_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

"""
#发现页推送
CREATE TABLE `cms_view_push` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `channel_id` int(11) NOT NULL,
   `city` varchar(20) DEFAULT null COMMENT '城市',
   `data_version` int(11) DEFAULT null COMMENT '发送次数',
    PRIMARY KEY (`id`),
    UNIQUE KEY `channel_city` (`channel_id`,`city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

"""
#cpinfo
CREATE TABLE `cms_cpinfo` (
  `id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `icon` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
"""

"""
#v3.7新增数据结构
#品牌
CREATE TABLE `cms_cp` (
  `id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `name_style` varchar(256) DEFAULT NULL,
  `icon` varchar(256) NOT NULL,
  `adver_icon` varchar(256) NOT NULL,
  `desc` varchar(256) DEFAULT NULL,
  `desc_style` varchar(256) DEFAULT NULL,
  `action_id` int(11) DEFAULT NULL,
  `action_json` longtext,
  `search_keyword` longtext,
  `service_time` varchar(256) DEFAULT NULL,
  `shop_type` varchar(256) DEFAULT NULL,
  `company_name` varchar(256) DEFAULT NULL,
  `certified_company` int(11) DEFAULT NULL,
  `location2` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#品牌展示表
CREATE TABLE `cms_cpdisplay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location1` int(11) NOT NULL,
  `mark` varchar(256) DEFAULT NULL,
  `text` varchar(256) DEFAULT NULL,
  `meta_id` int(11) NOT NULL,
  `op_desc` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#品牌分类表
CREATE TABLE `cms_cp_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `location` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#品牌和品牌分类的关联表
CREATE TABLE `cms_view_cp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cp_category_id` int(11) NOT NULL,
  `cp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#首页品牌区表
CREATE TABLE `cms_home_cp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `cp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#活动表

CREATE TABLE `cms_activity_v37` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `action_id` int(11) NOT NULL,
  `action_json` mediumtext,
  `priority` int(11) NOT NULL,
  `valid_time` varchar(256) NOT NULL,
  `city` longtext NOT NULL,
  `img` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#活动和品牌的关联表
CREATE TABLE `cms_activity_cp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `cp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#活动和商品的关联表
CREATE TABLE `cms_activity_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activity_id` int(11) NOT NULL,
  `goods_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#渠道和活动的关联表
CREATE TABLE `cms_view_activity37` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `activity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#分类组
CREATE TABLE `cms_category_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `location` int(11) NOT NULL,
  `memo` varchar(256) DEFAULT NULL,
  `valid_time` varchar(256) NOT NULL,
  `city` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#分类组和分类的关联表
CREATE TABLE `cms_view_group_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#渠道和分类组关联表
CREATE TABLE `cms_view_channel_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#内容流组和品牌关联表
CREATE TABLE `cms_stream_cp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stream_id` int(11) NOT NULL,
  `cp_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#分类增加首页排序字段
ALTER TABLE `pt_cms_db`.`cms_navi_category` ADD COLUMN `location2` INT DEFAULT NULL AFTER `show_style`;
"""
"""
#增加功能类别
INSERT INTO `cms_category_group` VALUES ('1', '到家服务', '1', '到家服务类别', '* * * * *', '*');
INSERT INTO `cms_category_group` VALUES ('2', '功能服务', '2', '功能服务类别', '* * * * *', '*');
"""

"""
#2016-1-15
CREATE TABLE `op_goods_activity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `activityId` bigint(20) DEFAULT '0',
  `activityPrice` bigint(20) DEFAULT '0',
  `applyUser` varchar(100) DEFAULT '0',
  `commentCount` bigint(20) DEFAULT '0',
  `cpid` bigint(20) DEFAULT '0',
  `goodsId` bigint(20) DEFAULT '0',
  `gorder` bigint(20) DEFAULT '0',
  `orderCount` bigint(20) DEFAULT '0',
  `promotionMsg` varchar(256) DEFAULT NULL,
  `promotionType` bigint(20) DEFAULT '0',
  `activityBeginDate` timestamp NULL DEFAULT NULL,
  `activityEndDate` timestamp NULL DEFAULT NULL,
  `activityCity` text,
  `rawstring` text,
  `updateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

ALTER TABLE `cms_goods`  ADD  INDEX `index_cpname` (`cp_name`);
ALTER TABLE `pt_cms_db`.`cms_cp`  ADD  INDEX `index_name` (`name`);
cp表name也要加索引，要不然和goods表的name关联查询很慢
"""

"""
#分类增加底色字段
alter TABLE cms_navi_category ADD COLUMN background VARCHAR(256) DEFAULT null COMMENT '底色';

#加上新分类
ALTER TABLE `pt_cms_db`.`cms_goods`
ADD COLUMN `new_category` INT NULL DEFAULT NULL AFTER `cp_name`,
ADD COLUMN `new_second_category` INT NULL DEFAULT NULL AFTER `new_category`;

#加上分类类型，0是旧分类，1是新分类
ALTER TABLE `pt_cms_db`.`cms_navi_category`
ADD COLUMN `type` INT NOT NULL DEFAULT 0 AFTER `background`;

"""

"""
#添加运营标签
alter TABLE cms_goods add column `mark` varchar(256) DEFAULT NULL COMMENT '运营标签';
alter TABLE cms_streamcontentbeans add column `mark` varchar(256) DEFAULT NULL COMMENT '运营标签';
"""


def modify_actionjson(request):
    objs = CmsCP.objects.all()
    for obj in objs:
        if obj.action_id:
            setCpAction(obj.id, obj.action_id)
    return HttpResponse(0)


"""
#添加cpdisplay字段
ALTER TABLE cms_cpdisplay ADD COLUMN parent_id int(11) NOT NULL DEFAULT 1;
"""

"""
#分享券
CREATE TABLE `cms_share_coupon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_type` int(11) NOT NULL,
  `dialog_title` varchar(256) NOT NULL DEFAULT '分享得现金券' COMMENT '弹窗标题',
  `dialog_content` varchar(256) NOT NULL DEFAULT '恭喜您获得现金券分享机会，分享给好友，领现金券' COMMENT '弹窗内容',
  `dialog_img` varchar(256) DEFAULT NULL,
  `button_name` varchar(256) NOT NULL DEFAULT '分享现金券' COMMENT '按钮名称',
  `action_type` int(11) NOT NULL DEFAULT '0' COMMENT '动作类型, 0：分享；1：跳转到指定页面',
  `share_imgurl` varchar(256) NOT NULL COMMENT '分享默认图',
  `share_title` varchar(256) NOT NULL COMMENT '分享标题',
  `share_content` varchar(256) DEFAULT NULL COMMENT '分享描述-内容',
  `share_url` varchar(256) NOT NULL COMMENT '分享链接',
  `action_id` int(11) NOT NULL,
  `action_json` varchar(256) DEFAULT NULL,
  `times_limit` int(11) DEFAULT '-1' COMMENT '每天次数限制，无限制为-1，',
  `start_time` int(11) DEFAULT NULL,
  `end_time` int(11) DEFAULT NULL,
  `city` varchar(256) NOT NULL DEFAULT '*',
  `show_style` int(11) NOT NULL DEFAULT '0' COMMENT '显示形式 0:仅出现在入口；1：出现在弹出和入口',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


ALTER TABLE `cms_share_coupon`
CHANGE COLUMN `share_imgurl` `share_imgurl` VARCHAR(256) NULL COMMENT '分享默认图' ,
CHANGE COLUMN `share_title` `share_title` VARCHAR(256) NULL COMMENT '分享标题' ,
CHANGE COLUMN `share_url` `share_url` VARCHAR(256) NULL COMMENT '分享链接' ,
CHANGE COLUMN `action_id` `action_id` INT(11) NULL ;



#分享券和渠道关联表
CREATE TABLE `cms_view_share_coupon` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `channel_id` INT NOT NULL,
  `share_coupon_id` INT NOT NULL,
  PRIMARY KEY (`id`));
  """
