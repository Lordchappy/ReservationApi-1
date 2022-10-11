from sqlite3 import Date
from ..database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column,Integer, String , Boolean,VARCHAR,DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True , nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String,nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    # is_verified = Column(Boolean , default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # rental_id = Column(Integer, ForeignKey("Reservations.id", ondelete="CASCADE"))
    # reservations = relationship("Reservations",ForeignKey("Reservations.id"))


class Reservations(Base):
    __tablename__ = "Reservations"
    id = Column(Integer, primary_key= True , nullable=False)
    name = Column(String(250),nullable=False)
    checkin = Column(TIMESTAMP(timezone=True), server_default=text('now()')) 
    checkout = Column(TIMESTAMP(timezone=True), server_default=text('now()')) 
    booking_time = Column(DateTime,nullable=False)
    Room_number = Column(Integer,nullable=False,unique=True)
    is_active = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner= relationship("User")
 

