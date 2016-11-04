(function(Vue, $) {
	/** by jogiter
	 * 新增弹窗组件
	 * 待优化：按钮再:active和:focus时的背景颜色待调整
	 */

	var DEFAULTS = {
		size: 'modal-md', // 控制弹窗的大小
		dropback: 'static', // 背景层是否可点击
		title: '提示', // 默认标题
		content: '提示信息...', // 默认提示信息
		btns: ['取消', '确定'],
		yes: function() { // 默认点击“确定”的回调
			// do something..
		},
		no: function() { // 默认点击“取消”的回调
			// do something..
		}
	};

	var helper = new Vue({
		el: '.helper',
		replace: false,
		template: '<div class="modal fade" id="modal-helper" style="z-index: 1060">\
                        <div class="modal-dialog" :class="option.size">\
                            <div class="modal-content">\
                                <div class="modal-header">\
                                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                                    <h4 class="modal-title">{{option.title}}</h4>\
                                </div>\
                                <div class="modal-body">\
                                    {{{option.content}}}\
                                </div>\
                                <div class="modal-footer" v-if="option.btns && option.btns.length !== 0">\
                                    <template v-if="option.btns && option.btns.length === 2">\
                                        <button type="button" class="btn btn-default" data-dismiss="modal" @click="no">{{option.btns[0]}}</button>\
                                        <button type="button" class="btn btn-primary" @click="yes">{{option.btns[1]}}</button>\
                                    </template>\
                                    <template v-if="option.btns && option.btns.length === 1">\
                                        <button type="button" class="btn btn-primary center-block" @click="yes">{{option.btns[0]}}</button>\
                                    </template>\
                                </div>\
                            </div>\
                        </div>\
                    </div>',
		data: function() {
			return {
				option: DEFAULTS
			};
		},
		methods: {
			yes: function() {
				var _this = this;
				$('#modal-helper').modal('hide');
				setTimeout(function() {
					_this.option.yes();
				}, 400);
			},
			no: function() {
				var _this = this;
				$('#modal-helper').modal('hide');
				setTimeout(function() {
					_this.option.no();
				}, 400);
			},
			close: function() {
				$('#modal-helper').modal('hide');
			},
			loading: function(option) {
				var _this = this;
				option = $.extend({}, DEFAULTS, {
					btns: [],
					title: '加载中...',
					size: 'modal-md',
					content: '<div class="progress">\
                                  <div class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" aria-valuenow="100%" aria-valuemin="0" aria-valuemax="100" style="width: 100%">\
                                    <span class="sr-only">100%(success)</span>\
                                  </div>\
                                </div>'
				}, option);
				_this.option = option;
				$('#modal-helper').modal({
					dropback: option.dropback
				});
			},
			alert: function(option) {
				var _this = this;
				option = $.extend({}, DEFAULTS, {
					btns: ['确定'],
					size: 'modal-md',
					title: '提示',
					content: '提示信息...'
				}, option);
				_this.option = option;
				$('#modal-helper').modal({
					dropback: option.dropback
				});
			},
			confirm: function(option) {
				var _this = this;
				option = $.extend({}, DEFAULTS, {
					btns: ['取消', '确定'],
					size: 'modal-md',
					title: '提示',
					content: '确认信息...'
				}, option);
				_this.option = option;
				$('#modal-helper').modal({
					dropback: option.dropback
				});
			}
		}
	});

	window['helper'] = helper;
	return null;
})(Vue, jQuery);