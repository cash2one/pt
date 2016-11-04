/**
 * Created by Administrator on 2015/9/16 0016.
 */
$(document).ready(function(){
    var cities = g_cities;
    var province_len=cities.length;


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
            htmlstr = '<div class="citydetailist row"><ul class="list-inline">';
        if(!that.data("flag")){
            $.each(that.data("subcity"),function(i,ele){
                htmlstr += '<li><label><input type="checkbox" value="'+ele+'"/>'+ele+'</label></li>';
            });
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
        for (var b=0;b<sib_len;b++){
            if(sib_obj[b].checked){
                counted++;
            }
        }
        if(!this.checked && counted==0){
            $(".citylist .list-group-item").eq(index).css("background","#fff");
        }

    });


    var specity=$(".city-spec .list-group-item");

    specity.find("input:checkbox").click(function(){
        if(this.checked){
            //pro.checked=true;
            $(this).parent(".city-spec .list-group-item").css({"background":"#ccc"});
        }else {
            $(this).parent(".city-spec .list-group-item").css({"background":"#fff"});
        }

    });

    //选中城市的，相应省份颜色要变调
    var citydetail=$(".citydetailist .list-inline");
    citydetail.find("input:checkbox").click(function(){
        var parentNode=$(this).parents(".citydetailist .list-inline");
        var index=citydetail.index(parentNode);
        if(this.checked){
            $(".citylist .list-group-item").eq(index).css("background","#ccc");
        }
        var city_len=citydetail.eq(index).find("input:checkbox").length;
        var input_list=citydetail.eq(index).find("input:checkbox");
        for(var a=0;a<city_len;a++){
            /*if(input_list.eq(a+1).val()){*/
            /* console.log(input_list.eq(a+1).val());*/
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


    $("#actionselect").change(function(){
        $("#action_id").val(this.value) ;
        if(this.value == -1)
            $("a.correctbtn").css("display","inline-block");
        else
            $("a.correctbtn").css("display","none");

    });
    $("#action_id").bind("propertychange",function(){
        var key_word = $(this).val();

    })
    $("a.correctbtn").click(function(){
        $(".correctcontent").show();
    });

    $("#validateTime").change(function(){
        var sValue = parseInt($(this).find("option:selected").attr("value"));
        if(sValue) {
            $("#validataDiv").show();
        }
        else  {
            $("#validataDiv").hide();
            $("#validataDiv").find("input:checkbox").prop("checked",false);
        }
    });

    /*$(document).bind("click",function(e){
        if(e.target.id != 'actionselect' && e.target.id != 'action_uid'){
            $("#actionselect").hide();
        }
    });*/
});




function returnCityValue(){
    //城市回传
    var g_selectedcities =($("#citystr").val()).split(",") || "";
    var provicelist =$(".citylist .list-group-item");
    var specity=$(".city-spec .list-group-item");
    var citydetail=$(".citydetailist .list-inline");
    var markcities=g_selectedcities;
    var mark_len=markcities.length;
    console.log("回传城市是:"+markcities);

    if(markcities[0]!=""){
        for(var i=0;i< mark_len; i++){
            if (markcities[i]=="*") {
                //markcities[i] ="全国";
                //回填时候判断，是否下拉城市列表
                $("#cityselect_id").find("option:first").prop("selected","selected");
                $("#city-selection").hide();
                return;

            }else if(markcities[i]!="*"){
                $("input[type='checkbox'][value="+markcities[i]+"]").prop("checked",'checked');
                $("#cityselect_id").find("option:last").prop("selected","selected");
                $("#city-selection").show();
            }
        }
    }



    //城市回填判断是否选中，如果全选城市，则省份也要选中

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

            /*var sib_obj=$(this).parents("li").siblings().find("input:checkbox");
            var sib_len=sib_obj.length;
            var counted=0;
            for (var b=0;b<sib_len;b++){
                if(sib_obj[b].checked){
                    counted++;
                }
            }
            if(!this.checked && counted==0){
                $(".citylist .list-group-item").eq(index).css("background","#fff");
            }*/

        });


        //判断是否有选中

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
