# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app
from flask.ext.login import LoginManager
from models import User
from yunapps import app
login_manager = LoginManager()
login_manager.init_app(app)

user = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


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