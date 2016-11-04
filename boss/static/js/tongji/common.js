/**
 * Created by Administrator on 2015/6/26 0026.
 */

/**
 * 字符串格式化
 * {0},{1},hehe".format(["hello","world"]); hello,world,hehe
 * 数学={shuxue},语文={yuwen}".format({"shuxue":100,"yuwen":95});//数学=100,语文=95
 */

var DEBUG = true;

String.prototype.format= function()
{
    var args = arguments;
    return this.replace(/\{(\d+)\}/g,function(s,i)
    {
        return args[i];
    });
};

//给当前窗口url增加一个参数
function addURLParam(url, arg, arg_val)
{
    var pattern = arg + '=([^&]*)';
    var replaceText = arg + '=' + arg_val;
    if(url.match(pattern))
    {
        var tmp = '/(' + arg + '=)([^&]*)/gi';
        tmp = url.replace(eval(tmp), replaceText);
        return tmp;
    }
    else
    {
        if(url.match('[\?]'))
        {
            return url + '&' + replaceText;
        }else{
            return url + '?' + replaceText;
        }
    }
}

//得到url传过来的参数
function getURLParam(arg)
{
    var re = new RegExp("[&,?]" + arg + "=([^\\&]*)", "i");
    var a = re.exec(location.search);
    if (a == null)
        return "";
    return a[1];
}

//举例：'2015-1-1'  -2，返回 2014-12-30
function getDateStr(datestr, delay)
{
    var d = new Date(datestr);
    d.setDate(d.getDate() + delay);
    var year = d.getFullYear();
    var month = d.getMonth() + 1;
    var day = d.getDate();

    if(month < 10)
      month = "0" + month;
    if(day < 10)
      day = "0" + day;

    return year + "-" + month + "-" + day;
}

//获取两个时间的间隔天数
//sDate1和sDate2是2002-12-18格式
function getDateDiff(start_str, end_str)
{
    var arr_date, start_date, end_date, ret;

    arr_date = start_str.split("-");
    start_date = new Date(arr_date[1] + '-' + arr_date[2] + '-' + arr_date[0]); //转换为12-18-2002格式
    arr_date = end_str.split("-");
    end_date = new Date(arr_date[1] + '-' + arr_date[2] + '-' + arr_date[0]);
    ret = parseInt(Math.abs(start_date - end_date) / 1000 / 60 / 60 / 24); //把相差的毫秒数转换为天数
    return ret + 1
}

//显示加载图标
var loading = (function(){
    var gif_selector, div_selector;
    return {
        init: function(g, d)
        {
            gif_selector = g;
            div_selector = d;
        },
        show: function(){
            var margin_top = $(div_selector).height() / 2 + 40;
            if(margin_top > 300)
                margin_top = 300;
            $(gif_selector).css("margin-top", margin_top + "px").show();
        },
        hide: function(){
            $(gif_selector).hide();
        }
    }
})();


function postJSON(path, data, succ_func, complete_func){
    var argc = arguments.length;
    $.ajax(path, {
        type: "POST",
        cache: false,
        data: data,
        beforeSend:function(XMLHttpRequest){
            //alert('远程调用开始...');
            loading.show();
         },
        success: function(data){
            if(argc >= 3)
                succ_func(data);
        },
        complete: function (){
            loading.hide();
            if(argc >= 4)
                complete_func();
        },
        error: function(data){
            if(DEBUG)
                console.log(data);
        }
    })
}

//django  csrf
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function scrollup(){
    var e = $("#scrollUp");
    e.fadeOut(0);
    $(window).scroll(function(){  //只要窗口滚动,就触发下面代码
        var scrollt = document.documentElement.scrollTop + document.body.scrollTop; //获取滚动后的高度
        if( scrollt > 200 ){  //判断滚动后高度超过200px,就显示
            e.fadeIn(400); //淡出
        }else{
            e.stop().fadeOut(400); //如果返回或者没有超过,就淡入.必须加上stop()停止之前动画,否则会出现闪动
        }
    });
//    e.click(function(){ //当点击标签的时候,使用animate在300毫秒的时间内,滚到顶部
//        $("html,body").animate({scrollTop:"0px"},100);
//    });
}

function arr2str(arr)
{
    if(arr)
        return new String(arr);
    else
        return "";
}

//二维数组进行排序
//field是数组坐标，按照第几列排序
function listSort(arr, field, order, type) {
    //不能用冒号:  以免和时长中的冒号重复。且尽量用小的ascii字符，因为它也会参与排序
    var split = "\t";

    function sortNumber(a, b)
    {
        var c = a.split(split)[0];
        var d = b.split(split)[0];
        //如果是None，则把它作为最小值
        if(c == "--") return -1;
        if(d == "--") return 1;
        //parseInt("34aa")  --->  34
        //以防后面一些带有百分比的情况
        var e = parseInt(c);
        var f = parseInt(d);
        return e - f;
    }

    var refer = [], result = [], order = order == 'asc' ? 'asc' : 'desc', index;
    for (var i = 0; i < arr.length; i++) {
        refer[i] = arr[i][field] + split + i;
    }
    //默认不按照数值的大小对数字进行排序，要实现这一点，就必须使用一个排序函数
    if(type == "int")
        refer.sort(sortNumber);
    else
        refer.sort();

    if (order == 'desc')
    {
        if(type == "int")
            refer.reverse(sortNumber);
        else
            refer.reverse();
    }
    for(var i = 0; i < refer.length; i++)
    {
        index = refer[i].split(split)[1];
        result[i] = arr[index];
    }
    return result;
}

