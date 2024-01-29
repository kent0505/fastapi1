from starlette.middleware.base import BaseHTTPMiddleware
from src.utils                 import log
from http                      import HTTPStatus


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        method      = request.method
        url_path    = str(request.url).replace(str(request.base_url), '/')
        status_code = response.status_code
        code_desc   = HTTPStatus(status_code).phrase

        # print(f"{method} {url_path} {status_code} {code_desc}")
        log(f"{method} {url_path} {status_code} {code_desc}")
        return response