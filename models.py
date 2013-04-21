from sqlalchemy import (
    Column,
    Boolean,
    DateTime,
    Integer,
    Text,
    String,
    ForeignKey,
    DateTime,
)

# You will need to point this to wherever your declarative base is
from ...models import Base

class ConnectFourProfile(Base):
    __tablename__ = 'connect_four_profiles'
    id                = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, primary_key=True)
    
    games_won         = Column(Integer)
    games_lost        = Column(Integer)
    games_drawn       = Column(Integer)
    games_in_progress = Column(Integer)

class ConnectFourGame(Base):
    __tablename__ = 'connect_four_games'
    id            = Column(Integer, primary_key=True)
    turn          = Column(Integer)
    
    started       = Column(DateTime, nullable=False)
    
    player1       = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    player2       = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    winner        = Column(Integer, ForeignKey("users.id"), nullable=True)
    current_state = Column(String, nullable=False)
    
    rematch = Column(Integer, ForeignKey("connect_four_games.id"))

class ConnectFourMove(Base):
    __tablename__ = 'connect_four_moves'
    id            = Column(Integer, primary_key=True)
    
    game          = Column(Integer, ForeignKey("connect_four_games.id"), nullable=False)
    player        = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    move          = Column(Integer, nullable=False)
    timestamp     = Column(DateTime, nullable=False)
