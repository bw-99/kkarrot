# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone, timedelta

from functools import wraps

from flask import request, redirect, url_for
from flask_restx import Api, Resource, fields

import requests

rest_api = Api(version="1.0", title="Users API")


# * click_history for sequence recommendation
product_model = rest_api.model('ProductModel', {
                                                "click_history": fields.Integer(required=True, min_length=3, max_length=100),
                                            })

# * user_id for feed recommendation
home_model = rest_api.model('HomeModel', {"user_id": fields.Integer(required=True, min_length=1, max_length=1),
                                            })



@rest_api.route('/api/view/home/<int:user_id>')
class Home(Resource):
    def get(self, user_id):
        """Get recent products."""
        return {"success": True,
                "user_id": user_id,
                }, 200
    
    def post(self, user_id):
        """Get recommended products."""
        return {"success": True,
                "user_id": user_id,
                "feed_lst": []
                }, 200
    
@rest_api.route('/api/view/product/<string:item_id>')
class Product(Resource):

    def get(self, item_id):
        """Get detailed description of the product."""
        return {"success": True,
                "item_id": item_id,
                }, 200
    
    @rest_api.expect(product_model, validate=True)
    def post(self, item_id):
        """Get recommended products via click history."""
        return {"success": True,
                "item_id": item_id,
                "feed_lst": []
                }, 200

