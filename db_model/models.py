from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RequestIP(Base):
    __tablename__ = "request_ips"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    pred_label = Column(String)
    probability = Column(Float)
    elapsed_time = Column(Float)
    request_ip_id = Column(Integer, ForeignKey('request_ips.id'))
    request_ip = relationship("RequestIP")
    request_time = Column(DateTime(timezone=True), server_default=func.now())