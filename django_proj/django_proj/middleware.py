from django.utils.deprecation import MiddlewareMixin


class CorsHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"

        return response
