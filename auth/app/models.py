import datetime
import uuid
from typing import Optional

import sqlalchemy
from flask_jwt_extended import get_current_user
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class User(db.Model):
    '''
    User model for storing user related details
    
    '''

    __tablename__ = "app_users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str]
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    is_authenticated: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class TokenBlocklist(db.Model):
    '''
    TokenBlocklist model for revoked tokens
    
    '''

    __tablename__ = "token_blocklist"

    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, index=True, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("app_users.id"),
        default=lambda: get_current_user().id,
        nullable=False,
    )
    token_type: Mapped[str] = mapped_column(String(10), nullable=False)

    def __repr__(self) -> str:
        return f"TokenBlocklist(jti={self.jti}, token_type={self.token_type})"
