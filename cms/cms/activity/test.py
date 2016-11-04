# -*- coding: utf-8 -*-
# Author:songroger
# Jul.15.2016
from django.db import connections


def get_count_dict(cids):
    data = {}
    data["used_count"] = {}
    data["coupon_count"] = {}
    c_sql = """
    SELECT cid,
           SUM(CASE WHEN STATUS = 0 OR 1 THEN 1 ELSE 0 END) AS TOTAL_COUNT,
           SUM(CASE WHEN STATUS = 1 THEN 1 ELSE 0 END) AS USED_COUNT
    FROM coupon_allot
    WHERE cid IN (%s)
    GROUP BY cid;
    """
    print c_sql % ','.join(map(lambda x: str(x), cids))
    cur = connections['activity'].cursor()
    cur.execute(c_sql, ','.join(map(lambda x: str(x), cids)))
    row = cur.fetchall()
    for r in row:
        data["used_count"].update({r[0]: r[2]})
        data["coupon_count"].update({r[0]: r[1]})
    return data


if __name__ == '__main__':
    data = get_count_dict([10351, 10355])
    print data
