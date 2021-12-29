from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP



class Post(Base):

    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class User(Base):

    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    #items = relationship("Item", back_populates="owner")



class Memberships(Base):

    __tablename__ = "items"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    #owner_id = Column(Integer, ForeignKey("users.id"))
    #owner = relationship("User", back_populates="items")
