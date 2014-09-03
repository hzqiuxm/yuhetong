# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, current_app, jsonify, request, render_template
from flask.ext.login import login_required

from yunapp.utils import get_int_page_num
from yunapp.orm import model, engine
from yunapp.orm.model import LxTempType, LxTemplate
from yunapp.logutils import StructedMsg
from yunapp.contract_temp import constants

template = Blueprint('template', __name__)
app_logger = logging.getLogger('yunapp')
biz_logger = logging.getLogger('business')

#TODO(wenwu) Detele before online, init template in db, cannot called by user
@template.route('/init_template_type', methods=['GET'])
def init_template_type():
    """ Init template type from file template_type_content
        The legal department should edit the document and run the function
    """
    content_path = current_app.root_path + '/contract_temp/template_type_content'
    with open(content_path, 'r') as c_t:
        for content in c_t.readlines():
            t_dict = get_temptype_content(content)
            if t_dict is None:
                biz_logger.error('Add template type error content:' + content)
                continue
            with engine.with_session() as ss:
                if t_dict.get('parent') == '0':
                    new_temp_type = LxTempType(
                        name = t_dict.get('name'),
                        level = t_dict.get('level'),
                        status = t_dict.get('status')
                    )
                    ss.add(new_temp_type)
                    biz_logger.info(StructedMsg('add level 0 template' +
                                                t_dict.get('name'),model=__name__))
                else:
                    parent_temp_type = LxTempType.query.filter_by(
                        name=t_dict.get('parent'), status=1
                    ).first()
                    new_temp_type = LxTempType(
                        name = t_dict.get('name'),
                        level = t_dict.get('level'),
                        status = t_dict.get('status'),
                        parent_id = parent_temp_type.id
                    )
                    ss.add(new_temp_type)
                    biz_logger.info(StructedMsg('add level ' + str(t_dict.get(
                        'level')) + ' template' +  t_dict.get('name'), model=__name__))
        return jsonify({'success': True})

def get_temptype_content(line):
    temptype_dict = {}
    try:
        template_type = line.split(',')
        temptype_dict['name'] = template_type[0].strip(' \t\n\r')
        temptype_dict['level'] = int(template_type[1].strip(' \t\n\r'))
        temptype_dict['parent'] = template_type[2].strip(' \t\n\r')
        temptype_dict['status'] = int(template_type[3].strip('\t\n\r'))
        return temptype_dict
    except:
        app_logger.exception('get temptype content error')
        return None
#TODO END

@template.route('/template_types', methods=['GET'])
# @login_required
def get_template_types():
    """ Get the template types from the system
    :param parent_type_id
    """
    # Get input params
    # ptype_id = request.values.get('parent_type_id', '')
    # page_num = get_int_page_num(request.values.get('page_num', '1'))

    f_dict = dict()
    f_dict['status'] = 1
    f_dict['level'] = 0
    # if ptype_id:
    #     f_dict['parent_id'] = ptype_id

    t_types = LxTempType.query.filter_by(**f_dict).order_by(LxTempType.id.desc())
    # t_types = t_types.paginate(page_num, constants.PAGE_SIZE, False)

    re_dict = dict()
    # re_dict['total'] = t_types.total
    # re_dict['total_page'] = t_types.pages
    type_list = list()
    for t_type in t_types:
        t_type = t_type.serialize()
        t_type.pop('gmt_modify')
        t_type.pop('gmt_create')
        # t_type.pop('parent_id')
        children = t_type.pop('children')
        child_list = list()
        for child in children:
            child = child.serialize()
            child.pop('children')
            child.pop('gmt_modify')
            child.pop('gmt_create')
            child_list.append(child)
        t_type['children'] = child_list
        type_list.append(t_type)
    re_dict['list'] = type_list
    return jsonify({'success':True, 'data':re_dict})

@template.route('/check_template_name', methods=['GET'])
def check_template_name():
    """ Check the template_name is exist or not
    :param template_name
    :return True: not exist can be used; False: exist can not be used
    """
    t_name = request.values.get('template_name', '')
    if not t_name:
        return jsonify(dict(success=False, errorMsg=constants.ERROR_CODE[
            'PARAM_NOT_ENOUGH']))
    templ = LxTemplate.query.filter_by(name=t_name).first()
    if templ is None:
        return jsonify(dict(success=True, data=True))
    else:
        return jsonify(dict(success=True, data=False))

