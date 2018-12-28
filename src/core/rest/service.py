#!python
from flask import Flask, jsonify
from flask_cors import CORS
from core.util import web


def create_service(prefix):

    app = Flask('twitter service')
    p = prefix if prefix == '' or prefix[0] == '/'\
        else ('' if prefix is None else '/' + prefix)

    @app.route(p + '/user/<user>/icon', methods=['GET'])
    def get_user_icon(user):
        img_url = web.get_icon(user)
        ret = {'url': img_url}
        return jsonify(ret)

    @app.route(p + '/user/<user>', methods=['GET'])
    def get_user(user):
        img_url = web.get_icon(user)
        ret = {'url': img_url}
        return jsonify(ret)

    return app


def run(prefix=''):
    app = create_service(prefix)
    app.run(debug=True)
