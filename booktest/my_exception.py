from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db import DatabaseError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # 1、调用系统方法，处理了APIException的异常，或其子类异常
    response = exception_handler(exc, context)
    # 判断Respone是否有值
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        if isinstance(exc, DatabaseError):
            response = Response("数据库异常")
        else:
            response = Response("其它异常")
    return response