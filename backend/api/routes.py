from datetime import datetime, timezone, timedelta
import sys
from ml.load import *
from functools import wraps
from flask import request, redirect, url_for
from flask_restx import Api, Resource, fields
import pandas as pd
from api.middleware import *
from api.infer import *
from api.constant import *

rest_api = Api(version="1.0", title="KKARROT Documentation")


# * load deep learning model
ttr_rec = load_twotower("ml/parameters/twotower.pth").cuda()
ll_rec = load_linkprediction("ml/parameters/linkprediction.pth").cuda()
session_rec = load_session("ml/parameters/session.pth").cuda()

# * click_history for sequence recommendation
product_model = rest_api.model('ProductModel', {
                                                "click_history": fields.List(fields.Integer(required=True)),
                                            })

# * user_id for feed recommendation
home_model = rest_api.model('HomeModel', {"user_id": fields.Integer(required=True, min_length=1, max_length=1),
                                            })

# * login infokmration
login_model = rest_api.model('LoginModel', {"user_id": fields.Integer(required=True, min_length=1, max_length=1),
                                            })

@rest_api.route('/api/view/home/<int:user_id>/p/<int:page>')
class Home(Resource):
    @user_id_check
    @login_check
    @page_check
    def get(self, user_id, page, end_idx):
        """Get Hottest products."""
        # print("from Home", session.keys())
        # print(request.is_logined)
        return {"success": True,
                "user_id": user_id,
                "page": page,
                "feed_lst": meta_df.iloc[page*FETCH_UNIT:end_idx].to_json(orient="records")
                }, 200

    @user_id_check
    @login_check
    def post(self, user_id, _):
        print(request)
        """Get recommended products."""
        if(not request.is_logined):
            return {}, 401

        # * retrieve
        retrieve_idx = retrieve(ttr_rec, user_id, ITEM_ID_LST)
        
        # * scoring
        scores = link_prediction(ll_rec, user_id, retrieve_idx, graph)
        
        # * ordering
        popularity = RATING_LST[retrieve_idx]
        popularity = (popularity - popularity.min())/(popularity.max()-popularity.min())
        scores = scores*ALPHA + popularity*(1-ALPHA)

        top_idx = torch.argsort(scores, descending=True)
        top_item_idx = retrieve_idx[top_idx]

        # ! optimize with sqlie needed!
        top_items = pd.merge(pd.DataFrame(top_item_idx, columns=['item_id']),meta_df, on='item_id', how='left')

        return {"success": True,
                "feed_lst": top_items.to_json(orient="records")
                }, 200
    
    
@rest_api.route('/api/view/product/<int:item_id>')
class Product(Resource):
    @item_check
    @login_check
    def get(self, item):
        """Get detailed description of the product."""
        if(not request.is_logined):
            return {}, 401
        user_history[f"user_id{request.user_id}"].append(item["item_id"].tolist()[0])
        click_history = user_history[f"user_id{request.user_id}"]
        if(len(click_history) < 5):
            feed_lst = meta_df.iloc[0:FETCH_UNIT].to_json(orient="records")
        else:
            click_history = click_history[-5:]
            user_history[f"user_id{request.user_id}"] = click_history
            top_pred_idx = sequence_recommend(session_rec, click_history)
            top_items = pd.merge(pd.DataFrame(top_pred_idx, columns=['item_id']),meta_df, on='item_id', how='left')
            feed_lst= top_items.to_json(orient="records")

        return {"success": True,
                "item": item.to_json(orient="records"),
                "feed_lst": feed_lst,
                }, 200
    
    @rest_api.expect(product_model, validate=True)
    @sequence_check
    @login_check
    def post(self, item_id):
        """Get recommended products via click history."""
        if(not request.is_logined):
            return {}, 401
        
        req_data = request.get_json()
        click_history = req_data.get("click_history")
        top_pred_idx = sequence_recommend(session_rec, click_history)

        # ! optimize with sqlie needed!
        top_items = pd.merge(pd.DataFrame(top_pred_idx, columns=['item_id']),meta_df, on='item_id', how='left')

        return {"success": True,
                "feed_lst": top_items.to_json(orient="records")
                }, 200
    

@rest_api.route('/api/login')
class Login(Resource):

    @rest_api.expect(login_model, validate=True)
    def post(self):
        """Get loginned user id and save it to session"""
        req_data = request.get_json()
        user_id = req_data.get("user_id")
        user_history[f"user_id{user_id}"] = []
        print("from login", user_history.keys())
        return {"success": True,
                }, 200