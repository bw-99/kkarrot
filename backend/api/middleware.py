import functools
from flask import Response, Request, request
import os
import jwt

def user_id_check(func):
    @functools.wraps(func)
    def wrapper(req, user_id, page):
        if(not(0 <= user_id <= 999)):
            return {}, 404

        return func(req, user_id, page)
    return wrapper

def page_check(func):
    @functools.wraps(func)
    def wrapper(req, user_id, page):
        print(req, user_id, page)
        if(page*10 >= 72319):
            return {}, 404
        
        end_idx = (page+1)*10
        end_idx = end_idx if end_idx < 72319 else 72319

        return func(req, user_id, page, end_idx)
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
            if(len(click_history) != 3):
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