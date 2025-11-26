from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean,
    DateTime, Text
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# -------------------------
# User
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(Text, nullable=False)

    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )


# -------------------------
# Role
# -------------------------

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles"
    )


# -------------------------
# User <-> Role association
# -------------------------

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)


# -------------------------
# Session (Bearer Token)
# -------------------------

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True)  # UUID
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)

    user = relationship("User")
