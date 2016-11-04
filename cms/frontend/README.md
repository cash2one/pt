## 前端开发记录

### 1.日期选择器

+   依赖: [jQuery](http://jquery.com/)
+   [online demo](https://jsfiddle.net/Jogiter/bwmubsa3/)



html: 具体参考[官网demo](https://github.com/CuriousSolutions/DateTimePicker/tree/gh-pages)

```html
<!-- 需要使用的地方添加，代码如下 -->
<input type="text" data-field="datetime"/>

<!-- '</body>'标签之前添加，初始化datetimepicker的容器  -->
<div id="dtBox"></div>
```

初始化：

```js
$("#dtBox").DateTimePicker({
    dateSeparator: '/',
    dateTimeFormat: 'yyyy/MM/dd HH:mm',
    dateFormat: 'yyyy/MM/dd',
    isPopup: true,
    language: 'zh-CN',
    titleContentDate: '设置日期',
    titleContentTime: '设置时间',
    titleContentDateTime: '设置日期&时间',
    shortDayNames: '星期日_星期一_星期二_星期三_星期四_星期五_星期六'.split('_'),
    fullDayNames: '星期日_星期一_星期二_星期三_星期四_星期五_星期六'.split('_'),
    shortMonthNames: '01_02_03_04_05_06_07_08_09_10_11_12'.split('_'),
    fullMonthNames: '01_02_03_04_05_06_07_08_09_10_11_12'.split('_'),
    setButtonContent: '设置',
    clearButtonContent: '清除',
    addEventHandlers: function()
    {
        var dtPickerObj = this;
        $(window).resize(function() {
            dtPickerObj.setIsPopup(true);
        });
    }
});
```

### 2.图片选择器

TODO：