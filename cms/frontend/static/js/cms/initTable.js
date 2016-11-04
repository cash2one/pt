/**
 * Created by Administrator on 2015/9/23 0023.
 */
function tableInit(options) {
    this.default = $.extend({
        curPage: 1,
        pageSize: 20,
        keyword: 'search',
        loadImgId: 'loading',
        pageSelector: '.pagelist li',
        pageContainer: 'pagination',
        tbodyId: 'tbody',
        searchBtn: 'search-btn',
        clearInput: 'clearInput'
    }, options)
}
tableInit.prototype.getData = function () {
    requestData(this.default);
};
tableInit.prototype.processData = function (data) {
    dataInit(data);
    hideExhangeIcon();
    checkAuthority();
};
tableInit.prototype.pageInit = function (pages) {
    var pageContainer = $("#" + this.default.pageContainer).empty().show(),
        ul = $("<ul class='pagination'>"),
        curpage = this.default.curPage,
        that = this;

    /*添加首页*/
    $(" <li  class='pagefirst'><a href='javascript:void(0)'>首页</a></li>").appendTo(ul);
    /*添加第一页*/
    if (curpage > 1)
        $(" <li  class='pagepre'><a href='javascript:void(0)'>上一页</a></li>").appendTo(ul);
    /*添加省略号*/
    if (curpage > 5 && curpage != 6)
        $(" <li><a href='javascript:void(0)' style='cursor:not-allowed'>......</a></li>").appendTo(ul);
    /*添加每一页*/
    var pageDiv = $("<div class='pagelist pagenavigate'></div>");
    for (var i = 1; i <= pages; i++) {
        var li = $(" <li><a href='javascript:void(0)'>" + i + "</a></li>");
        li.appendTo(pageDiv);
        pageDiv.appendTo(ul)
    }
    if (pages > 10 && curpage <= pages - 5)
        $(" <li><a href='javascript:void(0)' style='cursor:not-allowed'>" + "......" + "</a></li>").appendTo(ul);
    /*添加下一页*/
    if (curpage < pages)
        $(" <li  class='pagenext'><a href='javascript:void(0)'>下一页</a></li>").appendTo(ul);

    /*添加最后一页*/
    $(" <li  class='pagelast'><a href='javascript:void(0)'>尾页</a></li>").appendTo(ul);

    /*添加到页面节点*/
    pageContainer.append(ul);

    $(".pagelist.pagenavigate", pageContainer).on("click", "li", function () {
        that.default.curPage = parseInt($(this).text());
        requestData(that.default);
    });

    $('.pagepre').one('click', function (event) {    //上一页
        that.default.curPage = curpage - 1;
        if (that.default.curPage > 0)
            requestData(that.default);
    });
    $('.pagenext').one('click', function (event) {   //下一页
        that.default.curPage = curpage + 1;
        if (that.default.curPage <= pages)
            requestData(that.default);
    });
    $(".pagefirst", pageContainer).click(function () {
        that.default.curPage = 1;
        requestData(that.default);
    });
    $(".pagelast", pageContainer).click(function () {
        that.default.curPage = pages;
        requestData(that.default);
    })
};
tableInit.prototype.searchInit = function () {
    var that = this;
    $('.' + this.default.searchBtn).on('click', function () {
        requestData(that.default);
    });
    $("#" + that.default.keyword).keydown(function (e) {
        var e = e || event, keycode = e.keyCode || e.which;
        if (keycode == 13) {
            $('.' + that.default.searchBtn).click();
        }
    })
    $('.' + this.default.clearInput).on('click', function () {
        $("#" + that.default.keyword).val('');
        requestData(that.default);
    })
}

