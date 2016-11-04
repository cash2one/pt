/**
 * Created by Administrator on 2015/9/15 0015.
 */
var picNav = $("#pic-nav>li"),
	g_per_page = 32,
	cur_category = '广告图片',
	g_cur_page = 1,
	searchkeywords = '';

$(function() {
	/*页面图标弹出弹窗*/
	$(".addpicbtn").bind('click', function() {
		$(".addpicbtn").removeClass("mcurrent");
		$(this).addClass("mcurrent");
		$('#dialogUpload').modal('show');
	})


	/*页面加载不同类型的图片*/
	picNav.click(function() {
		$(this).addClass("active").siblings().removeClass("active");
		var cindex = picNav.index($(this));
		cur_category = $(this).text();

		//清空图片和分页内容，显示加载中图标

		$("#loading").show();
		$("#searchImg").val('');
		$(".imglist,.pagelist").empty();

		searchkeywords = '';

		//请求数据
		requestData(1);

	})
	requestData(1);

	/*绑定搜索按钮功能*/
	$("#searchBtn").click(function() {
		searchkeywords = $("#searchImg").val();
		requestData(1);
		return false;
	});


	/**/
	$("#searchImg").keydown(function(e) {
		var e = e || event,
			keycode = e.keyCode || e.which;
		if (keycode == 13) {
			$("#searchBtn").click();
			return false;
		}

	})

	$("#usepic").click(function() {
		var urlImg = $('.tab-content .delmodal.selected').siblings("img").attr("src");
		$('#dialogUpload').modal('hide');
		$(".addpicbtn.mcurrent").hide().next("input[type=hidden]").val(urlImg);
		$('<div class="newImg"><img src="' + urlImg + '"/><span class="glyphicon glyphicon-remove"></span></div>').insertAfter(".addpicbtn.mcurrent");
		/*$(".addpicbtn.mcurrent").hide();*/
		return false;
	})



	/*动态绑定图片删除状态*/
	$(document).on("click", '.tab-content .delmodal', function() {
		$('.tab-content .delmodal').removeClass("selected");
		$(this).toggleClass("selected");
	})


	/*本地上传图片*/
	$("#addLocalImg").click(function() {
		$('#dialogUpload').modal('hide');
		$('#UploadModal').modal('show');
		if (!uploader) {
			initImgUploader();
			//解决webuploader 在弹出框中浏览文件按钮不起作用的bug，一定要放在web uploader初始化之后
			$("#filePicker .webuploader-pick").click(function() {
				$("#filePicker :file").click();
			});
		}
	});
	$("#useTheImg").click(function() {
		$('#UploadModal').modal('hide');
		var imgSrc = $("#fileList img").data("src");
		$(".addpicbtn.mcurrent").hide().next("input[type=hidden]").val(imgSrc);
		$('<div  class="newImg"><img src="' + imgSrc + '"/><span class="glyphicon glyphicon-remove"></span>           </div>').insertAfter(".addpicbtn.mcurrent");
		//uploader.destroy();
		return false;
	});
	$(document).on('click', '.newImg span', function() {
		$(this).parent(".newImg").siblings("a.addpicbtn").show()
			.end().siblings("input[type=hidden]").val('')
			.end().remove();
	})
})
//图片列表创建函数
function CreateImgList(data) {
	var htmlstr = '';
	$.each(data, function(i, value) {
		htmlstr += '<div class="w1in8 pr1in40"><img style="width:100%" src="' + value[2] + '"/><p class="text-overflow-js">' + value[0] + '</p><div class="delmodal"></div></div>';
	})
	$('.imglist').empty().append($(htmlstr));
}

function pagination(pages) {
	var ul = $("<ul>");
	$("#pagination ul").remove();
	if (pages == 1) {
		$("#pagination").css(
			"display", "none");
	} else {
		$("#pagination").css(
			"display", "block");
	};
	ul.appendTo("#pagination");
	$(ul).addClass('pagination');

	for (var i = 1; i <= 1; i++) {
		var li = $(" <li><a href='javascript:void(0)' onclick='requestData(" + i + ")'>" + "首页" + "</a></li>");
		li.appendTo(ul);
	}
	var pageDiv = $("<div class='pagelist'></div>");
	for (var i = 1; i <= pages; i++) {
		var li = $(" <li><a href='javascript:void(0)'  onclick='requestData(" + i + ")'>" + i + "</a></li>");
		li.appendTo(pageDiv);
		pageDiv.appendTo(ul)
	}
	var li = $(" <li><a href='javascript:void(0)'  onclick='requestData(" + i + ")'>" + "尾页" + "</a></li>");
	li.appendTo(ul);

};