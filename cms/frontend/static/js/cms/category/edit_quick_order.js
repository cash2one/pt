/**
 * Created by sunq on 16/6/7.
 */
"use strict";

var data = {
	goods: [],
	goods_ids: [],
	cp_names: [],
	category_id: 0,
	category_name: '',
	quick_order_name: '',
	background_style: '#000000',
	order_style: '#000000',
	icon_url: "",
	quick_order_desc: "",
	is_h5: 0,
	h5_url: ''
};

var vm = new Vue({
	el: '#edit_quick_order',
	data: data,
	methods: {
		add_service: function(event) {
			var new_goods = {};

			var baseName = $('#sname').val().trim();
			var flag = true;
			if (baseName) {
				var baseNames = baseName.split('-');
				if (baseNames.length = 3) {
					new_goods.cpname = baseNames[0];
					new_goods.goodsname = baseNames[1];
					new_goods.city = baseNames[2];
				} else {
					flag = false;
					alert('服务异常,请重新选择!');
					return false
				}

			} else {
				flag = false;
				alert('请选择服务');
				return false
			}
			new_goods.goodsid = parseInt($('#goodsid').val().trim());
			var oldsort = parseInt($('#oldsort').val());

			if (this.goods_ids.indexOf(new_goods.goodsid) >= 0 && oldsort < 0) {
				flag = false;
				alert('该服务已经选了,请重新选择');
				return false
			}
			if (this.cp_names.indexOf(new_goods.cpname) >= 0 && oldsort < 0) {
				flag = false;
				alert('该CP已经选了,请重新选择');
				return false
			}
			new_goods.desc = $('#opdesc').val().trim() | '';

			var sort = parseInt($('#sort').val()) | 0;
			console.log(sort);
			if (sort == 0) {
				alert('请填写优先级');
				return false
			}
			if (sort < 1) {
				alert('优先级非法');
				return false
			}
			if (flag) {
				if (oldsort > -1) {
					// console.log('删除前', this.goods);
					// console.log('要删的位置:', this.goods.length - oldsort);
					this.del(this.goods.length - oldsort);
					// console.log("删除后:", this.goods)

				}
				// console.log("插入前:", this.goods);
				// console.log("要插入的位置:", this.goods.length - sort + 1);
				// console.log("要插入的元素:", new_goods);
				if (this.goods_ids.indexOf(new_goods.goodsid) >= 0) {
					flag = false;
					alert('该服务已经选了,请重新选择');
					$('#oldsort').val(-1);
					return false
				}
				if (this.cp_names.indexOf(new_goods.cpname) >= 0) {
					flag = false;
					alert('该CP已经选了,请重新选择');
					$('#oldsort').val(-1);

					return false
				}
				this.goods.splice(this.goods.length - sort + 1, 0, new_goods);
				// console.log("插入后:", this.goods);

				this.goods_ids.push(new_goods.goodsid);
				this.cp_names.push(new_goods.cpname);
				$('#sname').val('');
				$('#goodsid').val('');
				$('#opdesc').val('');
				$('#sort').val('');
				$("#closeServiceModal").click()
			}
		},
		up: function(event) {
			var button = $(event.target)[0];
			var index = parseInt(button.dataset.index);
			// console.log(index)
			if (index - 1 >= 0) {
				this.exch(index, index - 1)
			}
		},
		down: function(event) {
			var button = $(event.target)[0];
			var index = parseInt(button.dataset.index);
			// console.log(index)
			if (index + 1 < this.goods.length) {
				this.exch(index, index + 1)
			}
		},
		exch: function(i, j) {
			var i_temp = this.goods[i];
			var j_temp = this.goods[j];
			this.goods.splice(i, 1, j_temp);
			this.goods.splice(j, 1, i_temp);

		},
		del: function(i) {

			var old_good = this.goods[i];
			var index = this.goods_ids.indexOf(old_good.goodsid);
			this.goods_ids.splice(index, 1);
			index = this.cp_names.indexOf(old_good.cpname);
			this.cp_names.splice(index, 1);
			this.goods.splice(i, 1);
		},
		view_del: function(i) {
			if (confirm("确定删除资源?")) {
				this.del(i)
			}
		}


	}
});

