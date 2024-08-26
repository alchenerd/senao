from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, crud
from .database import engine, get_database
from .schemas import AccountCreation, AccountValidation, Response


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return JSONResponse({'success': False, 'reason': exc.detail}, status_code=exc.status_code)


@app.post("/accounts", status_code=status.HTTP_201_CREATED, response_model=Response, 
          responses={status.HTTP_409_CONFLICT: {'model': Response}})
def create_account(account: AccountCreation, db: Session = Depends(get_database)):
    try:
        crud.create_account(db, account)
    except IntegrityError as e:
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={'success': False, 'reason': f"Username `{account.username}` already exists"})
    return {'success': True, 'reason': f'Account `{account.username}` created'}


@app.post("/accounts/validate/", response_model=Response,
          responses={
              status.HTTP_401_UNAUTHORIZED: {'model': Response},
              status.HTTP_429_TOO_MANY_REQUESTS: {'model': Response},
          })
def validate_account(account: AccountValidation, db: Session = Depends(get_database)):
    crud.validate_account(db, account)
    return {'success': True, 'reason': 'Validation successful'}