//获取某个元素在一维数组里的坐标
function getIndex(arr, key)
{
    for(var i in arr)
    {
        if(arr[i] == key)
            return i;
    }
    return -1;
}

//获取某个元素在二维数组里的坐标
function get2Index(arr, key)
{
    for(var i in arr)
    {
        if(arr[i][0] == key)
            return i;
    }
    return -1;
}

function setRadio(radioName, radiovalue)
{
    var obj = document.getElementsByName(radioName);
    for(var i = 0; i < obj.length; i++)
    {
        if(obj[i].value == radiovalue)
        {
            obj[i].checked = true;
            return;
        }
    }
}

/*
*  方法:Array.remove(dx) 通过遍历,重构数组
*  功能:删除数组元素.
*  参数:dx删除元素的下标.
*/
//Array.prototype.remove = function(dx)
//{
//    if(isNaN(dx) || dx >= this.length)
//    {
//        return false;
//    }
//    for(var i = 0, n = 0; i < this.length; i++)
//    {
//        if(this[i] != this[dx])
//        {
//            this[n++] = this[i]
//        }
//    }
//    this.length -= 1;
//};

function arrRemove(arr, dx)
{
    if(isNaN(dx) || dx >= arr.length)
    {
        return false;
    }
    for(var i = 0, n = 0; i < arr.length; i++)
    {
        if(arr[i] != arr[dx])
        {
            arr[n++] = arr[i]
        }
    }
    arr.length -= 1;
}

//没有就放进去，有就把它删除
function mypush(arr, val)
{
    for(var i in arr)
    {

        if(arr[i] == val)
        {
            arrRemove(arr, i);
            return;
        }
    }
    arr.push(val);
}

//val 是个字典，判断name是否相同
//有就放进去，没有就删除
function mydictpush(arr, val)
{
    for(var i in arr)
    {

        if(arr[i]["name"] == val["name"])
        {
            arrRemove(arr, i);
            return;
        }
    }
    arr.push(val);
}

function getMatrix(arrs, index)
{
    var ret = [];
    for(var i in arrs)
    {
        ret.push(arrs[i][index]);
    }
    return ret;
}

function getHeadDate(arr)
{
    var temp = [];
    for(var i in arr)
    {
        if(arr[i].constructor ==  String)
            temp[i] = (arr[i]).substr(0,10).replace(/-/g, "");
        else
            temp[i] = arr[i];
    }
    return temp;
}

//设置左边导航栏
function setLeftNav(i,j)
{
    var subindex = j||0;
    $(".well .nav > li").removeClass("nav-active").eq(i).addClass("active")
        .find("li").removeClass("current")
        .eq(subindex).addClass("current");
}

//设置左边导航栏
function setTopNav(i,j)
{
    var subindex = j||0;
    $(".well .nav > li").removeClass("nav-active").eq(i).addClass("active")
        .find("li").removeClass("current")
        .eq(subindex).addClass("current");
    $(".well .nav > li.active > a").clone().appendTo(".secondNav h1");
    if( $(".well .nav > li.active a").length > 2){
        $(".well .nav > li.active").children(".subnav-warp").find("a").each(function(m,ele){
            console.log($(this))
            $("<h2></h2>").append($(this).clone()).appendTo(".secondNav");
        })
        $(".secondNav h2 a").eq(subindex).addClass("current");
    }
}

function initNav()
{
    //根据app参数，初始化左边导航栏各href
    $(".nav-list a").each(function()
    {
        var app = getURLParam("app");
        if(app)
        {
            var new_href = addURLParam($(this).attr("href"), "app", app);
            $(this).attr("href", new_href);
        }
    });
/*
    $(".nav-header").click(function(){
        $(".nav-list li").hide();
        $(".nav-list .nav-header").show();
        $(this).nextUntil(".nav-header").show();
    });
    */
}

//模态框居中对齐
function centerModals(){
    function __() {
        $('.modal').each(function (i) {
            var $clone = $(this).clone().css('display', 'block').appendTo('body');
            var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
            top = top > 0 ? top : 0;
            $clone.remove();
            $(this).find('.modal-content').css("margin-top", top);
        });
    }
    $('.modal').on('show.bs.modal', __);
    $(window).on('resize', __);
}

//初始化全局应用选择框
function initGlobalApps()
{
    $("#global_apps option[value='{0}']".format(getURLParam("app"))).attr("selected","selected");
    $("#global_apps").chosen({
        no_results_text: "Oops, nothing found!",//搜索不到的提示语
        search_contains: true,//可以让chosen搜索选项的中间字符
        width: "300px"
    }).change(function(){
        location.search = addURLParam(location.search, "app", this.value);
    });
}

$(document).ready(function()
{
    initGlobalApps();
    scrollup();
    //initNav();
    centerModals();
});