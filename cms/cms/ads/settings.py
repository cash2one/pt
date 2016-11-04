# -*- coding: utf-8 -*-
# Author:songroger
# Aug.31.2016
COVER_ADS_PARAMETERS = ["name", "logo", "start_time",
                        "end_time", "display_time", "city_names"]

# 1为开发环境
# 2为正式环境
# 3为COPY测试环境
REQ_ENV = 2

GET_BOUGHT_URL = {1: "http://api.test.putao.so/spay/daojia/order/queryUserBuyGoods?pt_token=%s",
                  2: "http://api.putao.so/spay/daojia/order/queryUserBuyGoods?pt_token=%s",
                  3: "http://api.copy.putao.so/spay/daojia/order/queryUserBuyGoods?pt_token=%s"}


GET_GOODS_INFO = {1: "http://api.test.putao.so/sopen/openGoods/queryGoodsPromotionPrice",
                  2: "http://api.putao.so/sopen/openGoods/queryGoodsPromotionPrice",
                  3: "http://api.copy.putao.so/sopen/openGoods/queryGoodsPromotionPrice"}


GET_GOODS_PROMOTION = {1: "http://open.test.putao.so/openGoods/queryGoodsInfoForSearch",
                       2: "http://api.putao.so/sopen/openGoods/queryGoodsInfoForSearch",
                       3: "http://open.copy.putao.so/openGoods/queryGoodsInfoForSearch"}
