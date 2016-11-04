# coding: utf-8
import json

import datetime

import pytz
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response

from common.views import pag, get_csv_response, add_common_var, report_render
from phone_fee.forms import CpPhoneFeeProductForm
from django.template import RequestContext
from django.db import transaction, connections

from phone_fee.models import CpPhoneFeeProduct, PtPhonefeeCpRelation, PtPhoneFeeProduct
from phone_fee.tasks import fee_updown_shelves_timing, fee_updown_shelves_timing_app
from phone_fee.views.phone_fee_pub import ReportConst, get_pf_cp, get_pf_carrier, \
    get_pf_management_table_columns, get_pf_province, get_max_prod_id, updown_shelves, edit_notify, \
    edit_sale_price, updown_shelves_app, get_app_name


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_PHONE_FEE, raise_exception=True)
@add_common_var
def phone_fee_goods_management(request, template_name):
    cp_names = get_pf_cp()
    carriers = get_pf_carrier()
    pf_management_table_columns = get_pf_management_table_columns()
    provinces = get_pf_province()
    my_app = request.GET.get('app', '-1')
    return report_render(request,template_name, {
        'app': my_app,
        "provinces": provinces,
        "cp_names": cp_names,
        "carriers": carriers,
        "table_columns": pf_management_table_columns,
    }, context_instance=RequestContext(request))


def check_order_info(product, cp_name, key, provinces, carriers):
    if cp_name:
        if str(product.cp_name) not in cp_name:
            return False

    if provinces:
        if str(product.prod_province_id) not in provinces:
            return False

    if carriers:
        if str(product.prod_isptype) not in carriers:
            return False

    if key:
        if key not in str(product.prod_isptype)  \
                and key not in str(product.cp_name)  \
                and key not in str(product.prod_province_id)  \
                and str(product.prod_content) != key:
            return False

    return True


def check_order_info_app(product, cp_name, key, provinces, carriers):
    if cp_name:
        try:
            p_name = PtPhonefeeCpRelation.objects.get(pt_prod_id=product.id).cp_name
        except:
            p_name = ''
        if str(p_name) not in cp_name:
            return False

    if provinces:
        if str(product.prod_name[0:-2]) not in provinces:
            return False

    if carriers:
        if str(product.prod_name[-2:]) not in carriers:
            return False

    if key:
        try:
            p_name = PtPhonefeeCpRelation.objects.get(pt_prod_id=product.id).cp_name
        except:
            p_name = ''
        if key not in str(product.prod_name[0:-2]) \
                and key not in str(p_name)  \
                and key not in str(product.prod_name[-2:])  \
                and str(product.prod_content) != key:
            return False

    return True


def update_order_info(orders,is_csv=0):
    result = []
    num = 0
    for order in orders:
        num += 1
        if is_csv == 0:
            result.append([
                str(''),
                str(order.id),
                str('more'),
                str(order.cp_name),
                str(order.prod_province_id),
                str(order.prod_isptype),
                str(order.prod_content),
                str(order.putao_price),
                str(order.prod_price),
                str(order.default_message),
                str(u'编辑'),
            ])
        else:
            result.append([
                str(num),
                str('more'),
                str(order.cp_name),
                str(order.prod_province_id),
                str(order.prod_isptype),
                str(order.prod_content),
                str(order.putao_price),
                str(order.prod_price),
                str(order.default_message),
            ])
    return result


def update_order_info_app(orders,is_csv=0):
    result = []
    i = 0
    for order in orders:
        i = i + 1
        if order.start_time == '' or order.end_time == '' or order.end_time is None or order.end_time is None:
            if order.status == 1:
                status = u'已上架'
            else:
                status = u'已下架'
        elif order.updown_status == 1:
            status = '上架:' + order.start_time + '--' + order.end_time
        elif order.updown_status == 0:
            status = '下架:' + order.start_time + '--' + order.end_time
        if order.message == None:
            message = ''
        else:
            message = order.message
        cp_names = PtPhonefeeCpRelation.objects.filter(pt_prod_id=order.id).values('cp_name')
        if not cp_names:
            cp_names = ''
        else:
            cp_names = cp_names[0]['cp_name']
        if is_csv == 0:
            result.append([
                str(''),
                str(order.id),
                str(status),
                str(cp_names),
                str(order.prod_name[0:-2]),
                str(order.prod_name[-2:]),
                str(order.prod_content),
                str(order.prod_price),
                str(order.purchase_price),
                str(message),
                str(u'编辑'),
            ])
        else:
            result.append([
                str(i),
                str(status),
                str(cp_names),
                str(order.prod_name[0:-2]),
                str(order.prod_name[-2:]),
                str(order.prod_content),
                str(order.prod_price),
                str(order.purchase_price),
                str(message),
            ])
    return result


