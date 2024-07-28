import functools
from flask import Response, Request, request, session
import os
import jwt
from api.constant import FETCH_UNIT, meta_df, user_history

def login_check(func):
    @functools.wraps(func)
    def wrapper(req, *args, **kwargs):
        
        is_logined = False
        print(user_history.keys())
        print(request.headers)
        try:
            user_id = request.headers.get("Authorization").strip().split(" ")[-1]
            user_id = int(user_id)
            request.user_id = user_id
            is_logined = True if f"user_id{user_id}" in user_history.keys() else False
        except:
            is_logined = False
        request.is_logined = is_logined
        
        return func(req,*args, **kwargs)
    return wrapper

def user_id_check(func):
    @functools.wraps(func)
    def wrapper(req, user_id, page):
        if(not(0 <= user_id <= 999)):
            return {}, 404

        return func(req, user_id, page)
    return wrapper

def page_check(func):
    @functools.wraps(func)
    def wrapper(req, page):
        print(req, page)
        if(page*FETCH_UNIT >= 72319):
            return {}, 404
        
        end_idx = (page+1)*FETCH_UNIT
        end_idx = end_idx if end_idx < 72319 else 72319

        return func(req, page, end_idx)
    return wrapper

def item_check(func):
    @functools.wraps(func)
    def wrapper(req, item_id):
        item = meta_df[meta_df["item_id"]==item_id]
        if(len(item) == 0):
            return {}, 404

        return func(req, item)
    return wrapper


def sequence_check(func):
    @functools.wraps(func)
    def wrapper(req, item_id):
        req_data = request.get_json()
        if("click_history" not in req_data.keys()):
            return {}, 400
        
        try:
            click_history = req_data.get("click_history")
            print(click_history)
            if(len(click_history) != 5):
                return {}, 400
        except IndexError as e:
            return {}, 400
        except TypeError as e:
            return {}, 400
        

        # * out of item embedding range
        for item in click_history:
            if(not(0<= item <= 72318)):
                return {}, 400
        

        return func(req, item_id)
    return wrapper