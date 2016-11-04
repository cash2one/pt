                    __
                   /\ \
         _____     \_\ \ __
        /\ '__'\ /\_\_\ \\_\
        \ \ \L\ \    \_\ \  __     __
         \ \ ,__/     \_\ \____\  /\_\
          \ \ \/       \_\__\__/  \/_/
           \ \_\
            \/_/

---

### 前端添加页面示例
1.cms/urls/url.py 的urlpatterns中定义一个url。详细说明见代码注释
2.定义的url中的template_name为对应的静态html位置

### 模板中json_load
1.在html顶部加入 {% load pt %}
2.{% 变量参数|pt_json %} ：load变量json串
3.{% 变量参数|pt_dumps %} ：dumps变量成json

### 代码结构
├─cms
│  ├─activity
│  ├─cms
│  ├─common
│  ├─config
│  │  ├─apis
│  │  ├─migrations
│  │  └─views
│  ├─main
│  │  ├─migrations
│  │  ├─model
│  │  ├─template_tag
│  │  └─views
│  ├─pt_open
│  ├─tools
│  └─urls
├─conf
├─docs
│  ├─古物
│  └─接口文档
└─frontend
    ├─static
    │  ├─css
    │  ├─fonts
    │  ├─images
    │  └─js
    │      ├─city
    │      ├─cms
    │      │  └─category
    │      └─switch
    │          ├─css
    │          └─js
    └─templates
        ├─actions
        ├─activities