def show_selected_columns(result, selected_columns):
    pf_management_table_columns = get_pf_management_table_columns()
    show_columns = []
    show_result = []
    row = []
    for col in selected_columns:
        for d_col in pf_management_table_columns:
            if col == d_col[1]:
                show_columns.append(d_col[0])
    for obj in result:
        for s_col in show_columns:
            row.append(obj[s_col])
        show_result.append(row)
        row = []
    return show_result


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_PHONE_FEE, raise_exception=True)
def phone_fee_goods_management_ajax(request):
    per_page = request.POST.get("per_page")
    cur_page = request.POST.get("cur_page")
    key = request.POST.get("key")
    if key != '' or key is not None:
        key = key.upper()
    provinces = request.POST.getlist("phone_fee_provinces[]")
    cp_name = request.POST.getlist("cp_name[]")
    carriers = request.POST.getlist("phone_fee_carriers[]")
    selected_columns = request.POST.getlist("pf_product_table[]")
    my_app = request.POST.get('app_id', '-1')
    if not cur_page:
        cur_page = 1
    if my_app == '-1':
        products = CpPhoneFeeProduct.objects.order_by('-m_time', 'id')
        # 有效商品检验
        tt_products = []
        for product in products:
            if check_order_info(product, cp_name, key, provinces, carriers):
                tt_products.append(product)

        # 获取订单列表下载信息
        global g_data
        g_data = []
        g_data = update_order_info(tt_products,is_csv=1)

        # 列表展示信息
        products, num_pages = pag(tt_products, per_page, cur_page)
        result = update_order_info(products)

        # 仅展示被选中的列表信息
        show_result = show_selected_columns(result, selected_columns)
        return HttpResponse(json.dumps([show_result, num_pages]))
    else:
        products = PtPhoneFeeProduct.objects.filter(app_id=my_app).order_by('-m_time', 'id')
        # 有效商品检验
        tt_products = []
        for product in products:
            if check_order_info_app(product, cp_name, key, provinces, carriers):
                tt_products.append(product)

        # 获取订单列表下载信息
        global g_data
        g_data = []
        g_data = update_order_info_app(tt_products,is_csv=1)

        # 列表展示信息
        products, num_pages = pag(tt_products, per_page, cur_page)
        result = update_order_info_app(products)

        # 仅展示被选中的列表信息
        show_result = show_selected_columns(result, selected_columns)
        return HttpResponse(json.dumps([show_result, num_pages]))


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_PHONE_FEE, raise_exception=True)
def phone_fee_goods_management_csv(request):
    filename = 'phone_fee_product_list.csv'
    csv_data = [[
                 u"排序",
                 u"状态",
                 u"供应商",
                 u"省份",
                 u"运营商",
                 u"面值",
                 u"售价",
                 u"进货价",
                 u"提示语",
                 ]]
    csv_data.extend(g_data)
    return get_csv_response(filename, csv_data)


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_PHONE_FEE, raise_exception=True)
def batch_edit_guarantee_order_info(request):
    edit_order_list = request.POST.get("edit_order_list")
    g_special_filter = request.POST.get("g_special_filter")
    check_status = request.POST.get("check_status")
    msg = u'no data update!'

    if edit_order_list and g_special_filter:
        cursor = connections['main'].cursor()
        sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET check_status = " + str(
            check_status) + " WHERE g_type = " + str(g_special_filter) + "  AND order_no IN ( " + str(
            edit_order_list) + " );"

        cursor.execute(sql)
        transaction.commit(using='main')
        msg = 'order update successfully!'

    return HttpResponse(json.dumps(msg))


