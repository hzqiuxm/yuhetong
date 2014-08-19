# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, current_app, jsonify

from yunapp.orm import model, engine
from yunapp.logutils import StructedMsg

template = Blueprint('template', __name__)
app_logger = logging.getLogger('yunapp')
biz_logger = logging.getLogger('business')

#TODO(wenwu) Detele before online, init template in db, cannot called by user
@template.route('/init', methods=['GET'])
def init_template():
    content_path = current_app.root_path + \
    '/contract_temp/template_type_content'
    with open(content_path, 'r') as c_t:
        for content in c_t.readlines():
            template_type = content.split(',')
            t_name = template_type[0].strip(' \t\n\r')
            t_level = template_type[1].strip(' \t\n\r')
            t_parent = template_type[2].strip(' \t\n\r')
            t_status = template_type[3].strip(' \t\n\r')


        return jsonify({'success': True})
