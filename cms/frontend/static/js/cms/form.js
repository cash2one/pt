/**
 * Created by Administrator on 2015/8/25 0025.
 */
function sendTime(){
            var mon=$("#cmsvalidtimemodel-month input[type='checkbox']");
            var day=$("#cmsvalidtimemodel-day input[type='checkbox']");
            var week=$("#cmsvalidtimemodel-week input[type='checkbox']");
            var hour=$("#cmsvalidtimemodel-hour input[type='checkbox']");
            var min=$("#cmsvalidtimemodel-minute input[type='checkbox']");
            var monstr="",daystr="",weekstr="",hourstr="",minstr="";
            var timestr="";

            var mon_len=mon.length, day_len=day.length, week_len=week.length, hour_len=hour.length, min_len=min.length;
            for(var a=0;a<mon_len;a++){
                if(mon[a].checked){
                    monstr+=$(mon[a]).val()+",";
                }
            }
            for(var b=0;b<day_len;b++){
                if(day[b].checked){
                     daystr+=$(day[b]).val()+",";
                }
            }
            for(var m=0;m<week_len;m++){
                if(week[m].checked){
                     weekstr+=$(week[m]).val()+",";
                }
            }
            for(var n=0;n<hour_len;n++){
                if(hour[n].checked){
                     hourstr+=$(hour[n]).val()+",";
                }
            }
             for(var k=0;k<min_len;k++){
                if(min[k].checked){
                     minstr+=$(min[k]).val()+",";
                }
            }

            if(monstr==""){
                monstr="*";
            }else {
                monstr=monstr.substring(0,monstr.length-1);
            }
            if(daystr==""){
                daystr="*";
            }else {
                daystr=daystr.substring(0,daystr.length-1);
            }
              if(weekstr==""){
                weekstr="*";
            } else {
                  weekstr=weekstr.substring(0,weekstr.length-1);
              }
              if(hourstr==""){
                hourstr="*";
            } else {
                  hourstr=hourstr.substring(0,hourstr.length-1);
              }
              if(minstr==""){
                minstr="*";
            } else {
                  minstr=minstr.substring(0,minstr.length-1);
              }

            //timestr = monstr+" "+daystr+" "+weekstr+" "+hourstr+" "+minstr;
            timestr = minstr+" "+hourstr+" "+daystr+" "+monstr+" "+weekstr;
            $("#valid_time").val(timestr);

    }

function selectAction(obj){
        var action_id=$(obj).data("value");
        var action_name=$(obj).html();
        console.log(action_id);
        $("#action_uid").val(action_id);
        $("#action_id").val(action_id);
        $("#actionselect").hide();
        if(action_id==-1){
            $(".correctbtn").show().css("display","inline-block");
        }else {
            $(".correctcontent").hide();
            $("#action_json").val("");
            $(".correctbtn").hide();
        }

    }

//checkdate
     function checkDate(){
          var timestr=document.getElementById("valid_time").value;

         if(timestr && timestr!="* * * * *"){
             document.getElementById("validateTime")[1].selected=true;
             $("#validataDiv").show();
         }
         console.log("时间"+timestr);
         var mon=$("#cmsvalidtimemodel-month input[type='checkbox']");
         var day=$("#cmsvalidtimemodel-day input[type='checkbox']");
         var week=$("#cmsvalidtimemodel-week input[type='checkbox']");
         var hour=$("#cmsvalidtimemodel-hour input[type='checkbox']");
         var min=$("#cmsvalidtimemodel-minute input[type='checkbox']");
         var monstr="",daystr="",weekstr="",hourstr="",minstr="";
         monstr=timestr.split(" ")[3];
         daystr=timestr.split(" ")[2];
         weekstr=timestr.split(" ")[4];
         hourstr=timestr.split(" ")[1];
         minstr=timestr.split(" ")[0];


         //开始对获取的日期遍历，勾选满足条件的
         checkDot(1,monstr,mon);
         checkDot(1,daystr,day);
         checkDot(1,weekstr,week);
         checkDot(0,hourstr,hour);
         checkDot(0,minstr,min);
     }


    function checkDot(x,sel_arr,chkbox_arr){
        if(x){
            for(var m=0;m< chkbox_arr.length;m++){
                chkbox_arr[m].value=m+1;
            }
        }else {
            for(var m=0;m< chkbox_arr.length;m++){
                chkbox_arr[m].value=m;
            }
        }

        //console.log("ser_arr"+typeof sel_arr);
        if(sel_arr){
            if(sel_arr=="*"){
                sel_arr=[];
            }else {
                sel_arr=sel_arr.split(",");
            }
            for(var i=0;i< sel_arr.length;i++){
                for(var j=0;j<chkbox_arr.length;j++){
                    if(sel_arr[i]==chkbox_arr[j].value){
                        chkbox_arr[j].checked=true;
                    }
                }
            }
        }

    }




