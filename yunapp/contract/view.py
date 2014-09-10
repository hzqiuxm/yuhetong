# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import logging,io,StringIO, json

from flask import Blueprint, jsonify, current_app, request,send_file, g

from yunapp.orm.model import LxContract, LxFile, LxUser
from yunapp.orm import engine
from yunapp.logutils import StructedMsg
from yunapp.contract.utils import Yunhetong_HTMLParser
from yunapp.contract import constants
from yunapp.business.file import save_file, generate_file_uuid, \
    save_contract_file, delete_unused_file

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
    """ Add a contract
    :param contract_name, contract_content
    :return new_contract_id
    """

    param_check_result = check_new_contract_param(request.values)
    if not param_check_result.get('success'):
        return jsonify(param_check_result)
    c_name = request.values.get('contract_name', '')
    c_content = request.values.get('contract_content', '')
    c_appendix = request.values.get('appendix', '')
    appendix_json = get_appendix_json(c_appendix)

    c_fuuid = generate_file_uuid()
    c_path = save_contract_file(c_content, c_fuuid)

    with engine.with_session() as ss:
        new_file = LxFile(fuuid=c_fuuid,
                          type=constants.CONTRACT_FILE_TYPE,
                          name=c_name,
                          fpath=c_path)
        ss.add(new_file)

        new_contract = LxContract(
            owner = g.user,
            name = c_name,
            stage = 1,
            version = 1,
            contract_v1 = new_file,
            appendix = appendix_json,
            status = 1
        )
        ss.add(new_contract)

    return jsonify({'success':True, 'errorMsg':''})

@contract.route('/<int:cid>', methods=['PUT'])
def update_contract(cid):
    """ Modify a contract
    :param contract_name, contract_content, participants, appendix. Only this four part can be modified
    :return contract_id
    """
    update_dict = dict()
    c_name = request.values.get('contract_name', '')
    if c_name:
        update_dict.update('name', c_name)    # Update contract name    1
    c_appendix = request.values.get('appendix', '')
    if c_appendix:
        appendix_json = get_appendix_json(c_appendix)
        update_dict.update('appendix', appendix_json) # Update appendix   2
    # c_participants = request.values.get('participants', '')
    # participants_json = check_participants(c_participants)
    # if participants_json is None:
    #     return {'success': False, 'errorMsg':constants.ERROR_CODE['participants_check_error']}
    # if participants_json:
    #     update_dict.update('participants', participants_json)  # Update appendix   3
    is_new_version = request.values.get('new_version', '')
    c_content = request.values.get('contract_content', '')

    with engine.with_session() as ss:
        contract_to_update = ss.query(LxContract).get(cid)

        now_version = contract_to_update.version
        if is_new_version.equals('True') and now_version < 5:
            c_fuuid = generate_file_uuid()       # Update contract file -- New file version  4
            c_path = save_contract_file(c_content, c_fuuid)
            new_file = LxFile(fuuid=c_fuuid,
                          type=constants.CONTRACT_FILE_TYPE,
                          name=c_name,
                          fpath=c_path)
            ss.add(new_file)
            update_dict.update('version', now_version + 1)
            update_dict.update('contract_v' + str(now_version), new_file)
        else:       # Update contract file -- Old file version      4
            file_to_update = contract_to_update.getattr(LxContract,
                                                        'contract_v' + str(now_version))
            save_contract_file(c_content, file_to_update.fuuid)
        contract_to_update.update(update_dict)

    return jsonify({'success':True, 'errorMsg':''})

@contract.route('/save_draft/<int:cid>', methods=['POST'])
def save_draft(cid):
    """ Save the draft of the contract
    :param content
    :return contract_id
    """

@contract.route('/<int:cid>', methods=['DELETE'])
def del_contract(cid):
    """ Delete the contract, check the
    :param cid
    :return contract_id
    """

def check_new_contract_param(args):
    return { 'success': True }

# def check_participants(participants_str):
#     par_list = participants_str.split(',')
#     ret_list = list()
#     for par_item in par_list:
#         if par_item.isdigit():
#             par_item = int(par_item)
#             if LxUser.query.get(par_item):
#                 ret_list.append(par_item)
#             else:
#                 return None
#         else:
#             return None
#     ret_json = json.dumps(ret_list)
#     return ret_json

def get_appendix_json(appendix_str):
    appendix_list = appendix_str.split(',')
    ret_list = list()
    for appendix_item in appendix_list:
        if appendix_item.isdigit():
            ret_list.append(appendix_item)
    return json.dumps(ret_list)