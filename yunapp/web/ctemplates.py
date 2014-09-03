# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

web_templates = Blueprint('web_templates', __name__)


@web_templates.route('/template_detail.html', methods=['GET'])
def template_detail():
    return render_template('contract_temp/template_detail.html')
