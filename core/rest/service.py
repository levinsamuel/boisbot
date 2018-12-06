#!python
from flask import Flask, jsonify
from core.util import web

app = Flask('twitter service')


@app.route('/user/<user>/icon', methods=['GET'])
def get_user_icon(user):
    img_url = web.get_icon(user)
    ret = {'url': img_url}
    return jsonify(ret)


def run():
    app.run(debug=True)
