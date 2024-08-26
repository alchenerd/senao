from sqlalchemy import Column, Integer, String, TIMESTAMP

from .database import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    hash_salt = Column(String, nullable=False)
    fail_count = Column(Integer, default=0) # up to 5, reset on successful login or ban expired
    banned_since = Column(TIMESTAMP(timezone=True), nullable=True) # fixed ban duration = 1 min
