# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify
user = Blueprint('user', __name__)


@user.route('/<int:uid>', methods=['GET'])
def profile(uid):
    return_dict = {'success': True, 'uid':uid}
    return jsonify(return_dict)

@user.route('/register', methods=['POST'])
def register():
    return_dict = {'success': True, 'uid':'uid'}
    return jsonify(return_dict)

@user.route('/namecheck')
def namecheck():
    return_dict = {'success': True, 'errorMsg':''}
    return jsonify(return_dict)

@user.route('/login')
def login():
    return_dict = {'success': True, 'errorMsg':''}
    return jsonify(return_dict)