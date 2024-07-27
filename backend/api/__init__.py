# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, json
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .routes import rest_api
from flask_session import Session
# from flask_session import Session
app = Flask(__name__)
load_dotenv()


app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False

Session(app)
rest_api.init_app(app)
CORS(app)
app.debug=True



"""
   Custom responses
"""

@app.after_request
def after_request(response):
    """
       Sends back a custom error with {"success", "msg"} format
    """

    if int(response.status_code) >= 400:
        response_data = json.loads(response.get_data())
        if "errors" in response_data:
            response_data = {"success": False,
                             "msg": list(response_data["errors"].items())[0][1]}
            response.set_data(json.dumps(response_data))
        response.headers.add('Content-Type', 'application/json')
    return response
