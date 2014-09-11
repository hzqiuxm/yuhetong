# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import logging,io,StringIO, json, string, random, base64
from passlib.hash import sha256_crypt

from flask import Blueprint, jsonify, current_app, request,send_file, g
from flask.ext.login import current_user

from yunapp.orm.model import LxContract, LxFile, LxUser
from yunapp.orm import engine
from yunapp.logutils import StructedMsg
from yunapp.contract.utils import Yunhetong_HTMLParser
from yunapp.contract import constants
from yunapp.business.file import save_file, generate_file_uuid, \
    save_contract_file, delete_unused_file
from yunapp import config
from yunapp.yunapps import bcrypt

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
    c_part_num = request.values.get('part_num', 2, type = int)
    appendix_json = get_appendix_json(c_appendix)

    with engine.with_session() as ss:
        owner = ss.query(LxUser).get(current_user.id)
        c_fuuid = generate_file_uuid()
        c_path = save_contract_file(current_user.id, c_content, c_name, c_fuuid)
        draft_uuid = generate_file_uuid()
        draft_path = save_contract_file(current_user.id, c_content, c_name, draft_uuid)

        new_file = LxFile(fuuid=c_fuuid,
                          type=constants.CONTRACT_FILE_TYPE,
                          name=c_name,
                          fpath=c_path)
        ss.add(new_file)

        draft_file = LxFile(fuuid=draft_uuid,
                          type=constants.DRAFT_FILE_TYPE,
                          name=c_name,
                          fpath=draft_path)

        new_contract = LxContract(
            part_num = c_part_num,
            owner = owner,
            name = c_name,
            stage = 1,
            version = 1,
            contract_v1 = new_file,
            draft = draft_file,
            appendix = appendix_json,
            status = 1
        )
        ss.add(new_contract)

    return jsonify({'success': True, 'data': new_contract.id})

@contract.route('/<int:cid>', methods=['PUT'])
def update_contract(cid):
    """ Modify a contract
    :param contract_name, contract_content, participants, appendix. Only this four part can be modified
    :return contract_id
    """
    update_dict = dict()
    c_name = request.values.get('contract_name', '')
    if c_name:
        update_dict.update({'name': c_name})    # Update contract name    1
    c_appendix = request.values.get('appendix', '')
    if c_appendix:
        appendix_json = get_appendix_json(c_appendix)
        update_dict.update({'appendix': appendix_json}) # Update appendix   2

    is_new_version = request.values.get('new_version', '')
    c_content = request.values.get('contract_content', '')

    with engine.with_session() as ss:
        contract_to_update = ss.query(LxContract).get(cid)

        now_version = contract_to_update.version
        if c_content:
            draft_to_update = contract_to_update.draft
            save_contract_file(contract_to_update.owner_id, c_content,
                                   c_name, draft_to_update.fuuid)
            if is_new_version == 'True' and now_version < 5:
                c_fuuid = generate_file_uuid()       # Update contract file -- New file version  4
                c_path = save_contract_file(contract_to_update.owner_id,
                                            c_content, c_name, c_fuuid)
                new_file = LxFile(fuuid=c_fuuid,
                              type=constants.CONTRACT_FILE_TYPE,
                              name=c_name,
                              fpath=c_path)
                ss.add(new_file)
                update_dict.update({'version': now_version + 1})
                update_dict.update({'contract_v' + str(now_version): new_file})
            else:       # Update contract file -- Old file version      4
                file_to_update = contract_to_update.__getattribute__('contract_v' + str(now_version))
                save_contract_file(contract_to_update.owner_id, c_content,
                                   c_name, file_to_update.fuuid)
        contract_to_update.update(update_dict)

    return jsonify({'success':True, 'errorMsg':''})

@contract.route('/save_draft/<int:cid>', methods=['POST'])
def save_draft(cid):
    """ Save the draft of the contract
    :param content
    :return contract_id
    """
    d_content = request.values.get('contract_content', '')
    if not d_content:
        return jsonify({'success':False, 'errorMsg':'No content to save'})
    with engine.with_session() as ss:
        contract_to_update = ss.query(LxContract).get(cid)
        draft_to_update = contract_to_update.draft
        save_contract_file(contract_to_update.owner_id, d_content,
                               contract_to_update.name, draft_to_update.fuuid)
    return jsonify({'success':True, 'data': draft_to_update.id})

