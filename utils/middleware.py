from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class ResponseMiddleware(MiddlewareMixin):
    """
    自定义响应数据格式
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                msg = response.data
                code = 1
                response.data = {'code': code, 'msg': msg}
            elif response.status_code == 200 or response.status_code == 201:
                msg = 'success'
                code = 0
                data = response.data
                response.data = {'code': code, 'msg': msg, 'data': data}
            else:
                return response
            response.content = response.rendered_content
        return response
