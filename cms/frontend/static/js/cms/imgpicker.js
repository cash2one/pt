(function(Vue, $, plupload) {
	var category = ['广告图片', '大图标', '小图标', '优惠券', '其他'];
	var listUrl = '/main/get_images/';
	var imageCDNUrl = 'http://img.putao.so/',
		tokenUrl = 'http://cms.putao.so/uptoken/',
		uploadUrl = 'http://upload.qiniu.com/';
	var uploader;

	var imgpicker = new Vue({
		el: '.imgpicker',
		replace: false,
		template: '<div class="modal fade imgpicker" id="imgpicker">\
                        <div class="modal-dialog modal-lg">\
                            <div class="modal-content">\
                                <div class="modal-header">\
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true" @click="close">&times;</button>\
                                    <div class="col-xs-5 col-sm-5 col-md-5">\
                                        <div class="input-group">\
                                            <input type="text" class="form-control" placeholder="请输入图片名" v-model="searchKey" @keyup.enter="search">\
                                            <span class="input-group-btn">\
                                                <button class="btn btn-primary" type="button" @click="search">搜索</button>\
                                            </span>\
                                        </div>\
                                    </div>\
                                    <div class="pull-right ctrls">\
                                        <button type="button" class="btn btn-warning" @click="ensure">确认使用</button>\
                                        <button type="button" class="btn btn-primary" id="fileupload" @click="localUpload">本地上传</button>\
                                    </div>\
                                </div>\
                                <div class="modal-body">\
                                    <div class="alert alert-danger" v-show="errorInfo">\
                                        <button type="button" class="close" @click="clearInfo">&times;</button>\
                                        <strong>提示：</strong><span v-text="errorInfo"></span>\
                                    </div>\
                                    <ul class="nav nav-tabs category" v-show="category.length">\
                                        <li v-for="item in category" :class="$index == isActive ? \'active \' : \'\'">\
                                            <a href="#" @click.prevent="tab(item, $index)" v-text="item"></a>\
                                        </li>\
                                    </ul>\
                                    <div class="imglist">\
                                        <template v-if="imgs.length">\
                                            <label v-for="item in imgs">\
                                                <input type="radio" name="img">\
                                                <img alt="img" :src="item[2]" @click="chooseImg(item[2])">\
                                                <span>\
                                                    <i class="glyphicon glyphicon-ok"></i>\
                                                </span>\
                                            </label>\
                                        </template>\
                                        <template v-else>\
                                            <p class="text-warning">没有找到任何图片~</p>\
                                        </template>\
                                    </div>\
                                    <div class="loading" v-show="ajax.isLoading">\
                                        <img src="/static/images/loading.gif">\
                                    </div>\
                                </div>\
                                <div class="modal-footer" v-show="ajax.pageTotal > 1">\
                                    <ul class="pager">\
                                        <li :class="ajax.pageNum>1?\'\':\'disabled\'"><a href="#" @click="goPrev">上一页</a></li>\
                                        <li :class="ajax.pageNum<ajax.pageTotal?\'\':\'disabled\'"><a href="#" @click="goNext">下一页</a></li>\
                                    </ul>\
                                    <div class="label label-default pager-state">\
                                        <span v-text="ajax.pageNum"></span>\
                                        <em>/</em>\
                                        <span v-text="ajax.pageTotal"></span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    </div>',
		data: function() {
			return {
				searchKey: '',
				category: category,
				isActive: 0,
				selectedImg: '',
				imgs: [],
				ajax: {
					isLoading: false,
					category: category[0],
					pageNum: 1,
					pageTotal: 1,
					pageSize: 32
				},
				errorInfo: '',
				callback: function() {}
			};
		},
		methods: {
			search: function() {
				var _this = this;
				this.ajax.pageNum = 1; // 重置分页页数
				this.getImgList({
					key: _this.searchKey
				}, function(res) {
					_this.imgs = res[0];
					_this.ajax.pageTotal = res[1];
				});
			},
			ensure: function() {
				var _this = this;
				if (!_this.selectedImg) {
					_this.errorInfo = '请选择一张图片';
					return;
				}
				$('#imgpicker').modal('hide');

				setTimeout(function() {
					_this.callback(_this.selectedImg);
				}, 400);
			},
			localUpload: function() {
				// 清空选中的图片
				this.selectedImg = '';
				var selected = document.querySelector('.imgpicker .modal-body .imglist input[type="radio"]:checked');
				if (!!selected)
					selected.checked = false;
			},
			tab: function(item, index) {
				var _this = this;
				this.isActive = index; // 设置tab激活
				this.ajax.pageNum = 1; // 重置分页页数
				this.ajax.category = item; // 设置当前分类
				this.getImgList({
					// cur_page: 1,
					image_category: _this.category[index]
				}, function(res) {
					_this.imgs = res[0];
					_this.ajax.pageTotal = res[1];
				});
			},
			chooseImg: function(img) {
				this.selectedImg = img;
			},
			goPrev: function() {
				var _this = this;
				if (this.ajax.pageNum === 1) {
					return;
				}
				this.ajax.pageNum -= 1;
				this.getImgList({
					cur_page: _this.ajax.pageNum
				}, function(res) {
					_this.imgs = res[0];
					_this.ajax.pageTotal = res[1];
				});
			},
			goNext: function() {
				var _this = this;
				if (this.ajax.pageNum === this.ajax.pageTotal) {
					return;
				}
				this.ajax.pageNum += 1;
				this.getImgList({
					cur_page: _this.ajax.pageNum
				}, function(res) {
					_this.imgs = res[0];
					_this.ajax.pageTotal = res[1];
				});
			},
			initUpload: function(option) {
				/**
                    [具体可参考官网文档](http://www.plupload.com/docs/Options)
                */
				$.getJSON(tokenUrl).done(function(res) {
					var token = res.token;
					var DEFAULT = {
						// container: '', // 上传按钮的父元素
						browse_button: 'fileupload',
						url: uploadUrl,
						multipart_params: {
							token: token
						},
						filters: {
							mime_types: 'image/*,application/zip',
							max_file_size: '10M' // 最大图片大小
						},
						multi_selection: false, // 是否可多选
						max_retries: 0, // 最大重试次数
						chunk_size: '2M'
					};
					option = $.extend({}, DEFAULT, option);
					uploader = new plupload.Uploader(option);

					uploader.bind('FileFiltered', function(uploader, file) {
						uploader.start();
						// 每个文件上传完成之前调用
						typeof option.loading === 'function' && option.loading();
					});

					uploader.bind('FileUploaded', function(uploader, file, response) {
						res = JSON.parse(response.response);
						// 每个文件上传完成后调用
						typeof option.done === 'function' && option.done(res);
					});

					uploader.bind('Error', function(uploader, error) {
						// 每个文件上传失败后调用
						typeof option.error === 'function' && option.error(error);
					});

					uploader.init();
				}).fail(function(e) {
					console.error('获取token失败，请稍后重试~');
				});
			},
			getImgList: function(url, data, done, fail) {
				var _this = this;

				var DEFAULT = {
					url: listUrl,
					data: {
						key: '',
						cur_page: _this.ajax.pageNum,
						per_page: _this.ajax.pageSize,
						image_category: _this.ajax.category
					}
				};
				if ($.type(url) === 'object') {
					fail = done || function() {};
					done = data || function() {};
					data = $.extend({}, DEFAULT.data, url);
					url = DEFAULT.url;
				} else if ($.type(url) === 'string') {
					fail = fail || function() {};
					done = done || function() {};
					data = $.extend({}, DEFAULT.data, data);
				}
				if (this.ajax.isLoading) {
					return;
				} else {
					this.ajax.isLoading = true;
				}
				$.getJSON(url, data).done(function(res) {
					done(res);
				}).fail(function(e) {
					console.error(e);
					_this.errorInfo = '获取图片列表失败，请稍后重试~';
					fail(e);
				}).always(function() {
					_this.ajax.isLoading = false;
				});
			},
			close: function() {
				$('#imgpicker [id^="html5_"]').remove();
				uploader.destroy();

				// 清空数据
				this.searchKey = '';
				this.isActive = 0;
				// this.selectedImg = '',
				this.errorInfo = '';
				this.ajax = {
					isLoading: false,
					category: category[0],
					pageNum: 1,
					pageTotal: 1
				};
			},
			clearInfo: function() {
				this.errorInfo = '';
			},
			// 自定义调用方法
			init: function(option) {
				var _this = this;
				if (typeof option === 'function') {
					this.callback = option;
				} else {
					if (!option || typeof option.callback !== 'function') {
						throw new Error('callback必须是一个函数');
					} else {
						this.callback = option.callback;
					}
				}
				this.getImgList({
					image_category: _this.category[0]
				}, function(res) {
					_this.imgs = res[0];
					_this.ajax.pageTotal = res[1];
				});

				option = $.extend({}, {
					loading: function() {
						_this.ajax.isLoading = true;
					},
					done: function(res) {
						_this.ajax.isLoading = false;
						var url = imageCDNUrl + res.hash;
						_this.close();

						setTimeout(function() {
							_this.callback(url);
						}, 400);
					},
					error: function(e) {
						if (e.code == -600) {
							_this.errorInfo = '图片超过了' + option.filters.max_file_size + '，请重新选择图片~';
						} else {
							_this.errorInfo = '上传图片失败，请稍后重试~';
						}
						_this.ajax.isLoading = false;
					}
				}, option);

				// 初始化本地上传按钮
				this.initUpload(option);
			}
		}
	});

	window['imgpicker'] = imgpicker;
	return null;
})(Vue, $, plupload);