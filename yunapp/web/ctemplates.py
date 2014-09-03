# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

web_templates = Blueprint('web_templates', __name__)


@web_templates.route('/template_detai.html', methods=['GET'])
def template_detail():
    return render_template('contract_temp/template_detail.html')
