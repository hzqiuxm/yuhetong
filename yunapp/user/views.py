# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/')
def index():
    pass