function chooseCityGroup(id,url){
        $(".city-wrap").find("input:checkbox").prop("checked",false);
        var group_id=$(id).children("option:selected").val();
        var provicelist =$(".citylist .list-group-item");
        var specity=$(".city-spec .list-group-item");

         $(".list-group-item").each(function(){
            $(this).css("background","#fff");
        });

        $.ajax({
            type:'GET',
            url:url,
            data:{"group_id":group_id},
            dataType:'json',
            success:function(data){
               /* console.log(data);*/

                var markcities=data;
                var mark_len=markcities.length;

                for(var i=0;i< mark_len; i++){
                    if (markcities[i]=="*") {
                        markcities[i] ="全国";
                    }
                    $("input[type='checkbox'][value="+markcities[i]+"]").prop("checked",true);
                }


                var citydetail=$(".citydetailist .list-inline");
                citydetail.find("input:checkbox").each(function(){
                    var parentNode=$(this).parents(".citydetailist .list-inline");
                    var index=citydetail.index(parentNode);
                    if(this.checked){
                        $(".citylist .list-group-item").eq(index).css("background","#ccc");
                    }
                    var city_len=citydetail.eq(index).find("input:checkbox").length;
                    var input_list=citydetail.eq(index).find("input:checkbox");
                    for(var a=0;a<city_len;a++){
                        /*if(input_list.eq(a+1).val()){*/
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

            },
            error:function(){

            }
        })
     }

    function cityDrop(){
         if($("#cityselect_id").find("option:selected").val()==1){
             $("#city-selection").show();
         }else {
             $("#city-selection").hide();
             $(".city-wrap input:checkbox").prop("checked",false);
             $(".city-wrap .list-group-item").css("background","#fff");
         }
    }


    function checkForm(error_hint){
         var hints=error_hint;
         var inputs=$("form input");
         var inputs_len=inputs.length;

         if(hints){
             var hintstr="<ul>";
             $.each(hints,function(i,item){

                 var name = $("input[name='"+i+"']").siblings("label").text().replace("*","").replace("：","").replace(":","");
                 $("input[name='"+i+"']").css("border","1px solid #D9534F");
                 //for(var s=0;s<inputs_len;s++){
                 //    if(inputs[s].name==i){
                 //       $(inputs[s]).siblings("label").length>0? i=$(inputs[s]).siblings("label").html().replace("*",""):i="";
                 //        $(inputs[s]).css("border","1px solid #D9534F");
                 //    }
                 //}
                 hintstr+='<li>'+name+"  :  "+item+'</li>';
             });
             hintstr+='</ul>';
             $("#error-hints").html(hintstr).show();

         }else {
             $("#error-hints").hide();
         }
     }



    function selectCity(){
         $("#cityselect_id").change(function(){
                var idx_val=$(this).find("option:selected").val();
                //console.log("变化的选项是"+idx_val);
                if(idx_val==1) {
                    $("#city-selection").show();
                }else if(idx_val==0){
                    $("#city-selection").hide();
                    $(".city-wrap input:checkbox").prop("checked",false);
                    $(".city-wrap .list-group-item").css("background","#fff");
                }

         });
    }



    $(document).ready(function(){
        $('.item-dropmenu').on("click",function(event){
                //console.log("进入");
                if(event.target.nodeName.toLowerCase()=='a'){
                    var item_id=$(event.target).data("value");
                    var item_name=$(event.target).html();
                    console.log(item_id);
                    $(event.target).parent().siblings("input").eq(1).val(item_name.replace("&nbsp;&nbsp;└&nbsp;&nbsp;","└ "));
                    console.log(item_id);
                    $(event.target).parent().siblings("input").eq(0).val(item_id);
                    $('.item-dropmenu').hide();
                }
        });

        $(".item_id").focus(function(){
             $(".item-dropmenu").show();
         }).on("input propertychange",function(){
            var item_str=$(this).val();
            var item_arr=$(".item-dropmenu a");
            var item_len=item_arr.length;
            for(var i=0;i<item_len;i++){
                var htmlstr=$(item_arr[i]).html();
                if(htmlstr.indexOf(item_str.toLowerCase())>=0){
                    $(item_arr[i]).show();
                }else {
                    $(item_arr[i]).hide();
                }
            }

        });
    });

        function setPhone(){
            var telstr=$("#numbers").val();
            var tel_obj=JSON.parse(telstr);
            var tel_len=tel_obj.length;
            var clonenode=$("#first-tel").clone().removeAttr("id");
            var len=$(".extra-wrap").length;
            console.log(tel_len);
            console.log("回填的电话号码是"+tel_obj);
            if(tel_len){
                for(var i=0;i<tel_len;i++){
                    if(i==0){
                        $("#first-tel").find("input").eq(0).val(tel_obj[i].number).end()
                            .eq(1).val(tel_obj[i].number_description);
                    }else {
                        clonenode.find("label").eq(0).html("电话"+(len+1)).end()
                            .eq(1).html("电话"+(len+1)+"描述");
                        clonenode.find("input").eq(0).attr("name","tel"+(len+1)).val(tel_obj[i].number).end()
                            .eq(1).attr("name","tel"+(len+1)+"_desc").val(tel_obj[i].number_description);
                        $("#more-tel").append(clonenode);
                    }
                }
            }
        }