vm.$watch('category_id', function() {
	if (id < 1) {
		this.goods = [];
		this.goods_ids = [];
	}

});
$("#serviceModal").on('show.bs.modal', function(event) {
	var button = $(event.relatedTarget);
	var sname = button.data('sname');
	$('#sname').val(sname);
	var goodsid = button.data('goodsid');
	var desc = button.data('desc');
	var sort = button.data('sort');
	$('#goodsid').val(goodsid);
	$('#opdesc').val(desc);
	$('#sort').val(sort);
	if (sort > -1) {
		$("#serviceModalLabel").html('编辑服务资源');
		$('#oldsort').val(sort);

	} else {
		$("#serviceModalLabel").html('新增服务资源');
		$('#oldsort').val(-1);
		$('#sort').val(1)

	}

	var category_id = $("#categoryid").val() | 0;
	var category_name = $("#categoryname").val();
	Vue.set(data, 'category_id', category_id);
	Vue.set(data, 'category_name', category_name);
});
$("#serviceModal").on('hide.bs.modal', function(event) {
	$("#goodselect").html('');
});
$(document).ready(function() {
	init();
	new pullData().init("#categoryname", "#categoryid", "#categoryselect", "/main/ajax_second_categories/", "");
	new pullData().init("#sname", "#goodsid", "#goodselect", "/main/ajax_goods/", "#categoryid");
	if (id > 0) {
		get_edit_data(id)
	}
});

function init() {
	/*初始化页面*/
	setNavBg("category");
}

function get_edit_data(id) {
	$.ajax({
		url: "/main/update_quick_order/",
		data: {
			id: id
		},
		dataType: "json",
		type: "get",
		success: function(data) {
			if (data.code == 0) {
				render_data(data.extra)
			} else {
				console.log(data)
			}
		},
		error: function(req) {
			console.log(req.statusText)
		}
	})
}

function render_data(edit_data) {
	console.log(edit_data);
	vm.$set('is_h5', edit_data.is_h5);
	vm.$set('h5_url', edit_data.h5_url);

	if (edit_data.category_id > 0) {
		$('#categoryname').attr('disabled', true);
		$('#categoryname').val(edit_data.category_name);
		$('#categoryid').val(edit_data.category_id);
		Vue.set(data, 'category_id', edit_data.category_id);
		Vue.set(data, 'category_name', edit_data.category_name);
		Vue.set(data, 'quick_order_name', edit_data.quick_order_name);
		Vue.set(data, 'background_style', edit_data.background_style);
		Vue.set(data, 'order_style', edit_data.order_style);
		Vue.set(data, 'icon_url', edit_data.image_url);
		Vue.set(data, 'quick_order_desc', edit_data.quick_order_desc);
		Vue.set(data, 'goods_ids', edit_data.goods_ids);
		Vue.set(data, 'cp_names', edit_data.cp_names);
		var new_goods = [];
		for (var i = 0; i < edit_data.goods.length; i++) {
			var item = {};
			item.goodsname = edit_data.goods[i][4];
			item.cpname = edit_data.goods[i][2];
			item.desc = edit_data.goods[i][1];
			item.city = edit_data.goods[i][3];
			item.goodsid = edit_data.goods[i][0];
			new_goods.push(item)
		}
		Vue.set(data, 'goods', new_goods);
		var image_html = '<div class="newImg"><img src="' + edit_data.image_url + '"><span class="glyphicon glyphicon-remove"></span></div>'
		$('#edit_quick_order section.top-sec ol li.active').html('编辑快捷入口');
		$('#edit_quick_order div:nth-child(2) div:nth-child(6) a').hide();
		$('#edit_quick_order div:nth-child(2) div:nth-child(6) a').after(image_html);

	}
}

function cancel() {
	if (confirm("确定取消?")) {
		window.location.href = "/main/quick_order/";
	}
}

function submit() {
	var args = check_args();
	console.log(args);
	if (args) {
		args.id = id;
		$.ajax({
			url: '/main/insert_quick_order/',
			data: args,
			type: 'post',
			dataType: 'json',
			success: function(data) {
				if (data.code == 0) {
					window.location.href = "/main/quick_order/"
				} else {
					alert('必填字段不能为空')
				}
			},
			error: function(req) {
				console.log(req.statusText)
			}
		})
	}
}

function check_args() {
	var args = {};
	args.category_id = $("#categoryid").val() | 0;
	var old_category_id = data.category_id;
	if (args.category_id == 0) {
		alert("请选择分类!");
		return false
	}
	args.quick_order_name = data.quick_order_name.trim();
	if (args.quick_order_name < 1) {
		alert("请输入快捷入口名称!");
		return false
	}
	if (old_category_id != args.category_id && data.goods.length > 1) {
		alert("服务资源列表错误,请重新选择!");
		return false
	}
	args.icon_url = $("#icon_url").val().trim();

	if (args.icon_url == "") {
		alert("请选择快捷入口底图!");
		return false
	}
	args.quick_order_desc = data.quick_order_desc.trim();
	args.goods = JSON.stringify(data.goods);
	args.background_style = data.background_style;
	args.order_style = data.order_style;
	args.is_h5 = parseInt($('[name="is_h5"]:checked').val());
	args.h5_url = args.is_h5 == 1 ? $('[name="h5_url"]').val() : '';
	return args

}