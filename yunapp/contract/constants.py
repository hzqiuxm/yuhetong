# -*- coding: utf-8 -*-
ERROR_CODE = {
    'participants_check_error': 'Participants ids is not correct.',
    'NO_AUTH_CUR_CONTRACT': 'You have no auth for the current contract.',
    'CAN_NOT_DEL_NOT_NEW_CONTRACT': 'You can not del the contract not new stage.',
    'WRONG_PASS_WORD': 'User password wrong.',
    'NO_READ_PERM_CUR_CONTRACT': 'You can not read the current contract.',
    'AUTH_NOT_EXISTS':'this auth is not exists',
    'CONTRACT_STAGE_ERROR': 'Contract stage error',
    'CONTRACT_AUTH_TYPE_ERROR': 'No such auth type or you can not auth this type',
    'LONG_AUTH_ONLY_TO_SUB_USER': 'LONG_AUTH_ONLY_TO_SUB_USER',
    'ONLY_AUTH_TO_SUB_USER': 'ONLY_AUTH_TO_SUB_USER',
    'AUTH_PASSWD_ERROR': 'AUTH_PASSWD_ERROR',
    'NO_SIGN_AUTH': 'NO_SIGN_AUTH',
    'CONTRACT_AUTH_ERROR': 'CONTRACT_AUTH_ERROR',

}
PAGE_SIZE = 20
CONTRACT_FILE_TYPE = 2
DRAFT_FILE_TYPE = 3
CONTRACT_STAGE = {
    'NEW_CONTRACT': 1,
    'OWNER_CONFIRM': 2,
    'PARTICIPANTS_TAKE': 3,
    'PARTICIPANTS_CONFIRM': 4,
    'SIGN': 5,
}
CONTRACT_PART_STAGE = {
    'REJECT': -1,
    'TAKE': 1,
    'SIGN': 2,
}
CONTRACT_AUTH_TYPE = {
    'READ': 1,
    'WRITE': 2,
    'SIGN': 3,
}