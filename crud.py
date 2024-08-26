import bcrypt
from fastapi import status
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, schemas


def create_account(db: Session, user: schemas.AccountCreation) -> models.Account:
    username = user.username
    password = user.password

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(str.encode(password, 'utf-8'), salt)

    db_account = models.Account(username=username, password=hashed.hex(), hash_salt=salt.hex())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


def validate_account(db: Session, user: schemas.AccountValidation) -> models.Account:
    def raise_401():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    def raise_429(when):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts since {when}",
        )

    username = user.username
    password = user.password
    now = datetime.now()
    
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if not db_account:
        raise_401()
    
    if db_account.banned_since and now - db_account.banned_since <= timedelta(minutes=1):
        raise_429(db_account.banned_since)

    salt = bytes.fromhex(db_account.hash_salt)
    hashed = bcrypt.hashpw(str.encode(password, 'utf-8'), salt)
    authenticated = hashed.hex() == db_account.password
    
    if not authenticated:
        banned = False
        db_account.fail_count += 1
        if db_account.fail_count >= 5:
            banned = True
            db_account.fail_count = 0
            db_account.banned_since = now
        db.commit()
        db.refresh(db_account)
        if banned:
            raise_429(db_account.banned_since)
        else:
            raise_401()
    else:
        db_account.fail_count = 0
        db_account.banned_since = None
        db.commit()
        db.refresh(db_account)

    return db_account
