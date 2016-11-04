 function pagination(pages)
 {
   var ul = $("<ul>");
   $("#pagination ul").remove();
   if (pages == 1)
    {
      $("#pagination").css(  "display","none");
    }
   else
      {
   $("#pagination").css( "display","block");
      };
          ul.appendTo("#pagination");
   $(ul).addClass('pagination');

     for(var i = 1; i <= 1; i++)
     {
        var li = $(" <li  class='pagefirst'><a href='javascript:void(0)' onclick='requestData(" + i + ")'>"+"首页"+"</a></li>");
           li.appendTo(ul);
     }
        var li = $(" <li  class='pagepre'><a href='javascript:void(0)'>"+"上一页"+"</a></li>");
           if(g_cur_page>1)
           li.appendTo(ul);
        var li = $(" <li><a href='javascript:void(0)' style='cursor:not-allowed'>"+"......"+"</a></li>");
     if(g_cur_page>5 && g_cur_page!=6)
           li.appendTo(ul);
        var pageDiv = $("<div class='pagelist pagenavigate'></div>");
       for(var i = 1; i <= pages; i++)
      {
           var li = $(" <li><a href='javascript:void(0)' onclick='requestData(" + i + ")'>"+i+"</a></li>");
              li.appendTo(pageDiv);
              pageDiv.appendTo(ul)
      }
           var li = $(" <li><a href='javascript:void(0)' style='cursor:not-allowed'>"+"......"+"</a></li>");
       if(pages>10 && g_cur_page <= pages-5)                                              
          li.appendTo(ul);
       var li = $(" <li  class='pagenext'><a href='javascript:void(0)'>"+"下一页"+"</a></li>");
          if(g_cur_page<pages)
          li.appendTo(ul);
       var li = $(" <li  class='pagelast'><a href='javascript:void(0)'  onclick='requestData(" + pages + ")'>"+"尾页"+"</a></li>");
           li.appendTo(ul);
       $('.pagepre').one('click', function(event) {    //上一页
          var prePage = g_cur_page-1;
       if(prePage > 0)
          requestData(prePage);
          });
        $('.pagenext').one('click', function(event) {   //下一页                   
          var nextPage = g_cur_page+1;
        if(nextPage <= pages)
             requestData(nextPage);
             });
    }