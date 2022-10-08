from sqlalchemy import Column, Numeric, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class Crypto(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    symbol = Column(String,unique=True, index=True)
    price = Column(Numeric(10, 2))
    total_supply = Column(Numeric(10, 2))
    max_supply = Column(Numeric(10, 2))
    market_cap = Column(Numeric(10, 2))