@login_required
@permission_required(u'man.%s' % ReportConst.SHELVES_MANAGEMENT_PHONE_FEE, raise_exception=True)
def normal_edit_guarantee_order_info(request):
    # order_no = request.POST.get("order_no")
    # g_special_filter =request.POST.get("g_special_filter")
    # pt_comment =request.POST.get("pt_comment")
    # msg = 'no data update!'
    #
    # if order_no and g_special_filter and pt_comment != "":
    #     cursor = connections['main'].cursor()
    #     sql = "UPDATE pt_biz_db.pt_daojia_order_guarantee SET pt_comment = \""+str(pt_comment)+"\" WHERE g_type = "+str(g_special_filter)+"  AND order_no IN ( \""+str(order_no)+"\" );"
    #
    #     cursor.execute(sql)
    #     transaction.commit(using='main')
    #     msg = 'order update successfully!'
    #
    # return HttpResponse(json.dumps(msg))
    data = request.POST.copy()
    if data['prod_content'].find('.') != -1:
        data['prod_content'] = data['prod_content'][0:data['prod_content'].find('.')]
    app_id = request.POST.get('app_id', '-1')
    if app_id != '-1':
        PtPhoneFeeProduct.objects.filter(id=data['v_id'], app_id=app_id).update(prod_price=data['putao_price'],
                                                                                purchase_price=data['prod_price'],
                                                                                message=data['default_message'])
        PtPhonefeeCpRelation.objects.filter(pt_prod_id=data['v_id']).update(cp_name=data['cp_name'])
        return HttpResponse('ok')
    form = CpPhoneFeeProductForm(data)
    if form.is_valid():
        if data['cp_name'] == 'GY':
            data['cp_id'] = 7
        else:
            data['cp_id'] = 16
        try:
            c_p_fee_product = CpPhoneFeeProduct.objects.get(id=data['v_id'])
            c_p_fee_product.cp_id = data['cp_id']
            c_p_fee_product.prod_price = data['prod_price']
            c_p_fee_product.prod_name = data['prod_province_id'] + data['prod_isptype']
            c_p_fee_product.putao_price = data['putao_price']
            c_p_fee_product.is_able = 0
            c_p_fee_product.default_message = data['default_message']
            c_p_fee_product.save()
            pt_cp_re = PtPhonefeeCpRelation.objects.filter(cp_prod_id=c_p_fee_product.prod_id).values_list('pt_prod_id',
                                                                                                           )
            for i in pt_cp_re:
                # 编辑时只修改上架的商品信息
                PtPhoneFeeProduct.objects.filter(id=i[0], status=1).update(prod_price=data['putao_price'],
                                                                           purchase_price=data['prod_price'],
                                                                           message=data['default_message'])

            # PtPhonefeeCpRelation.objects.filter(cp_prod_id=c_p_fee_product.prod_id).update(cp_name=data['cp_name'])
            return HttpResponse('ok')
        except:
            data['prod_name'] = data['prod_province_id'] + data['prod_isptype']
            cp_p_f_data = CpPhoneFeeProduct.objects.filter(prod_name=data['prod_name'],
                                                            prod_content=data['prod_content'],
                                                            cp_name=data['cp_name'])
            if cp_p_f_data:
                return HttpResponse('false')
            # data['prod_price']=float(data['prod_price'])
            # data['putao_price']=float(data['putao_price'])
            # data['prod_content']=float(data['prod_content'])
            # data['is_able']=int(data['is_able'])
            # f_save = CpPhoneFeeProductForm(data).save()
            max_prod_id = get_max_prod_id() + 1
            data['prod_id'] = max_prod_id
            f_save = CpPhoneFeeProductForm(data)
            f_save.save()

            return HttpResponse('ok')
    else:
        errors = {}
        for item in form.errors:
            errors[item] = form.errors[item][0]

        return HttpResponse(json.dumps(errors))


# 批量上架
def phone_fee_batch_shelve_ajax(request):
    data = request.POST.copy()
    app = data['selectapp'].split(',')
    app_id = request.POST.get('app_id', '-1')
    selectlist = json.loads(data['selectlist'])
    pt_data = []
    if app_id == '-1':
        for i in selectlist:
            CpPhoneFeeProduct.objects.filter(id=i[0][0]).update(m_time=datetime.datetime.now())
            pt_not_null = updown_shelves(app, i[0], data['done'], data['is_updown'])
            if len(pt_not_null) != 0:
                pt_data += pt_not_null
    else:
        for i in selectlist:
            pt_data = updown_shelves_app(app_id, i[0], data['is_updown'], '', '', -1)
    return HttpResponse(json.dumps(pt_data))


