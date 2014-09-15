# -*- coding:utf-8 -*-

import os
import uuid
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from yunapp.config import CONTRACT_STORE_FOLDER
from yunapp.config import YOUR_FILE_STORE_FOLDER
FILE_STORE_FOLDER = YOUR_FILE_STORE_FOLDER


def save_file(file_upload, fuuid):
    """ Save file and return file path
    Currently use local file
    """
    try:
        file_path = os.path.join(FILE_STORE_FOLDER, fuuid)
        file_upload.save(file_path)
        return file_path
    except Exception, e:
        print e
        return None


def generate_file_uuid():
    """ Generate file name use uuid
    May be replace with other generate method
    """
    return uuid.uuid1().hex


def save_contract_file(owner_id, contract_content, contract_name, fuuid):
    """ Save file and return file path
    Currently use local file
    """
    try:
        contract = ET.Element("contract")
        owner = ET.SubElement(contract, "owner")
        name = ET.SubElement(contract, "name")
        content = ET.SubElement(contract, "content")
        owner.text = str(owner_id)
        name.text = contract_name
        content.text = contract_content
        contract_path = os.path.join(CONTRACT_STORE_FOLDER, fuuid)
        contract_file = ET.ElementTree(contract)
        contract_file.write(contract_path)

        return contract_path
    except Exception, e:
        print str(e)
        return None


def get_contract_content(fpath):
    try:
        tree = ET.parse(fpath)
        contract = tree.getroot()
        return contract[2].text
    except Exception, e:
        print str(e)
        return None


def delete_unused_file():
    pass