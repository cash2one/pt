/**
 * Created by sunq on 16/6/2.
 */

/**
 * 组件化input选择框
 * @param input_id 需要填入的input的id
 * @param div_id 数据存放的div的id
 * @param uri 数据接口
 */
var pullData = (function () {
    var _focus = function (that) {
        that.input.focus(function () {
            that.div.show();
            that.search_key = '';
            that.cur_page = 0;
            that.total_page = 1;
            that.next_page = 1;
            that.pages = [];
            var type = 1;
            if (that.next_page <= that.total_page && !that.isloading && that.cur_page < that.total_page && that.pages.indexOf(that.next_page) < 0) {
                that.get_ajax_actions(that, type);

            }
        })
    };

    var _bind = function (that) {
        that.input.on("input propertychange", function () {
            that.search_key = $(this).val();
            that.cur_page = 0;
            that.total_page = 1;
            that.next_page = 1;
            that.pages = [];
            var type = 1;
            if (that.next_page <= that.total_page && !that.isloading && that.cur_page < that.total_page && that.pages.indexOf(that.next_page) < 0) {
                that.get_ajax_actions(that, type);

            }
        })
    };
    var _scroll = function (that) {
        that.div.scroll(function () {
            that.nScrollHight = $(this)[0].scrollHeight;
            that.nScrollTop = $(this)[0].scrollTop;
            if (that.nScrollHight - that.nScrollTop - that.containerHeight <= 100) {
                var type = 2;
                if (that.next_page <= that.total_page && !that.isloading && that.cur_page < that.total_page && that.pages.indexOf(that.next_page) < 0) {

                    that.get_ajax_actions(that, type)
                }
            }
        })
    };
    var _load_html = function (that, actions, type) {
        if (type == 1) {
            that.div.html('');
        }
        var data_to_html = function (item) {
            var html = '<a data-value="' + item[0] + '" onclick="selectOne(this,\'' + that.hide_input_id + '\',\'' + that.input_id + '\',\'' + that.div_id + '\')">' + item[1] + '</a>';
            return html
        };

        var htmls = actions.map(data_to_html);
        var html_str = htmls.reduce(function (a, b) {
            return a + b
        }, '');
        that.div.append(html_str);
    };

    var pullDataFun = function (input_id, hide_input_id, div_id, uri) {

    };
    pullDataFun.prototype.init = function (input_id, hide_input_id, div_id, uri, rely_id) {
        this.input = $(input_id);
        this.div = $(div_id);
        this.hide_input = $(hide_input_id);
        this.hide_input_id = hide_input_id;
        this.input_id = input_id;
        this.div_id = div_id;
        this.uri = uri;
        this.next_page = 1;
        this.cur_page = 0;
        this.total_page = 1;
        this.search_key = "";
        this.nScrollHight = 0; //滚动距离总长(注意不是滚动条的长度)
        this.nScrollTop = 0;   //滚动到的当前位置
        this.containerHeight = this.div.height();
        this.isloading = false;
        this.rely_id = rely_id;
        this.pages = [];
        _focus(this);
        _bind(this);
        _scroll(this);
        return this
    };
    pullDataFun.prototype.get_ajax_actions = function (that, type) {
        var data = {'page': that.next_page, 'search_key': that.search_key};
        if (that.rely_id.length > 0) {
            var id = $(that.rely_id).val().trim();
            if (id) {
                data['id'] = id;
            }
        }
        $.ajax({
            url: that.uri,
            data: data,
            dataType: 'json',
            method: 'GET',
            beforeSend: function (that) {
                that.isloading = true;
            },
            success: function (data) {
                var actions = data.actions;
                that.next_page = data.cur_page + 1;
                that.cur_page = data.cur_page;
                that.total_page = data.total_page;
                that.pages.push(that.cur_page);

                _load_html(that, actions, type)
            }, error: function (req) {
                console.log(req.statusCode)
            }
        }).done(function (that) {
            that.isloading = false;
        });

    };


    return pullDataFun;
})();
function selectOne(obj, hide_input_id, input_id, div_id) {
    var action_id = $(obj).data("value");
    var action_name = $(obj).html();
    $(hide_input_id).val(action_id);
    $(input_id).val(action_name);
    $(div_id).hide();

}



