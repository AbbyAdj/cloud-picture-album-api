from fastapi import FastAPI, HTTPException, Request
from pg8000.dbapi import DatabaseError
from src.api.main import app


@app.exception_handler(DatabaseError)
def database_error_handler(request: Request, exc: DatabaseError):
    raise HTTPException(status_code=500, detail="Unknown Database Error")
