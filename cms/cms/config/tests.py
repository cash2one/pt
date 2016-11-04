#coding=utf-8
import jpush
import json
import time
app_key = "5e111aec05ad8a27b651624f"
master_secret = "423462d8a3880ce786765d6b"

def jpush_foundpage(channel_no,version,id,title,city):
    cities = city.split(",")
    new_cities = []
    for city in cities:
        if len(city)>2 and city[-1] in ["市","县"]:
            city = city[:-1]
        new_cities.append(city)
    cities = new_cities
    version = "Putao_" + version.replace(".","_")
    app_key = "5e111aec05ad8a27b651624f"
    master_secret = "423462d8a3880ce786765d6b"
    _jpush = jpush.JPush(app_key,master_secret)
    push = _jpush.create_push()
    push.platform = jpush.all_
    for i in range(0,len(cities),20):
        city = cities[i:i+20]
        msg_time = int(time.time())
        city_list=[]
        # push.audience = jpush.all_
        if "*" in city:
            push.audience = jpush.audience(
                jpush.tag(channel_no,version)
            )
        else:
            push.audience = jpush.audience(
                jpush.tag(*city),
                jpush.tag_and(channel_no,version)
            )
            city_list=city
        # push.notification = jpush.notification(alert="new found page")

        messages = {
            "version": 1,
            "data": [
                {
                    "msg_digest": title,
                    "msg_type": 10,
                    "msg_subject": title,
                    "msg_id": id,
                    "is_notify": 0,
                    "msg_expand_param": {
                        "tab_index":1,
                        "city_list":city_list
                    },
                    "msg_time": msg_time,
                    "msg_product_type": "0"
                }
            ]
        }
        push.message = {
            "msg_content":json.dumps(messages)
        }
        push.send()

city1="上海市,天津市,长沙市,株洲市,湘潭市,衡阳市,邵阳市,岳阳市,常德市,张家界市,益阳市,永州市,怀化市,娄底市,湘西,南京市,无锡市,徐州市,常州市,苏州市,南通市,连云港市,淮安市,盐城市,扬州市,镇江市,泰州市,宿迁市,深圳"
city2="*"
jpush_foundpage("putao_live_01","3.2.0",15,"guangjie",city1)