/**
 * Created by Administrator on 2015/9/23 0023.
 */
function tableInit(options){
    this.default = $.extend({
        curPage : 1,
        pageSize : 20,
        keyword : $("#search").val(),
        loadImgId : 'loading',
        pageSelector : '.pagelist li',
        pageContainer :'pagination',
        tbodyId : 'tbody'
    },options)
}
tableInit.prototype.getData = function(){
    requestData(this.default);
};
tableInit.prototype.processData = function(data){
    var tbodyId = this.default.tbodyId,htmlStr='';
    if(data.length == 0) return ;
    $.each(data,function(i,value){
       /* if(value[0] ==1) htmlStr+='<tr class="level2">'
        else */htmlStr+='<tr>';
        $.each(value,function(j,ele){
            if(j == value.length - 1){
                htmlStr += '<td><span class="glyphicon glyphicon-edit" aria-hidden="true" style="margin-right:10px;cursor: pointer"></span><span class="glyphicon glyphicon-trash" aria-hidden="true" style="cursor: pointer"></span></td>';
            }
            else{
                htmlStr +='<td>'+ele+'</td>';
            }
        })
        htmlStr+='</tr>';
    });
    $('#'+tbodyId).empty().append($(htmlStr)).on("click",'.glyphicon-edit',function(){
        alert("editPage");
    }).on("click",'.glyphicon-trash',function(){
        alert("deletePage");
    });
};
tableInit.prototype.pageInit = function(pages){
    var pageContainer = $("#"+this.default.pageContainer).empty(),
        ul = $("<ul class='pagination'>"),
        curpage = this.default.curPage,
        that = this;

    /*添加首页*/
    $(" <li  class='pagefirst'><a href='javascript:void(0)'>首页</a></li>").appendTo(ul);    
    /*添加第一页*/
    if(curpage>1)
        $(" <li  class='pagepre'><a href='javascript:void(0)'>上一页</a></li>").appendTo(ul);
    /*添加省略号*/
    if(curpage>5 && curpage!=6)
        $(" <li><a href='javascript:void(0)' style='cursor:not-allowed'>......</a></li>").appendTo(ul);
    /*添加每一页*/
    var pageDiv = $("<div class='pagelist pagenavigate'></div>");
    for(var i = 1; i <= pages; i++)
    {
        var li = $(" <li><a href='javascript:void(0)'>"+i+"</a></li>");
        li.appendTo(pageDiv);
        pageDiv.appendTo(ul)
    }
    if(pages>10 && curpage <= pages-5)
        $(" <li><a href='javascript:void(0)' style='cursor:not-allowed'>"+"......"+"</a></li>").appendTo(ul);
    /*添加下一页*/
    if(curpage<pages)
        $(" <li  class='pagenext'><a href='javascript:void(0)'>下一页</a></li>").appendTo(ul);

    /*添加最后一页*/
    $(" <li  class='pagelast'><a href='javascript:void(0)'>尾页</a></li>").appendTo(ul);

    /*添加到页面节点*/
    pageContainer.append(ul);

    $(".pagelist.pagenavigate",pageContainer).on("click","li", function(){
        that.default.curPage = parseInt($(this).text());
        requestData(that.default);
    });

    $('.pagepre').one('click', function(event) {    //上一页
        that.default.curPage = curpage-1;
        if(that.default.curPage > 0)
            requestData(that.default);
    });
    $('.pagenext').one('click', function(event) {   //下一页
        that.default.curPage = curpage+1;
        if(that.default.curPage <= pages)
            requestData(that.default);
    });
    $(".pagefirst",pageContainer).click(function(){
        that.default.curPage = 1;
        requestData(that.default);
    });
    $(".pagelast",pageContainer).click(function(){
        that.default.curPage =pages;
        requestData(that.default);
    })

}