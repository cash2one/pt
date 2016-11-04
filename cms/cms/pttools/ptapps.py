# -*- coding: utf-8 -*-
# Author:songroger
# Jun.27.2016
import random
import string
from math import radians, atan, tan, sin, acos, cos

originCode = string.ascii_uppercase + string.digits


def code_gen(length=7):
    string = ''
    for index in range(length):
        string += random.choice(originCode)
    return string


def check_range(pt, poly):
    '''
    point_list = [{'lat':1, 'lng':1},{'lat':1, 'lng':4},
    {'lat':3, 'lng':7},{'lat':4, 'lng':4},{'lat':4, 'lng':1}]
    print check_range({'lat':2, 'lng':5}, point_list)
    '''
    c = False
    i = -1
    l = len(poly)
    j = l - 1
    while i < l - 1:
        i += 1
        if ((poly[i]["lat"] <= pt["lat"] and pt["lat"] < poly[j]["lat"]) or (poly[j]["lat"] <= pt["lat"] and pt["lat"] < poly[i]["lat"])):
            if (pt["lng"] < (poly[j]["lng"] - poly[i]["lng"]) * (pt["lat"] - poly[i]["lat"]) / (poly[j]["lat"] - poly[i]["lat"]) + poly[i]["lng"]):
                c = not c
        j = i
    return c


def calc_distance(lat_a, lng_a, lat_b, lng_b):
    """
    通过经纬度计算两个位置之间的距离，返回单位：米
    """
    if abs(lat_a - lat_b) < 0.0000000001 and abs(lng_a - lng_b) < 0.0000000001:
        return 0

    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    rad_lat_a = radians(lat_a)
    rad_lng_a = radians(lng_a)
    rad_lat_b = radians(lat_b)
    rad_lng_b = radians(lng_b)
    pA = atan(rb / ra * tan(rad_lat_a))
    pB = atan(rb / ra * tan(rad_lat_b))
    xx = acos(sin(pA) * sin(pB) + cos(pA) *
              cos(pB) * cos(rad_lng_a - rad_lng_b))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr) * 1000
    return distance


def safe_distance(lat1, lng1, lat2, lng2):
    """
    安全计算距离，参数非浮点型将返回0，有一组经纬度为(0，0)时也返回0
    :param lat1:
    :param lng1:
    :param lat2:
    :param lng2:
    :return: 地球两点之间的距离
    """
    if not isinstance(lat1, float) \
            or not isinstance(lng1, float) \
            or not isinstance(lat2, float) \
            or not isinstance(lng2, float) \
            or (lat1 == 0 and lng1 == 0) \
            or (lat2 == 0 and lng2 == 0):
        return 0
    return int(calc_distance(lat1, lng1, lat2, lng2))
