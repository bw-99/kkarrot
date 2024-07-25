import functools
from flask import Response, Request
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