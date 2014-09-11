# -*- coding: utf-8 -*-
ERROR_CODE = {
    'participants_check_error': 'Participants ids is not correct.',
    'NO_AUTH_CUR_CONTRACT': 'You have no auth for the current contract.',
    'CAN_NOT_DEL_SIGN_CONTRACT': 'You can not del the contract for it is signed.',
    'WRONG_PASS_WORD': 'User password wrong.',
    'NO_READ_PERM_CUR_CONTRACT': 'You can not read the current contract.'
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
