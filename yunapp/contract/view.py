# -*- coding: utf-8 -*-
__author__ = 'Seanwu'

import logging, io, StringIO, json, string, random, base64, datetime
from passlib.hash import sha256_crypt

from flask import Blueprint, jsonify, request, send_file
from flask.ext.login import current_user, login_required
from sqlalchemy import func

from yunapp.orm.model import LxContract, LxFile, LxUser, \
    LxContractParticipation, LxContractAuthorization
from yunapp.orm import engine
from yunapp.contract.utils import YunhetongHTMLParser
from yunapp.contract import constants
from yunapp.business import file as file_biz
from yunapp import config
from yunapp.yunapps import bcrypt

contract = Blueprint('contract', __name__)
app_logger = logging.getLogger('yunapp')
biz_logger = logging.getLogger('business')


@contract.route('/<filename>.docx', methods=['POST'])
def doc_create(filename):
    doc_file = StringIO.StringIO()
    parser = Yunhetong_HTMLParser(doc_file)
    data = request.values.get('data', '')

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
    :params contract_name, contract_content, appendix,  and part_num (default 2)
    :return new_contract_id
    """

    param_check_result = check_new_contract_param(request.values)
    if not param_check_result.get('success'):
        return jsonify(param_check_result)
    c_name = request.values.get('contract_name', '')
    c_content = request.values.get('contract_content', '')
    c_appendix = request.values.get('appendix', '')
    c_part_num = request.values.get('part_num', 2, type=int)
    # Default 2 participants

    appendix_json = get_appendix_json(c_appendix)

    with engine.with_session() as ss:
        # owner = ss.query(LxUser).get(current_user.id)
        c_fuuid = file_biz.generate_file_uuid()
        c_path = file_biz.save_contract_file(
            current_user.id, c_content, c_name, c_fuuid
        )
        draft_uuid = file_biz.generate_file_uuid()
        draft_path = file_biz.save_contract_file(
            current_user.id, c_content, c_name, draft_uuid
        )

        new_file = LxFile(fuuid=c_fuuid,
                          type=constants.CONTRACT_FILE_TYPE,
                          name=c_name,
                          fpath=c_path)
        ss.add(new_file)

        draft_file = LxFile(
            fuuid=draft_uuid,
            type=constants.DRAFT_FILE_TYPE,
            name=c_name,
            fpath=draft_path
        )

        new_contract = LxContract(
            part_num=c_part_num,
            owner=current_user,
            name=c_name,
            stage=constants.CONTRACT_STAGE['NEW_CONTRACT'],
            version=1,
            contract_v1=new_file,
            draft=draft_file,
            appendix=appendix_json,
            status=1
        )
        ss.add(new_contract)

    return jsonify({'success': True, 'data': new_contract.id})


@contract.route('/<int:cid>', methods=['PUT'])
def update_contract(cid):
    """ Modify a contract
    :params contract_name, contract_content, participants, appendix. Only
    this four part can be modified
    :return contract_id
    """
    update_dict = dict()
    c_name = request.values.get('contract_name', '')
    if c_name:
        update_dict.update({'name': c_name})    # Update contract name    1
    c_appendix = request.values.get('appendix', '')
    if c_appendix:
        appendix_json = get_appendix_json(c_appendix)
        update_dict.update({'appendix': appendix_json})  # Update appendix   2

    is_new_version = request.values.get('new_version', '')
    c_content = request.values.get('contract_content', '')


    with engine.with_session() as ss:
        contract_to_update = ss.query(LxContract).get(cid)

        now_version = contract_to_update.version
        if c_content:
            draft_to_update = contract_to_update.draft
            file_biz.save_contract_file(
                contract_to_update.owner_id, c_content,
                c_name, draft_to_update.fuuid
            )
            if is_new_version == 'True' and now_version < 5:
                c_fuuid = file_biz.generate_file_uuid()
                 # Update contract file -- New file version  4
                c_path = file_biz.save_contract_file(
                    contract_to_update.owner_id,
                    c_content, c_name, c_fuuid
                )
                new_file = LxFile(
                    fuuid=c_fuuid,
                    type=constants.CONTRACT_FILE_TYPE,
                    name=c_name,
                    fpath=c_path
                )
                ss.add(new_file)
                update_dict.update({'version': now_version + 1})
                update_dict.update({'contract_v' + str(now_version): new_file})
            else:       # Update contract file -- Old file version      4
                file_to_update = contract_to_update.__getattribute__(
                    'contract_v' + str(now_version)
                )
                file_biz.save_contract_file(
                    contract_to_update.owner_id, c_content,
                    c_name, file_to_update.fuuid
                )
        update_dict['stage'] = 1  # The owner confirm become invalid when
        # update
        contract_to_update.update(update_dict)

    return jsonify({'success': True, 'errorMsg': ''})


@contract.route('/save_draft/<int:cid>', methods=['POST'])
def save_draft(cid):
    """ Save the draft of the contract
    :params content
    :return contract_id
    """
    d_content = request.values.get('contract_content', '')
    if not d_content:
        return jsonify({'success': False, 'errorMsg': 'No content to save'})
    with engine.with_session() as ss:
        contract_to_update = ss.query(LxContract).get(cid)
        draft_to_update = contract_to_update.draft
        file_biz.save_contract_file(
            contract_to_update.owner_id, d_content,
            contract_to_update.name, draft_to_update.fuuid
        )
    return jsonify({'success': True, 'data': draft_to_update.id})


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
        take_passwd = [random.choice(
            string.digits + string.ascii_lowercase + string.ascii_uppercase
        ) for i in range(0, 8)]
        take_passwd = ''.join(take_passwd)
        confirm_dict['take_passwd'] = sha256_crypt.encrypt(take_passwd)
        # print confirm_dict
        contract_to_confirm.update(confirm_dict)  # Do the update

        # Add owner participation
        new_part = LxContractParticipation(
            contract=contract_to_confirm,
            user=current_user,
            stage=constants.CONTRACT_PART_STAGE['TAKE'],
            is_owner=1
        )
        ss.add(new_part)

    return_dict = dict()
    # sign_url = 'http://' + config.SERVER_NAME + \
    #     '/api/contract/take_contract/' + base64.encodestring(str(cid))
    sign_url = 'http://' + config.SERVER_NAME + \
        '/contract/take_contract/' + str(cid)
    return_dict['contract_take_url'] = sign_url
    return_dict['take_passwd'] = take_passwd
    return jsonify({'success': True, 'data': return_dict})


@contract.route('/<int:cid>', methods=['DELETE'])
def del_contract(cid):
    """ Delete the contract, check the
    :param cid
    :return contract_id
    """
    user_pass = request.values.get('passwd', '')
    # Check user password first
    with engine.with_session() as ss:
        contract_to_del = ss.query(LxContract).get(cid)

        if not bcrypt.check_password_hash(
                contract_to_del.owner.passwd, user_pass):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'WRONG_PASS_WORD']})
        if contract_to_del.owner.id != current_user.id:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})
        if contract_to_del.stage > constants.CONTRACT_STAGE['NEW_CONTRACT']:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'CAN_NOT_DEL_NOT_NEW_CONTRACT']})
        del_dict = dict(status=-1)
        contract_to_del.update(del_dict)  # Do the delete
        delete_contract_related(contract_to_del, ss)
    return jsonify({'success': True, 'data': cid})


@contract.route('/part_read_contract/<int:cid>', methods=['POST'])
def part_read_contract(cid):
    """ Participates get the contract content and confirm it after read it
    :param cid
    :return contract_id
    """
    take_pass = request.values.get('take_passwd', '')
    with engine.with_session() as ss:
        cur_contract = ss.query(LxContract).get(cid)
        if not sha256_crypt.verify(take_pass, cur_contract.take_passwd):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'WRONG_PASS_WORD']})
        now_version = cur_contract.version
        now_contract_file = cur_contract.__getattribute__(
            'contract_v' + str(now_version))
        # print now_contract_file.fpath
        contract_content = file_biz.get_contract_content(
            now_contract_file.fpath)
        return jsonify({'success': True, 'data': contract_content})


@contract.route('/part_take_contract/<int:cid>', methods=['POST'])
# @login_required
def part_take_contract(cid):
    """ Participates get the contract content and confirm it after read it
    :param cid
    :return contract_id
    """
    take_pass = request.values.get('take_passwd', '')
    with engine.with_session() as ss:
        cur_contract = ss.query(LxContract).get(cid)
        if not sha256_crypt.verify(take_pass, cur_contract.take_passwd):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'WRONG_PASS_WORD']})
        if cur_contract.stage != constants.CONTRACT_STAGE['OWNER_CONFIRM']:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'CONTRACT_STAGE_ERROR']})
        cur_user = ss.query(LxUser).get(current_user.id)
        new_part = LxContractParticipation(
            contract=cur_contract,
            user=cur_user,
            stage=constants.CONTRACT_PART_STAGE['TAKE']
        )
        ss.add(new_part)
        participation = ss.query(
            LxContractParticipation
        ).filter_by(
            contract_id=cid
        )
        if participation.count() == cur_contract.part_num:
            # If all participation take the contract the stage change to
            cur_contract.update(
                {'stage': constants.CONTRACT_STAGE['PARTICIPANTS_TAKE']}
            )
    return jsonify({'success': True, 'data': new_part.id})


@contract.route('/part_reject_contract/<int:cid>', methods=['POST'])
# @login_required
def part_reject_contract(cid):
    """ Participates get the contract content and confirm it after read it
    :param cid
    :return contract_id
    """
    take_passwd = request.values.get('take_passwd', '')
    with engine.with_session() as ss:
        cur_contract = ss.query(LxContract).get(cid)
        if not sha256_crypt.verify(take_passwd, cur_contract.take_passwd):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})
        if cur_contract.stage != constants.CONTRACT_STAGE['OWNER_CONFIRM']:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'CONTRACT_STAGE_ERROR']})
        # TODO reject contract send message to the owner and set stage to new
        #  contract
        cur_contract.update({'stage': constants.CONTRACT_STAGE['NEW_CONTRACT']})

    return jsonify({'success': True, 'data': 1})


@contract.route('/auth_contract/<int:cid>', methods=['POST'])
# @login_required
def auth_contract(cid):
    """ Participates can give others read and sign auth
        Owner can give others read, write and sign auth
    :param cid, auth_type(3 int param, the meaning of read write and sign)
         expire_days the days for the auth to expire 0 means forever
    :return take auth url
    """
    read_perm = request.values.get('read_perm', 0, type=int)
    write_perm = request.values.get('write_perm', 0, type=int)
    sign_perm = request.values.get('sign_perm', 0, type=int)
    expire_days = request.values.get('expire_days', 0, type=int)
    sub_user_id = request.values.get('sub_user_id', 0, type=int)
    long_term_auth = True
    gmt_expire = None
    if 0 < expire_days < 15:
        long_term_auth = False
        gmt_expire = datetime.datetime.now() + datetime.timedelta(expire_days)
        # print gmt_expire
    if long_term_auth and not sub_user_id:
        return jsonify(
            {'success': False,
             'errorMsg': constants.ERROR_CODE['LONG_AUTH_ONLY_TO_SUB_USER']})

    with engine.with_session() as ss:
        cur_contract = ss.query(LxContract).get(cid)
        partners = ss.query(LxContractParticipation).filter_by(contract_id=cid)
        sub_user = ss.query(LxUser).get(sub_user_id)

        if long_term_auth and (not sub_user.parent_id == current_user.id):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'ONLY_AUTH_TO_SUB_USER']})
        print cur_contract.owner.id
        owner_auth = (cur_contract.owner.id == current_user.id)
        partner_auth = False
        for partner in partners:
            if partner.user_id == current_user.id:
                partner_auth = True
        # print 'owner_auth:: ' + str(owner_auth)
        # print 'partner_auth:: ' + str(partner_auth)
        if not (owner_auth or partner_auth):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})
        if partner_auth and write_perm == 1:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_AUTH_CUR_CONTRACT']})

        auth_passwd = [random.choice(
            string.digits + string.ascii_lowercase + string.ascii_uppercase
        ) for i in range(0, 8)]
        auth_passwd = ''.join(auth_passwd)
        auth_hash = sha256_crypt.encrypt(auth_passwd)
        if not long_term_auth:
            new_auth = LxContractAuthorization(
                contract=cur_contract,
                read_perm=read_perm,
                write_perm=write_perm,
                sign_perm=sign_perm,
                auth_passwd=auth_hash,
                gmt_expire=gmt_expire,
                auth_own_user=current_user
            )
            ss.add(new_auth)
        else:
            new_auth = LxContractAuthorization(
                contract=cur_contract,
                read_perm=read_perm,
                write_perm=write_perm,
                sign_perm=sign_perm,
                auth_passwd=auth_hash,
                user=sub_user,
                auth_own_user=current_user
            )
            ss.add(new_auth)
    re_dict = dict()
    re_dict['auth_passwd'] = auth_passwd
    auth_url = 'http://' + config.SERVER_NAME + '/api/contract/take_auth/' \
               + str(new_auth.id)
    re_dict['auth_url'] = auth_url
    return jsonify({'success': True, 'data': re_dict})


@contract.route('/take_auth/<int:aid>', methods=['POST'])
# @login_required
def take_auth(aid):
    """ Take the auth of the given contract
    :param aid (auth id)
    :return contract_id
    """
    auth_passwd = request.values.get('auth_passwd', '')
    with engine.with_session() as ss:
        cur_auth = ss.query(LxContractAuthorization).get(aid)
        if not cur_auth:
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'AUTH_NOT_EXISTS']})
        if not sha256_crypt.verify(auth_passwd, cur_auth.auth_passwd):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'AUTH_PASSWD_ERROR']})
        update_dict = dict()
        update_dict['user'] = current_user
        cur_auth.update(update_dict)
    return jsonify({'success': True, 'data': cur_auth.contract_id})


@contract.route('/<int:cid>', methods=['GET'])
# @login_required
def get_contract(cid):
    """ Get contract according the contract_id (Check the perm of the user
    with the contract Owner or Participant can get, has read_perm for the
    contract can read）
    :param cid
    :return contract content
    """
    with engine.with_session() as ss:
        cur_contract = ss.query(LxContract).get(cid)
        is_owner = (cur_contract.owner.id == current_user.id)
        is_partner = ss.query(LxContractParticipation).filter_by(
            contract_id=cid, user_id=current_user.id
        ).first()
        has_auth = ss.query(LxContractAuthorization).filter_by(
            contract_id=cid, user_id=current_user.id
        ).first()
        if not (is_owner or is_partner or has_auth):
            return jsonify(
                {'success': False,
                 'errorMsg': constants.ERROR_CODE['NO_AUTH_CUR_CONTRACT']})

        re_contract = dict()
        re_contract['name'] = cur_contract.name
        re_contract['id'] = cur_contract.id
        re_contract['part_num'] = cur_contract.part_num
        now_version = cur_contract.version
        re_contract['version'] = now_version
        now_contract_file = cur_contract.__getattribute__(
            'contract_v' + str(now_version))
        contract_content = file_biz.get_contract_content(
            now_contract_file.fpath)
        re_contract['content'] = contract_content
        draft_content = file_biz.get_contract_content(cur_contract.draft.fpath)
        re_contract['draft_content'] = draft_content
        return jsonify({'success': True, 'data': re_contract})


@contract.route('/', methods=['GET'])
@login_required
def get_contracts():
    """ Get all contracts related to the current user
    :params cid
    :return contract_id
    """
    with engine.with_session() as ss:
        mine_contracts = list()
        my_part_contracts = list()
        my_auth_contracts = list()
        my_contracts = ss.query(
            LxContract.id, LxContract.name, LxContract.part_num
        ).filter_by(
            owner_id=current_user.id, status=1
        )
        for cont in my_contracts:
            mine_contracts.append(cont)
        my_participations = ss.query(LxContractParticipation).filter_by(
            user_id=current_user.id, status=1, is_owner=0
        )
        for part in my_participations:
            my_part_contracts.append(
                (part.contract.id, part.contract.name, part.contract.part_num)
            )
        my_authorizations = ss.query(LxContractAuthorization).filter_by(
            user_id=current_user.id, status=1
        )
        now = datetime.datetime.now()
        print len(my_auth_contracts)
        for auth in my_authorizations:
            print auth.gmt_expire > now
            if auth.gmt_expire > now:
                my_auth_contracts.append(
                    (auth.contract.id,
                     auth.contract.name,
                     auth.contract.part_num)
                )
        re_dict = dict()
        re_dict['mine_contracts'] = mine_contracts
        re_dict['part_contracts'] = my_part_contracts
        re_dict['auth_contracts'] = my_auth_contracts
    return jsonify({'success': True, 'data': re_dict})


@contract.route('/sign_contract/<int:cid>', methods=['POST'])
# @login_required
def sign_contract(cid):
    """ All Participates take the contract, Then all parts confirm the contract
    The contract stage must be 'PARTICIPANTS_TAKE': 3, the content must not
    change and the signer must be one of the participates or have sign auth.
    :param cid
    :return contract_id
    """
    with engine.with_session() as ss:
        is_part = ss.query(LxContractParticipation).filter_by(
            contract_id=cid, user_id=current_user.id
        ).first()
        has_sign_auth = ss.query(LxContractAuthorization).filter_by(
            contract_id=cid, user_id=current_user.id,
        ).first()
        if not (is_part or has_sign_auth):
            return jsonify({'success': False, 'errorMsg': constants.ERROR_CODE[
                'NO_SIGN_AUTH']})
        if is_part:
            is_part.update({'stage': constants.CONTRACT_PART_STAGE['SIGN']})
        elif has_sign_auth:
            present_part = ss.query(LxContractParticipation).filter_by(
                contract_id=cid, user_id=has_sign_auth.auth_own_user.id
            ).first()
            if not present_part:
                return jsonify(
                    {'success': False,
                     'errorMsg': constants.ERROR_CODE['CONTRACT_AUTH_ERROR']})
            present_part.update(
                {'stage': constants.CONTRACT_PART_STAGE['SIGN']})
        cur_contract = ss.query(LxContract).get(cid)
        cur_sign_num = ss.query(
            func.count(LxContractParticipation.id)
        ).filter_by(
            contract_id=cid, stage=constants.CONTRACT_PART_STAGE['SIGN']
        ).one()
        if cur_contract.part_num == cur_sign_num:
            cur_contract.update({'stage': constants.CONTRACT_STAGE['SIGN']})
        return jsonify({'success': True, 'data': cur_sign_num})


def check_new_contract_param(args):
    # TODO(wenwu) implement the function
    if not 'contract_name' in args.keys():
        return {'success': False,
                'errmsg': constants.ERROR_CODE['CONTRACT_NAME_NULL_ERROR']}
    return {'success': True}


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
    del_dict = dict(status=-1)
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
    return {'success': True}
