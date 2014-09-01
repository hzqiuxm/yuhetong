# -*- coding: utf-8 -*-
from yunapp.config import YOUR_FILE_STORE_FOLDER
FILE_STORE_FOLDER= YOUR_FILE_STORE_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])
STITIC_FILE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


ERROR_CODE = {
    'NOT_ALLOWED_FILE' : 'File type is not allowed',
    'NO_PERM_FOR_FILE' : 'The user has no perm to access the file',
    'NO_PERM_FOR_CONTRACT' : 'The user has no perm to access the contract'
}