# 批量改修改语
def phone_fee_batch_notify_ajax(request):
    app_id = request.POST.get('app_id', '-1')
    notify_data = json.loads(request.POST.get('notify_data'))
    notify_msg = request.POST.get('notify')
    for i in notify_data:
        errors = edit_notify(i[0], notify_msg, app_id)
    return HttpResponse(json.dumps(errors))


# 批量修改售价
def phone_fee_batch_sale_price_ajax(request):
    app_id = request.POST.get('app_id', '-1')
    sale_data = json.loads(request.POST.get('sale_data'))
    sale_status = request.POST.get('sale_status')
    not_cover = json.loads(request.POST.get('not_cover', []))
    errors = []
    # print sale_data
    for i in sale_data:
        errors += edit_sale_price(i[0], sale_status, not_cover, app_id)
    return HttpResponse(json.dumps({'sale_status': sale_status, 'data': errors}))


# 定时上下架
def phone_fee_batch_shelve_timing(request):
    app_id = request.POST.get('app_id', '-1')
    data = request.POST.copy()
    selectapp = data['selectapp']
    selectlist = json.loads(data['selectlist'])
    updown = data['is_updown']
    str_time = datetime.datetime.strptime(str(data['starttime']), '%Y-%m-%d %H:%M:%S')
    tz = pytz.timezone('Asia/Shanghai')
    str_t = tz.localize(str_time)
    end_time = datetime.datetime.strptime(str(data['endtime']), '%Y-%m-%d %H:%M:%S')
    end_t = tz.localize(end_time)
    if app_id == '-1':
        if updown == '1':
            for i in selectlist:
                fee_updown_shelves_timing.apply_async((selectapp, i[0], 1, str(data['starttime']), str(data['endtime']), 1), eta=str_t)
                fee_updown_shelves_timing.apply_async((selectapp, i[0], 0, '', '', -1), eta=end_t)
        else:
            for i in selectlist:
                fee_updown_shelves_timing.apply_async((selectapp, i[0], 0, str(data['starttime']), str(data['endtime']), 0), eta=str_t)
                fee_updown_shelves_timing.apply_async((selectapp, i[0], 1, '', '', -1), eta=end_t)
    else:
        if updown == '1':
            for i in selectlist:
                fee_updown_shelves_timing_app.apply_async((app_id, i[0], 1, str(data['starttime']), str(data['endtime']), 1), eta=str_t)
                fee_updown_shelves_timing_app.apply_async((app_id, i[0], 0, '', '', -1), eta=end_t)
        else:
            for i in selectlist:
                fee_updown_shelves_timing_app.apply_async((app_id, i[0], 0, str(data['starttime']), str(data['endtime']), 0), eta=str_t)
                fee_updown_shelves_timing_app.apply_async((app_id, i[0], 1, '', '', -1), eta=end_t)
    return HttpResponse()


def phone_fee_more_ajax(request):
    data_id = request.POST.get("id")

    more_list = []
    cp_prod_id = CpPhoneFeeProduct.objects.get(id=data_id).prod_id
    pt_re_data = PtPhonefeeCpRelation.objects.filter(cp_prod_id=cp_prod_id).values_list('pt_prod_id', 'cp_name')
    num = 0
    for i in pt_re_data:
        data_list = []
        num += 1
        try:
            pt_f_p = PtPhoneFeeProduct.objects.get(id=i[0])
        except:
            pass
        else:
            data_list.append(num)
            data_list.append(get_app_name(pt_f_p.app_id))
            data_list.append(i[1])
            if pt_f_p.start_time == '' or pt_f_p.end_time == '' or pt_f_p.start_time is None or pt_f_p.end_time is None:
                if pt_f_p.status == 1:
                    data_list.append(u'已上架')
                else:
                    data_list.append(u'已下架')
            elif pt_f_p.updown_status == 1:
                data_list.append('上架:' + pt_f_p.start_time + '--' + pt_f_p.end_time)
            elif pt_f_p.updown_status == 0:
                data_list.append('下架:' + pt_f_p.start_time + '--' + pt_f_p.end_time)
            more_list.append(data_list)

    return HttpResponse(json.dumps(more_list))
