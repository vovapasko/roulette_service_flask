from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship

Base = declarative_base()


class Player(Base):
    __tablename__ = "player"
    player_username = Column(String, primary_key=True)
    balance = Column(Float, nullable=False)
    passwrd = Column(String(64), nullable=False)
    banks = relationship("Bank", cascade="all, delete", passive_deletes=True)
    casinos = relationship("Casino", cascade="all, delete", passive_deletes=True)


class Bank(Base):
    __tablename__ = "bank"
    player_username = Column(String, ForeignKey(Player.player_username, ondelete="cascade"), primary_key=True)
    sold_time = Column(TIMESTAMP, primary_key=True)
    sold_coins = Column(Float, nullable=False)


class Bet(Base):
    __tablename__ = "bet"
    bet_id = Column(String, primary_key=True)
    bet_money = Column(Float, nullable=False)
    won_money = Column(Float, nullable=False)
    won_bet = Column(Boolean, nullable=False)
    bet_time = Column(TIMESTAMP, nullable=False)
    bet_color = Column(String, nullable=False)
    bet_number = Column(Integer, nullable=True)
    casinos = relationship("Casino", cascade="all, delete", passive_deletes=True)


class Casino(Base):
    __tablename__ = "casino"
    player_username = Column(String, ForeignKey(Player.player_username, ondelete="cascade"), primary_key=True)
    bet_id = Column(String, ForeignKey(Bet.bet_id, ondelete="cascade"), primary_key=True)
