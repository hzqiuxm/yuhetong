# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import logging,io,StringIO
from docx import Document
from docx.shared import Inches

from flask import Blueprint, render_template, jsonify, current_app, request,send_file

from yunapp.orm import model
from yunapp.orm import engine
from yunapp.logutils import StructedMsg
from yunapp.yunapps import app
from yunapp.contract.models import Yunhetong_HTMLParser

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