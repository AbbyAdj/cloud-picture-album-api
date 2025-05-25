from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pg8000.dbapi import DatabaseError
from botocore.exceptions import ClientError


def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred."},
    )

def return_404_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

def aws_client_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"detail": "AWS Client Error Occured."},
    )



