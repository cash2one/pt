/**
 * Created by Administrator on 2015/8/25 0025.
 */

//得到url传过来的参数
function getURLParam(arg)
{
    var re = new RegExp("[&,?]" + arg + "=([^\\&]*)", "i");
    var a = re.exec(location.search);
    if (a == null)
        return "";
    return a[1];
}

//给url添加一个参数，arg是参数名称，arg_val是参数的值
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

function getIndex(arr, key)
{
    for(var i in arr)
    {
        if(arr[i] == key)
            return i;
    }
    return -1;
}


String.prototype.format= function()
{
    var args = arguments;
    return this.replace(/\{(\d+)\}/g,function(s,i)
    {
        return args[i];
    });
};

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


function getImgURL(url)
{
    if(!url || url.indexOf("http://") == 0 || url.indexOf("https://") == 0)
        return url;
    else
        return "http://m.putao.cn/images/" + url + ".png"
}

    $(document).ready(function(){
        //点击图片自动放大功能
            var dialogstr='<div class="modal fade" id="myModal_img" tabindex="-1" ' +
                'role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div ' +
                'class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" ' +
                'aria-hidden="true">&times;</button> <h4 class="modal-title" id="myModalLabel" style="text-align: center">大图预览</h4> </div> <div ' +
                'class="modal-body" style="text-align: center"> <p><img src="" style="width:auto;max-width:100%"><p></div></div></div></div>';
            $(dialogstr).appendTo('article');
            $('table').on('click',function(event){
                if(event.target.nodeName.toLowerCase()=='img'){
                    var imgsrc=$(event.target).attr('src');
                    $("#myModal_img").find('img').attr('src',imgsrc);
                    //console.log("我被点击了");
                }
            })
    });


$(document).ready(function(){
    var backtop='<div class="back-to-top"><a class="tap-btn"><i>⇧</i></a></div>';
    $(backtop).appendTo('article');

    $(window).scroll(function(){
        if($(window).scrollTop()>80){
            $(".back-to-top").fadeIn(1500);
        }else {
            $(".back-to-top").fadeOut(1000);
        }
    });
    $(".back-to-top").on('click',function(){
        $(window).scrollTop(0);
    });
});

function reload(){
     window.location.reload();
  }

function checkJson(obj){
    if(obj && obj.indexOf(":")>=0 && obj.indexOf("{")>=0 && obj.indexOf("}")>=0){
        obj=JSON.parse(obj);
        var is_json = (typeof(obj) == "object") && (Object.prototype.toString.call(obj).toLowerCase() == "[object object]") && !obj.length;
        //console.log("成功进入程序转化");
        return is_json;
    }else{
        return false;
    }
}

//隐藏交换顺序按钮
function hideExhangeIcon() {
    $(".edit-td").each(function () {
        //var data_status = this.dataset.status;
        //console.log(data_status);
        //console.log($(this).parent("tr").prev().find("td.edit-td").data("status"));
        if ($(this).parent("tr").prev().find("td.edit-td").data("status") == 0) {
            $(this).find(".glyphicon-arrow-up").hide();
        }
        if ($(this).parent("tr").next().find("td.edit-td").data("status") == 0) {
            $(this).find(".glyphicon-arrow-down").hide();
        }
    });
}