@template.route('/templates', methods=['POST'])
def add_template():
    """ Add a template
    :param template_name, template_type_id, template_content
    :return new_template_id
    """
    param_check_result = check_new_template_param(request.values)
    if not param_check_result.get('success'):
        return jsonify(param_check_result)
    t_name = request.values.get('template_name', '')
    t_type_id = int(request.values.get('template_type_id', ''))
    t_content = request.values.get('template_content', '')
    with engine.with_session() as ss:
        t_type = LxTempType.query.filter_by(
            id=t_type_id, status=1).first()
        if t_type is None:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
            'NO_SUCH_TEMPLATE_TYPE']})
        new_template = LxTemplate(
            name = t_name,
            type = t_type,
            content = t_content,
            status = 1
        )
        ss.add(new_template)
    return jsonify({'success':True, 'data':new_template.id})

@template.route('/template/<int:tid>', methods=['GET'])
def get_template(tid):
    """ Get a template by id
    :param template_type_id
    :return the particular template
    """
    with engine.with_session() as ss:
        templ = ss.query(LxTemplate).get(tid)
        if templ is None:
            return jsonify({'success':False, 'errorMsg': constants.ERROR_CODE[
            'NO_SUCH_TEMPLATE']})
        templ = templ.serialize()
        templ.pop('gmt_modify')
        templ.pop('gmt_create')
        templ.pop('type')
        templ.pop('owner')
        # return jsonify({'success':True, 'data': templ})
        return jsonify({'success':True, 'data': templ})

@template.route('/', methods=['GET'])
def get_templates():
    """ Get templates by template_type_id or name key word
        search_key use a like search
    :param template_type_id, search_key
    :return templ_list
    """
    page_num = get_int_page_num(request.values.get('page_num', '1'))

    filter_dict = dict(status = 1)
    if 'template_type_id' in request.values:
        filter_dict['type_id'] = request.values.get('template_type_id', '')
    search_key = None
    if 'search_key' in request.values:
        search_key = request.values.get('search_key', '')
    templates = LxTemplate.query.filter_by(**filter_dict).order_by(
        LxTemplate.id.desc())
    # templates = ss.query(LxTemplate).filter_by(**filter_dict)
    if search_key:
        templates = templates.filter(
            LxTemplate.name.like('%' + search_key +'%'))

    templates = templates.paginate(page_num, constants.PAGE_SIZE, False)
    re_dict = dict()
    re_dict['total'] = templates.total
    re_dict['total_page'] = templates.pages
    print templates.page
    print templates.pages
    print templates.total
    print templates.next_num
    print templates.prev_num
    templ_list = []
    for templ in templates.items:
        templ_item = templ.serialize()
        templ_item.pop('gmt_modify')
        templ_item.pop('gmt_create')
        templ_type = templ_item.pop('type')

        templ_item['type_id'] = templ_type.id
        templ_item['type_name'] = templ_type.name
        templ_item.pop('owner')
        templ_list.append(templ_item)
    re_dict['list'] = templ_list
    # return render_template('contract_temp/template_list.html', data=re_dict)
    return jsonify({'success':True, 'data': re_dict})




@template.route('/<int:tid>', methods=['DELETE'])
def del_template(tid):
    """ Delete templates by template_type_id
    :param template_type_id
    :return templ.id
    """
    with engine.with_session() as ss:
        templ = ss.query(LxTemplate).get(tid)
        if templ is None:
            return jsonify({'success':False, 'errorMsg': constants.ERROR_CODE[
            'NO_SUCH_TEMPLATE']})
        templ.update(dict(status=-1))
        return jsonify({'success':True, 'data': templ.id})

@template.route('/<int:tid>', methods=['PUT'])
def update_template(tid):
    """ Update templates by template_type_id
    :param template_type_id
    :return templ.id
    """
    with engine.with_session() as ss:
        templ = ss.query(LxTemplate).get(tid)
        if templ is None:
            return jsonify({'success':False, 'errorMsg': constants.ERROR_CODE[
            'NO_SUCH_TEMPLATE']})
        update_dict = dict()
        if 'template_name' in request.values:
            update_dict['name'] = request.values.get('template_name', '')
        if 'template_type_id' in request.values:
            t_type_id = int(request.values.get('template_type_id', ''))
            t_type = ss.query(LxTempType).filter_by(
                id=t_type_id, status=1).first()
            if t_type is None:
                return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
            'NO_SUCH_TEMPLATE_TYPE']})
            update_dict['type'] = t_type
        if 'template_content' in request.values:
            update_dict['content'] = request.values.get('template_content', '')
        templ.update(update_dict)
    return jsonify({'success':True, 'data': templ.id})

def check_new_template_param(arg_values):
    """ Delete templates by template_type_id
    :param arg_values
    :return True or False
    """
    t_name = arg_values.get('template_name', '')
    t_type_id = arg_values.get('template_type_id', '')
    t_content = arg_values.get('template_content', '')
    if not t_name or not t_type_id or not t_content:
        return {'success': False, 'errorMsg': constants.ERROR_CODE[
            'PARAM_NOT_ENOUGH']}
    return {'success': True}
    #TODO check other param


