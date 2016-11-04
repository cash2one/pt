/**
 * Created by Administrator on 2015/8/25 0025.
 */
    $(document).ready(function(){

        var cities = g_cities;
        var province_len=cities.length;
        console.log("开始时间是"+new Date());

        var citystr_spe='<div id="spec-city">'
            +'<div class="width1in8"><div class="list-group-item list-inline"><input type="checkbox" value="北京"/>北京</div></div>'
            + '<div class="width1in8"><div class="list-group-item list-inline"><input type="checkbox" value="上海"/>上海</div></div>'
            +'<div class="width1in8"><div class="list-group-item list-inline"><input type="checkbox" value="天津"/>天津</div></div>'
            +'<div class="width1in8"><div class="list-group-item list-inline"><input type="checkbox" value="重庆"/>重庆</div></div></div>';

        $(".city-spec").append(citystr_spe);


        for(var x=0;x<province_len;x++){
            var nodesample = $('<div class="width1in8">  <div class="list-group-item list-inline"> </div></div>');
            nodesample.find(".list-group-item").html('<input type="checkbox" value="'+cities[x].proname+'"/>  '+cities[x].proname).data({'subcity':cities[x].citylist,"py":cities[x].pinyin});
            $(".list-group").append(nodesample);
        }

        var provicelist =$(".citylist .list-group-item");

        provicelist.each(function(i,ele){
            var that = $(this),
                index = provicelist.index(that),
                insertIndex = (parseInt(index/8)+1)* 8-1,
                htmlstr = '<div class="citydetailist row"><ul class="list-inline" style="vertical-align: middle">';

            /*if(index == 0) return;*/
            if(!that.data("flag")){
                $.each(that.data("subcity"),function(i,ele){
                    htmlstr += '<li><label><input type="checkbox" value="'+ele+'"/>'+ele+'</label></li>';
                })
                htmlstr += '</ul></div>';
                if(insertIndex >= provicelist.length-1){
                    $(htmlstr).appendTo('.citylist .list-group').hide();
                }
                else{
                    $(htmlstr).insertBefore(provicelist.eq(insertIndex+1).parent(".width1in8")).hide();
                }
                that.data("flag",1);
            }
        });

        console.log("结束时间是"+new Date());

    });




    function putCitygroup(){

        var provicelist =$(".citylist .list-group-item");
        var specity=$(".city-spec .list-group-item");
        var citydetail=$(".citydetailist .list-inline");
        if(g_markcities!=undefined){
            var markcities=g_markcities;
            var mark_len=markcities.length;
            for(var i=0;i< mark_len; i++){
                $("input[type='checkbox'][value="+markcities[i]+"]").attr("checked",'checked');
            }
        }else{
            g_markcities!=undefined
        }

        citydetail.find("input:checkbox").each(function(){
            var parentNode=$(this).parents(".citydetailist .list-inline");
            var index=citydetail.index(parentNode);
            if(this.checked){
                $(".citylist .list-group-item").eq(index).css("background","#ccc");
            }
            var city_len=citydetail.eq(index).find("input:checkbox").length;
            var input_list=citydetail.eq(index).find("input:checkbox");
            for(var a=0;a<city_len;a++){

                if(input_list.eq(a).prop("checked") && (input_list.eq(a+1).prop("checked") || (input_list.eq(a+1).val())==undefined)){
                    $(".citylist .list-group-item").eq(index).find("input:checkbox").prop("checked","checked");
                }

            }
             for(var a=0;a<city_len;a++){
                 if(!(input_list.eq(a).prop("checked"))){
                    $(".citylist .list-group-item").eq(index).find("input:checkbox").removeAttr("checked");
                }
            }

            var sib_obj=$(this).parents("li").siblings().find("input:checkbox");
            var sib_len=sib_obj.length;
            var counted=0;

            for (var b=0;b<sib_len;b++){
                if(sib_obj[b].checked){
                    counted++;
                }
            }
            if(!this.checked && counted==0){
                $(".citylist .list-group-item").eq(index).css("background","#fff");
            }

        });



        provicelist.find("input:checkbox").each(function(l,pro){
            var parentNode = $(this).parent(".citylist .list-group-item");
            var index = provicelist.index(parentNode);
             //如果其下城市有选中，则使省份变蓝色
            $(".citydetailist").eq(index).find("input").each(function(k,item){
                if(item.checked==true){
                    //pro.checked=true;
                    $(pro).parent(".citylist .list-group-item").css({"background":"#ccc"});
                }
                /*console.log(k);*/
            });

        });

        specity.find("input:checkbox").each(function(s,x){
            if(x.checked){
                //pro.checked=true;
                $(x).parent(".city-spec .list-group-item").css({"background":"#ccc"});
            }else {
                $(x).parent(".city-spec .list-group-item").css({"background":"#fff"});
            }
        })
    }


    function clickReaction(){
        var provicelist =$(".citylist .list-group-item");
        var specity=$(".city-spec .list-group-item");
        var citydetail=$(".citydetailist .list-inline");


        provicelist.click(function(){
          var that = $(this),
                index = provicelist.index(that);
            $(".citydetailist").hide().eq(index).show();
            provicelist.each(function(i,k){
                $(k).css("border","1px solid #ccc");
            });
            $(this).css("border","1px solid #34CB95");

        });
        provicelist.find("input:checkbox").click(function(){
            var parentNode = $(this).parent(".citylist .list-group-item");
            var index = provicelist.index(parentNode);
            $(".citydetailist").eq(index).find("input").prop("checked",parentNode.find("input:checkbox")[0].checked);
             if(this.checked){
                $(this).parent(".citylist .list-group-item").css({"background":"#ccc"});
            }/*else {
                $(this).parent(".citylist .list-group-item").css({"background":"#fff"});
            }*/

            var sib_obj=$(".citydetailist").eq(index).find("input:checkbox");
            var sib_len=sib_obj.length;
            var counted=0;
            //console.log("兄弟节点是"+sib_obj);
            //console.log("兄弟长度是"+sib_obj.length);
            for (var b=0;b<sib_len;b++){
                if(sib_obj[b].checked){
                    counted++;
                }
            }
            if(!this.checked && counted==0){
                $(".citylist .list-group-item").eq(index).css("background","#fff");
            }
        });


        specity.find("input:checkbox").click(function(){
            if(this.checked){
                //pro.checked=true;
                $(this).parent(".city-spec .list-group-item").css({"background":"#ccc"});
            }else {
                $(this).parent(".city-spec .list-group-item").css({"background":"#fff"});
            }

        });


         //选中城市的，相应省份颜色要变调

        citydetail.find("input:checkbox").click(function(){
            var parentNode=$(this).parents(".citydetailist .list-inline");
            var index=citydetail.index(parentNode);
            if(this.checked){
                $(".citylist .list-group-item").eq(index).css("background","#ccc");
            }
            console.log(citydetail.eq(index).find("input:checkbox").length);
            var city_len=citydetail.eq(index).find("input:checkbox").length;
            var input_list=citydetail.eq(index).find("input:checkbox");
            for(var a=0;a<city_len;a++){
                /*if(input_list.eq(a+1).val()){*/
                //console.log(input_list.eq(a+1).val());
                if(input_list.eq(a).prop("checked") && (input_list.eq(a+1).prop("checked") || (input_list.eq(a+1).val())==undefined)){
                    $(".citylist .list-group-item").eq(index).find("input:checkbox").prop("checked","checked");
                }

            }
             for(var a=0;a<city_len;a++){
                 if(!(input_list.eq(a).prop("checked"))){
                    $(".citylist .list-group-item").eq(index).find("input:checkbox").removeAttr("checked");
                }
            }

            var sib_obj=$(this).parents("li").siblings().find("input:checkbox");
            var sib_len=sib_obj.length;
            var counted=0;
            for (var b=0;b<sib_len;b++){
                if(sib_obj[b].checked){
                    counted++;
                }
            }
            if(!this.checked && counted==0){
                $(".citylist .list-group-item").eq(index).css("background","#fff");
            }

        });

    }
