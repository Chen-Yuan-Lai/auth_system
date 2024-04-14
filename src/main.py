from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .auth import models
from .auth.router import router as auth_router
from .database import engine
from .exceptions import NewHTTPException
from .log import init_logging, logger

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

init_logging()


@app.middleware("http")
async def get_request(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code < 400:
            logger.info("Info")
        return response
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "reason": "Internal Server Error"},
        )


@app.exception_handler(NewHTTPException)
async def unicorn_exception_handler(request: Request, exc: NameError):
    logger.error(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "reason": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]

    error_message: str

    if error["type"] == "string_too_short":
        error_message = f"{error['loc'][1]} is too short"
    elif error["type"] == "string_too_long":
        error_message = f"{error['loc'][1]} is too long"
    elif error["type"] == "missing":
        error_message = f"{error['loc'][1]} is is required"
    else:
        error_message = "Invalid password: must include at least one lowercase letter, one uppercase letter, and one digit."

    logger.error(error_message)

    return JSONResponse(
        status_code=422, content={"success": False, "reason": error_message}
    )


app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])
