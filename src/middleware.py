from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import logging
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware


the_logger = logging.getLogger("uvicorn.access")
the_logger.disabled = True


def register_the_middleware(app: FastAPI):

    @app.middleware("http")
    async def the_authorization(request: Request, call_the_next):
        print("second middleware")
        if not "Authorization" in request.headers:
            return JSONResponse(
                content= {
                    "message": "Not Authenticated",
                    "resolution": "Please provide the Valid Access Token..."
                },
                status_code= status.HTTP_401_UNAUTHORIZED
            )

        print(request.headers)
        the_response = await call_the_next(request)
        
        return the_response
    
    
    @app.middleware("http")
    async def the_logging_middleware(request: Request, call_the_next):
        print("first middleware")
        start_time = time.time()

        the_response = await call_the_next(request)

        the_processing_time = time.time() - start_time

        the_message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {the_response.status_code} - {the_processing_time}"

        print(the_message)

        return the_response
    
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins= ["*"],
        allow_methods= ["*"],
        allow_headers= ["*"],
        allow_credentials= True
    )
    
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts = ["localhost", "127.0.0.1"]
    )
    
    