@contract.route('/owner_confirm_contract/<int:cid>', methods=['GET'])
def owner_confirm_contract(cid):
    """ The owner of the contract confirm the contract, and generate a url
    for others to sign
    :param cid
    :return contract_sign_url      include the contract id  and the sign_passwd
    """
    with engine.with_session() as ss:
        contract_to_confirm = ss.query(LxContract).get(cid)
        if contract_to_confirm.owner.id != current_user.id:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})
        confirm_dict = dict()
        confirm_dict['stage'] = constants.CONTRACT_STAGE['OWNER_CONFIRM']
        take_passwd = [random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase) for i in range(0,8) ]
        take_passwd = ''.join(take_passwd)
        confirm_dict['take_passwd'] = sha256_crypt.encrypt(take_passwd)
        contract_to_confirm.update(confirm_dict) # Do the update
        return_dict = dict()
        # sign_url = 'http://' + config.SERVER_NAME + \
        #     '/api/contract/take_contract/' + base64.encodestring(str(cid))
        sign_url = 'http://' + config.SERVER_NAME + \
            '/contract/take_contract/' + str(cid)
        return_dict['sign_url'] = sign_url
        return_dict['take_passwd'] = take_passwd
    return jsonify({'success':True, 'data': return_dict})

@contract.route('/<int:cid>', methods=['DELETE'])
def del_contract(cid):
    """ Delete the contract, check the
    :param cid
    :return contract_id
    """
    user_passwd  = request.values.get('passwd', '')
    # Check user password first
    with engine.with_session() as ss:
        contract_to_del = ss.query(LxContract).get(cid)

        if not bcrypt.check_password_hash(contract_to_del.owner.passwd,
                                       user_passwd):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'WRONG_PASS_WORD']})
        if contract_to_del.owner.id != current_user.id:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})
        if contract_to_del.stage > constants.CONTRACT_STAGE['SIGN']:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'CAN_NOT_DEL_SIGN_CONTRACT']})
        del_dict = dict('status', -1)
        contract_to_del.update(del_dict) # Do the delete
        delete_contract_related(contract_to_del, ss)
    return jsonify({'success': True, 'data': cid})

@contract.route('/part_read_contract/<int:cid>', methods=['POST'])
def part_read_contract(cid):
    """ Participates get the contract content and confirm it after read it
    :param cid
    :return contract_id
    """
    take_passwd  = request.values.get('take_passwd', '')
    with engine.with_session() as ss:
        cur_contract = ss.query(LxContract).get(cid)
        if not sha256_crypt.verify(take_passwd, cur_contract.take_passwd):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})

@contract.route('/part_take_contract/<int:cid>', methods=['POST'])
def part_read_contract(cid):
    """ Participates get the contract content and confirm it after read it
    :param cid
    :return contract_id
    """
    take_passwd  = request.values.get('take_passwd', '')
    with engine.with_session() as ss:


def check_new_contract_param(args):
    # TODO(wenwu) implement the function

    return { 'success': True }


def get_appendix_json(appendix_str):
    appendix_list = appendix_str.split(',')
    ret_list = list()
    for appendix_item in appendix_list:
        if appendix_item.isdigit():
            ret_list.append(appendix_item)
    return json.dumps(ret_list)

def delete_contract_related(contract_to_del, ss):
    """ Delete the related files of the contract
    :param contract_to_del
    """
    del_dict = dict('status', -1)
    if contract_to_del.draft:
        contract_to_del.draft.update(del_dict)
    if contract_to_del.contract_v1:
        contract_to_del.contract_v1.update(del_dict)
    if contract_to_del.contract_v2:
        contract_to_del.contract_v2.update(del_dict)
    if contract_to_del.contract_v3:
        contract_to_del.contract_v3.update(del_dict)
    if contract_to_del.contract_v4:
        contract_to_del.contract_v4.update(del_dict)
    if contract_to_del.contract_v5:
        contract_to_del.contract_v5.update(del_dict)
    appendix = json.loads(contract_to_del.appendix)
    for append in appendix:
        append_to_del = ss.query(LxFile).get(int(append))
        append_to_del.update(del_dict)
    return { 'success': True }
