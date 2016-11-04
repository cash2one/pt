/**
 * Created by sunq on 16/6/11.
 */


var myTable;
$(function () {
    init();
    myTable = new tableInit({});
    myTable.getData();
    /*绑定搜索部分功能*/
    myTable.searchInit();
});
var data = {
    category_indexs: [],
}
var vm = new Vue({
    el: '#category_index',
    data: data,
    methods: {
        delete: function (id, index) {
            if (confirm("确定删除分类首页?")) {
                var that = this;
                $.ajax({
                    url: "/main/delete_category_index/",
                    data: {id: id},
                    type: "get",
                    dataType: "json",
                    success: function (data) {
                        if (data.code == 0) {
                            that.category_indexs.splice(index, 1)
                        } else {
                            alert(data.msg)
                        }

                    }, error: function (req) {
                        console.log(req.statusText)
                    }
                })
            }

        }
    }
});

function init() {
    /*初始化页面*/
    setNavBg("category");
}
function requestData(options) {
    $.ajax({
        url: "/main/search_category_index/",
        type: "get",
        cache: false,
        data: {
            key: $("#" + options.keyword).val(),
            cur_page: options.curPage,
            per_page: options.pageSize
        },
        beforeSend: function (XMLHttpRequest) {
            $("#" + options.loadImgId).show();
            $("#pagination").hide();
        },
        success: function (result) {
            //console.log(result);
            var data = eval(result)[0], num_pages = eval(result)[1];
            if (data.length == 0) {
                $('#' + myTable.default.tbodyId).empty();
                $("#pagination").hide();
                $(".no_content").show();
                $(".my_thead").hide();
            }
            else {
                $(".no_content").hide();
                dataInit(data)
                $(".my_thead").show();
                myTable.processData(data);
                if (num_pages >= 2) myTable.pageInit(num_pages);
            }
        },
        error: function (result) {
            console.log(result);
        },
        complete: function (result) {
            $("#" + options.loadImgId).hide();
            var currentpage = options.curPage - 1;
            $(options.pageSelector).eq(currentpage).css('background', '#34cb95');
            if (currentpage > 5) {
                $(options.pageSelector).eq(currentpage - 5).prevAll().hide();
            }
        }
    })
}
/*处理后台返回数据*/
function dataInit(data_s) {
    Vue.set(data, 'category_indexs', data_s)
}