/**
 * Created by sunq on 16/6/12.
 */
$(document).ready(function() {
	init();
	new pullData().init("#categoryname", "#categoryid", "#categoryselect", "/main/ajax_second_categories_ci/", "");
	new pullData().init("#actionname", "#actionid", "#actionselect", "/main/ajax_actions/", "#categoryid");
	new pullData().init("#quickordername", "#quickorderid", "#quickorderselect", "/main/ajax_quick_order/", "#categoryid");
	new pullData().init("#goodsname", "#goodsid", "#goodsselect", "/main/ajax_desc_goods/", "#categoryid");
	if (id > 0) {
		get_edit_data(id)
	}

});

function init() {
	/*初始化页面*/
	setNavBg("category");
}

var data = {
	goods: [],
	goods_ids: [],
	banners: [],
	quick_orders: [],
	quick_order_ids: [],
	category_id: 0

};

var vm = new Vue({
	el: "#edit_category_index",
	data: data,
	methods: {
		edit_banner: function(event) {
			var button = $(event.target)[0];
			var adbean_id = parseInt(button.dataset.adbeanid);
			var adbean_name = button.dataset.adbeanname;
			var image = button.dataset.image;
			var action_id = button.dataset.actionid;
			var action_name = button.dataset.actionname;
			var start = button.dataset.start;
			var end = button.dataset.end;
			var activecity = button.dataset.activecity;
			var sort = button.dataset.sort;
			var index = parseInt(button.dataset.index);


			// console.log(event)
			// console.log(index);
			// console.log(adbean_id);
			// console.log(adbean_name);
			// console.log(action_id);
			// console.log(action_name);
			// console.log(start);
			// console.log(end);

			if (index < 0) {
				$("#edit_banner h4").html("添加banner");
				$('#edit_banner div:nth-child(2) a').show();
				$('#edit_banner div:nth-child(2) div.newImg').remove();
			} else {
				$("#edit_banner h4").html("编辑banner")
				var image_html = '<div class="newImg"><img src="' + image + '"><span class="glyphicon glyphicon-remove"></span></div>';
				$('#edit_banner div:nth-child(2) a').hide();
				$('#edit_banner div:nth-child(2) a').after(image_html);
			}
			$('#icon_url').val(image);
			$('#bannertitle').val(adbean_name);
			$('#bannerid').val(adbean_id);
			$('#actionid').val(action_id);
			$('#actionname').val(action_name);
			$('#bannersort').val(sort);
			$('#bannerindex').val(index);
			$('#bannercity').val(activecity);
			$('#bannerstart').val(start);
			$('#bannerend').val(end);
			$('#banners').hide();
			$('#submit-confirm').attr('disabled', true);
			$('#edit_banner').show();

		},
		delete_banner: function(index) {
			if (confirm("确定删除Banner?")) {
				this.del(index, this.banners)
			}

		},
		save_banner: function() {
			var index = $('#bannerindex').val();
			var adbean = {};
			adbean.adbean_id = parseInt($('#bannerid').val().trim());
			adbean.adbean_name = $('#bannertitle').val().trim();
			adbean.image = $('#icon_url').val().trim();
			if (adbean.image == '') {
				alert("请选择banner图片");
				return false
			}
			if (adbean.adbean_name == '') {
				alert("请输入banner标题");
				return false
			}
			adbean.action_id = $('#actionid').val().trim() | '';
			adbean.action_name = $('#actionname').val().trim();
			if (adbean.action_id == '') {
				adbean.action_id = -1
			}
			var sort = $('#bannersort').val().trim();
			if (sort == '') {
				alert("请输入排序");
				return false
			}
			adbean.start = $('#bannerstart').val().trim();
			if (adbean.start == '') {
				alert("请选择开始时间");
				return false

			}
			adbean.end = $('#bannerend').val().trim();
			if (adbean.end == '') {
				alert("请选择结束时间");
				return false

			}
			if (adbean.start >= adbean.end) {
				alert("开始时间比较小于结束时间!");
				return false
			}
			adbean.active_city = $('#bannercity').val().trim();
			if (adbean.active_city == '') {
				alert("请选择城市");
				return false
			}
			console.log(adbean);
			if (sort < 0) {
				alert('优先级非法');
				return false
			}
			if (index > -1) {
				this.del(index, this.banners)
			}
			this.banners.splice(this.banners.length - sort + 1, 0, adbean);

			return this.cancel('#edit_banner', '#banners')

		},
		edit_quick_order: function(event) {
			var category_id = $('#categoryid').val();
			if (category_id != this.category_id) {
				Vue.set(data, 'category_id', category_id);
			}
			var button = $(event.target)[0];
			var quick_id = button.dataset.quickid;
			var quick_name = button.dataset.quickname;
			var sort = button.dataset.sort;
			var index = button.dataset.index;
			if (index < 0) {
				$("#edit_quickorder h4").html("添加快捷入口")
			} else {
				$("#edit_quickorder h4").html("编辑快捷入口")
			}
			$('#quickorderid').val(quick_id);
			$('#quickordername').val(quick_name);
			$('#quickordersort').val(sort);
			$('#quickindex').val(index);
			$('#quickorders').hide();
			$('#submit-confirm').attr('disabled', true);

			$('#edit_quickorder').show();
		},
		delete_quick_order: function(index) {
			if (confirm("确定删除快捷入口?")) {
				var old_quick_order = this.quick_orders[index];
				this.del(index, this.quick_orders);
				var index = this.quick_order_ids.indexOf(old_quick_order.quick_order_id);
				this.del(index, this.quick_order_ids)
			}
		},
		save_quick_order: function() {
			var flag = true;
			var quick_order = {};
			var quick_order_ids = $('#quickorderid').val();
			quick_order.quick_order_id = parseInt(quick_order_ids.split('-')[0]);
			quick_order.quick_order_desc = quick_order_ids.split('-')[1];
			quick_order.quick_order_name = $('#quickordername').val();
			if (quick_order.quick_order_id == '') {
				alert('请选择快捷入口');
				flag = false;
				return false
			}
			var sort = $('#quickordersort').val();
			var index = parseInt($('#quickindex').val());

			if (this.quick_order_ids.indexOf(quick_order.quick_order_id) >= 0 && index < 0) {
				alert("该快捷入口已经选择,请重新选择!");
				flag = false;
				return false
			}
			if (sort < 0) {
				alert('优先级非法');
				return false
			}
			if (flag) {
				if (index > -1) {
					var old_quick_order = this.quick_orders[index];
					if (old_quick_order) {
						this.del(index, this.quick_orders);
						var index = this.quick_order_ids.indexOf(old_quick_order.quick_order_id);
						this.del(index, this.quick_order_ids)
					}

				}
				if (this.quick_order_ids.indexOf(quick_order.quick_order_id) >= 0) {
					alert("该快捷入口已经选择,请重新选择!");
					flag = false;
					$('#quickindex').val(-1);
					return false
				} else {
					this.quick_orders.splice(this.quick_orders.length - sort + 1, 0, quick_order);
					this.quick_order_ids.push(quick_order.quick_order_id);
					this.cancel('#edit_quickorder', '#quickorders')
				}

			}

		},
		edit_recommended_goods: function(event) {
			var category_id = $('#categoryid').val();
			if (category_id != this.category_id) {
				Vue.set(data, 'category_id', category_id);
			}

			var button = $(event.target)[0];
			var index = button.dataset.index;
			if (index < 0) {
				$("#edit_recomendedservice h4").html("添加推荐服务")
			} else {
				$("#edit_recomendedservice h4").html("编辑推荐服务")
			}
			var goods_name = button.dataset.goodsname;
			var goods_id = button.dataset.goodsid;
			var sort = button.dataset.sort;
			var start = button.dataset.start;
			var end = button.dataset.end;
			$('#goodsid').val(goods_id);
			$('#goodsname').val(goods_name);
			$('#recommendedsort').val(sort);
			$('#recommendedstart').val(start);
			$('#recommendedend').val(end);
			$('#oldindex').val(index);
			$('#recommendedservices').hide();
			$('#submit-confirm').attr('disabled', true);

			$('#edit_recomendedservice').show();
		},
		delte_reommended_goods: function(index) {
			if (confirm("确定删除推荐服务?")) {
				var old_quick_order = this.goods[index];
				this.del(index, this.goods);
				var index = this.goods_ids.indexOf(old_quick_order.goods_id);
				this.del(index, this.goods_ids)
			}

		},
		save_recommended_goods: function() {
			var recommended_good = {};
			var flag = true;
			var sort = $('#recommendedsort').val().trim();
			var old_index = parseInt($('#oldindex').val());
			recommended_good.goods_id = parseInt($('#goodsid').val().trim());
			recommended_good.goods_name = $('#goodsname').val().trim();

			if (recommended_good.goods_id == '' || recommended_good.goods_name == '') {
				alert("请选择服务");
				flag = false;
				return false
			}
			recommended_good.start = $('#recommendedstart').val().trim();
			if (recommended_good.start == '') {
				alert("请选择开始时间");
				flag = false;
				return false
			}
			recommended_good.end = $('#recommendedend').val().trim();
			if (recommended_good.end == '') {
				alert("请选择结束时间");
				flag = false;
				return false
			}
			if (recommended_good.start >= recommended_good.end) {
				alert("开始时间比较小于结束时间!");
				flag = false;
				return false
			}
			if (this.goods_ids.indexOf(recommended_good.goods_id) >= 0 && old_index < 0) {
				alert("该服务已经选择,请重新选择!");
				flag = false;
				return false
			}
			if (sort < 0) {
				alert('优先级非法');
				return false
			}

			if (flag) {
				if (old_index > -1) {
					var old_quick_order = this.goods[old_index];
					if (old_quick_order) {
						this.del(old_index, this.goods);
						var index = this.goods_ids.indexOf(old_quick_order.goods_id);
						this.del(index, this.goods_ids)
					}

				}
				if (this.goods_ids.indexOf(recommended_good.goods_id) >= 0) {
					alert("该服务已经选择,请重新选择!");
					flag = false;
					$('#oldindex').val(-1);
					return false
				} else {
					this.goods.splice(this.goods.length - sort + 1, 0, recommended_good);
					this.goods_ids.push(recommended_good.goods_id);
					this.cancel('#edit_recomendedservice', '#recommendedservices')
				}
			}


		},
		cancel: function(edit_field, table_field) {
			$(edit_field).hide();
			$(table_field).show();
			$('#submit-confirm').attr('disabled', false);
			$('.newImg').remove();

		},
		del: function(index, arr) {
			arr.splice(index, 1);
		},
		up: function(index, arr) {
			if (index - 1 >= 0) {
				this.exch(index, index - 1, arr)
			}
		},
		down: function(index, arr) {
			if (index + 1 < arr.length) {
				this.exch(index, index + 1, arr)
			}
		},
		exch: function(i, j, arr) {
			var i_temp = arr[i];
			var j_temp = arr[j];
			arr.splice(i, 1, j_temp);
			arr.splice(j, 1, i_temp);
		}
	}

});

