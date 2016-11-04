/**
 * Created by Administrator on 2015/9/16 0016.
 */
/*加载上传图片控件*/
var config = {
    swfUri: '/webuploader/0.1.5/.swf',
    tokenUrl : 'http://cms.putao.so/uptoken',
    imageUrl : 'http://img.putao.so',
    imageUploadUrl : 'http://upload.qiniu.com/',
    token:''
},uploader;
// 全局令牌
$.ajax({
    url: config.tokenUrl,
    type: 'POST',
    dataType:'json',
    crossDomain: true,
    withCredentials: true,
    success: function(json) {
        config.token = json.token;
    },
    error:function(){
    }
});

// 图片上传demo
function initImgUploader() {
    var $ = jQuery,
        $list = $('#fileList'),
    // 优化retina, 在retina下这个值是2
        ratio = window.devicePixelRatio || 1,

    // 缩略图大小
        thumbnailWidth = 100 * ratio,
        thumbnailHeight = 100 * ratio;

    // Web Uploader实例


    // 初始化Web Uploader
    uploader = WebUploader.create({

        // 自动上传。
        auto: true,

        // swf文件路径
        //swf: BASE_URL + '/js/Uploader.swf',

        // 文件接收服务端。
        server: 'http://upload.qiniu.com/',

        // 选择文件的按钮。可选。
        // 内部根据当前运行是创建，可能是input元素，也可能是flash.
        pick: '#filePicker',

        // 只允许选择文件，可选。
        accept: {
            title: 'Images',
            extensions: 'gif,jpg,jpeg,bmp,png',
            mimeTypes: 'image/*'
        }
    });

    // 当有文件添加进来的时候
    uploader.on( 'fileQueued', function( file ) {
        var $li = $(
                '<div id="' + file.id + '" class="file-item thumbnail">' +
                '<img>' +
                '<div class="info">' + file.name + '</div>' +
                '</div>'
            ),
            $img = $li.find('img');

        $list.empty().append( $li );

        // 创建缩略图
        uploader.makeThumb( file, function( error, src ) {
            if ( error ) {
                $img.replaceWith('<span>不能预览</span>');
                return;
            }

            $img.attr( 'src', src );
        }, thumbnailWidth, thumbnailHeight );
    });
    /*开始上传之前做TOKEN认证*/
    uploader.on("uploadBeforeSend",function(object,data,headers){
        data.token = config.token;
    })
    // 文件上传过程中创建进度条实时显示。
    uploader.on( 'uploadProgress', function( file, percentage ) {
        var $li = $( '#'+file.id ),
            $percent = $li.find('.progress span');

        // 避免重复创建
        if ( !$percent.length ) {
            $percent = $('<p class="progress"><span></span></p>')
                .appendTo( $li )
                .find('span');
        }

        $percent.css( 'width', percentage * 100 + '%' );
    });

    // 文件上传成功，给item添加成功class, 用样式标记上传成功。
    uploader.on( 'uploadSuccess', function( file, response) {
      // alert("上传成功");
        $("#filePicker .webuploader-pick").text("重新选择图片");
        var src = config.imageUrl + '/' + response.key;
        $("#fileList img").data("src",src);
        $("#useTheImg").show();
        $( '#'+file.id ).addClass('upload-state-done');
    });
    // 文件上传失败，现实上传出错。
    uploader.on( 'uploadError', function( file ) {
        var $li = $( '#'+file.id ),
            $error = $li.find('div.error');

        // 避免重复创建
        if ( !$error.length ) {
            $error = $('<div class="error"></div>').appendTo( $li );
        }

        $error.text('上传失败');
    });

    // 完成上传完了，成功或者失败，先删除进度条。
    uploader.on( 'uploadComplete', function( file ) {
        $( '#'+file.id ).find('.progress').remove();
    });
}
