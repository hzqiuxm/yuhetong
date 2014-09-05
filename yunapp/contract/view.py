# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import logging,io,StringIO

from flask import Blueprint, jsonify, current_app, request,send_file

from yunapp.orm.model import LxContract
from yunapp.orm import engine
from yunapp.logutils import StructedMsg
from yunapp.contract.utils import Yunhetong_HTMLParser

contract = Blueprint('contract', __name__)
app_logger = logging.getLogger('yunapp')
biz_logger = logging.getLogger('business')

@contract.route('/<filename>.docx',methods=['POST'])
def doc_create(filename):
    doc_file = StringIO.StringIO()
    parser = Yunhetong_HTMLParser(doc_file)
    data=request.values.get('data','')

    parser.feed(data)

    # return 'hello world'
    # return send_file(io.BytesIO(fileData))
    s = io.BytesIO(parser.get_file())
    doc_file.close()
    parser.close()
    return send_file(s)

@contract.route('/', methods=['POST'])
def add_contract():
    """ Add a template
    :param template_name, template_type_id, template_content
    :return new_template_id
    """
    param_check_result = check_new_contract_param(request.values)
    if not param_check_result.get('success'):
        return jsonify(param_check_result)
    t_name = request.values.get('template_name', '')
    t_type_id = int(request.values.get('template_type_id', ''))
    t_content = request.values.get('template_content', '')
    with engine.with_session() as ss:
        t_type = LxContract.query.filter_by(
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
    return jsonify({'success':True, 'errorMsg':''})

def check_new_contract_param(args):
    pass