function get_edit_data(id) {
	$.ajax({
		url: "/main/update_category_index/",
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
	console.log(edit_data)
	if (edit_data.category_index_id > 0) {
		$('#categoryname').attr('disabled', true);
		$('#categoryid').val(edit_data.category_id);
		Vue.set(data, 'category_id', edit_data.category_id);

		$('#categoryname').val(edit_data.category_name);
		if (edit_data.category_is_need > 0) {
			$("#is-need-all").attr('checked', true)
		} else {
			$("#is-need-all").attr('checked', false)
		}
		$('#category-index-city').val(edit_data.category_city);
		$('#edit_category_index  section.top-sec ol  li.active').html('编辑分类首页')
	}
	if (edit_data.banners.length > 0) {
		render_banners(edit_data.banners)
	}
	if (edit_data.goods.length > 0) {
		render_goods(edit_data.goods, edit_data.goods_ids)
	}
	if (edit_data.quick_orders.length > 0) {
		render_quick_order(edit_data.quick_orders, edit_data.quick_order_ids)
	}
}

function render_banners(arr) {
	var banners = [];
	for (var i = 0; i < arr.length; i++) {
		var banner = {};
		banner.adbean_id = arr[i][0];
		banner.adbean_name = arr[i][1];
		banner.image = arr[i][2];
		banner.action_id = arr[i][5];
		banner.action_name = arr[i][6];
		banner.active_city = arr[i][7];
		banner.start = arr[i][3];
		banner.end = arr[i][4];
		banners.push(banner)
	}
	Vue.set(data, 'banners', banners)

}

function render_goods(goods, goods_ids) {
	Vue.set(data, 'goods_ids', goods_ids);

	var result = [];
	for (var i = 0; i < goods.length; i++) {
		var good = {};
		good.goods_id = goods[i][0];
		good.goods_name = goods[i][1];
		good.start = goods[i][2];
		good.end = goods[i][3];
		result.push(good);
	}
	Vue.set(data, 'goods', result)
}

function render_quick_order(quick_orders, quick_order_ids) {
	Vue.set(data, 'quick_order_ids', quick_order_ids);

	var result = [];
	for (var i = 0; i < quick_orders.length; i++) {
		var quick_order = {};
		quick_order.quick_order_id = quick_orders[i][0];
		quick_order.quick_order_name = quick_orders[i][2];
		quick_order.quick_order_desc = quick_orders[i][1];
		result.push(quick_order)
	}
	Vue.set(data, 'quick_orders', result)
}

function cancel() {
	if (confirm("确定取消?")) {
		window.location.href = "/main/category_index/";
	}
}

function submit() {
	var args = check_args();
	console.log(args);
	args.id = id;

	if (args) {
		$.ajax({
			url: '/main/insert_category_index/',
			data: args,
			type: 'post',
			dataType: 'json',
			success: function(data) {
				if (data.code == 0) {
					window.location.href = "/main/category_index/"
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
	args.category_id = $('#categoryid').val().trim();
	var old_category_id = data.category_id;
	if (old_category_id != args.category_id && (data.banners.length > 0 || data.quick_orders.length > 0 || data.goods.length > 0)) {
		alert("服务资源列表错误,请重新选择!");
		return false
	}

	for (var i = 0; i < data.banners.length; i++) {
		if (data.banners[i].active_city == '不限(全国)') {
			data.banners[i].active_city = '*'
		}
	}
	args.banners = JSON.stringify(data.banners);

	args.quick_orders = JSON.stringify(data.quick_orders);
	args.recommended_goods = JSON.stringify(data.goods);
	args.city = $('#category-index-city').val().trim();
	if (args.city == '不限(全国)') {
		args.city = '*';
	}
	if ($('#is-need-all:checked').val()) {
		args.is_need_all = 1;
	} else {
		args.is_need_all = 0;

	}
	return args;
}

vm.$watch('category_id', function() {
	if (id < 1) {
		this.goods = [];
		this.goods_ids = [];
		this.quick_orders = [];
		this.quick_order_ids = [];
	}

});