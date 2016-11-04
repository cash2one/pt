(function($) {
	var cdn = {
		swfUri: '/webuploader/0.1.5/.swf',
		tokenUrl: 'http://cms.putao.so/uptoken',
		imageUrl: 'http://img.putao.so',
		imageUploadUrl: 'http://upload.qiniu.com/',
		token: ''
	};

	// 获取七牛上传token
	$.post(cdn.tokenUrl).done(function(res) {
		res = JSON.stringify(res);
		upload(res.token);
	}).fail(function(e) {
		throw new Error(e);
	});

	function upload(token) {
		var uploader = (function(option) {
			var DEFAULT = {
				// container: '', // 上传按钮的父元素
				browse_button: 'fileupload', // 上传按钮的id
				url: "http://upload.qiniu.com/?token=" + token,
				filters: {
					mime_types: 'image/*',
					max_file_size: '10M', // 最大图片大小
					prevent_duplicates: false // 阻止重复提交
				},
				multi_selection: true, // 是否可多选
				max_retries: 0, // 最大重试次数
				chunk_size: '2M'
			};
			option = $.extend({}, DEFAULT, option);
			return new plupload.Uploader(option);
		})();
		window['uploader'] = uploader;
	};

	$.post('http://cms.putao.so/uptoken').done(function(res) {
		res = JSON.stringify(res);
		var token = res.token,
			DEFAULT = {
				// container: '', // 上传按钮的父元素
				browse_button: 'fileupload', // 上传按钮的id
				url: "http://upload.qiniu.com/?token=" + token,
				filters: {
					mime_types: 'image/*',
					max_file_size: '10M', // 最大图片大小
					prevent_duplicates: false // 阻止重复提交
				},
				multi_selection: true, // 是否可多选
				max_retries: 0, // 最大重试次数
				chunk_size: '2M'
			},
			option = $.extend({}, DEFAULT, option);

		new plupload.Uploader(option);
	}).fail(function(e) {
		throw new Error(e);
	});


})(jQuery);