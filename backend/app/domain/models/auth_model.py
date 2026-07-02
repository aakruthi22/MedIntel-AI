from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)  # Firebase UID
    email = Column(String, unique=True, index=True)

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id")) # SCOPED TO USER
    filename = Column(String)
    vector_id = Column(String)