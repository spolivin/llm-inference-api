from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class BadRequestTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if 400 <= response.status_code < 500:
            if response.status_code == 404:
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": f"Resource not found ({response.status_code} Bad Request)"
                    },
                )
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "error": f"Error parsing the request ({response.status_code} Bad Request)"
                    },
                )

        return response
