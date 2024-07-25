from datetime import datetime, timezone, timedelta
import sys

from ml.load import *
from functools import wraps
from flask import request, redirect, url_for
from flask_restx import Api, Resource, fields
import pandas as pd

rest_api = Api(version="1.0", title="Kkarrot Documentation")

# * load data
meta_df = pd.read_pickle("data/processed/item_meta.pkl")


# * load deep learning model
ttr_rec = load_twotower("ml/parameters/twotower.pth")
ll_rec = load_linkprediction("ml/parameters/linkprediction.pth")
session_rec = load_session("ml/parameters/session.pth")

# * click_history for sequence recommendation
product_model = rest_api.model('ProductModel', {
                                                "click_history": fields.Integer(required=True, min_length=3, max_length=100),
                                            })

# * user_id for feed recommendation
home_model = rest_api.model('HomeModel', {"user_id": fields.Integer(required=True, min_length=1, max_length=1),
                                            })



@rest_api.route('/api/view/home/<int:user_id>/p/<int:page>')
class Home(Resource):
    def get(self, user_id, page):
        """Get Hottest products."""
        return {"success": True,
                "user_id": user_id,
                "page": page,
                "feed_lst": meta_df.iloc[page*10:(page+1)*10].to_json(orient="records")
                }, 200
    
    def post(self, user_id, page):
        """Get recommended products."""
        return {"success": True,
                "page": page,
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

