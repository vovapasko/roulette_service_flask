import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import root.credentials
from root.entities import Player, Bet, Bank, Casino

from sqlalchemy import update


class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    cstr = 'postgresql://{user}:{password}@{hostname}/{database}'.format(
        user=root.credentials.username,
        password=root.credentials.password,
        hostname=root.credentials.host,
        database=root.credentials.database
    )
    engine = db.create_engine(cstr)

    def __init__(self):
        self.connection = self.engine.connect()
        self.session = Session(bind=self.connection)
        print("DB Instance created")

    # Player

    def createPlayer(self, player):
        self.session.add(player)
        self.session.commit()
        print("Player created successfully!")

    def updatePlayer(self, player_username, player_balance, player_passwd):
        session = Session(bind=self.connection)
        dataToUpdate = {Player.balance: player_balance, Player.passwrd: player_passwd}
        playerData = session.query(Player).filter(Player.player_username == player_username)
        playerData.update(dataToUpdate)
        session.commit()
        print("Player updated successfully!")

    def updatePlayerBalance(self, player_username, new_balance):
        session = Session(bind=self.connection)
        dataToUpdate = {Player.balance: new_balance}
        playerData = session.query(Player).filter(Player.player_username == player_username)
        playerData.update(dataToUpdate)
        session.commit()
        # player = self.session.query(Player).filter(Player.player_username == player_username).first()
        # player.balance = new_balance
        # self.session.commit()
        print("Player's balance updated successfully!")

    def fetchAllPlayers(self):
        self.session = Session(bind=self.connection)
        players = self.session.query(Player).all()
        return players

    def fetchPlayer(self, player_username):
        self.session = Session(bind=self.connection)
        player = self.session.query(Player).filter(Player.player_username == player_username).first()
        return player

    def deletePlayer(self, player_username):
        session = Session(bind=self.connection)
        playerData = session.query(Player).filter(Player.player_username == player_username).first()
        session.delete(playerData)
        session.commit()
        print("Player deleted successfully!")

    # Bet
    def createBet(self, bet):
        self.session.add(bet)
        self.session.commit()
        print("Bet created successfully!")

    def updateBet(self, bet_id, bet_money, won_money, won_bet, bet_time):
        dataToUpdate = {Bet.bet_money: bet_money, Bet.won_money: won_money,
                        Bet.won_bet: won_bet, Bet.bet_time: bet_time}
        betData = self.session.query(Bet).filter(Bet.bet_id == bet_id)
        betData.update(dataToUpdate)
        self.session.commit()
        print("Bet updated successfully!")

    def fetchAllBets(self):
        bets = self.session.query(Bet).all()
        return bets

    def fetchBet(self, bet_id):
        bet = self.session.query(Bet).filter(Bet.bet_id == bet_id).first()
        return bet

    def deleteBet(self, bet_id):
        betData = self.session.query(Bet).filter(Bet.bet_id == bet_id).first()
        self.session.delete(betData)
        self.session.commit()
        print("Bet deleted successfully!")

    # Bank
    def createBank(self, bank):
        self.session.add(bank)
        self.session.commit()
        print("Bank created successfully!")

    def updateBank(self, player_username, sold_time, sold_coins):
        dataToUpdate = {Bank.sold_time: sold_time, Bank.sold_coins: sold_coins}
        betData = self.session.query(Bank).filter(Bank.player_username == player_username)
        betData.update(dataToUpdate)
        self.session.commit()
        print("Bank updated successfully!")

    def updateBankWithTime(self, player_username, sold_time, sold_coins):
        dataToUpdate = {Bank.sold_coins: sold_coins}
        bankData = self.session.query(Bank).filter(Bank.player_username == player_username).filter(
            Bank.sold_time == sold_time)
        bankData.update(dataToUpdate)
        self.session.commit()
        print("Bank updated successfully!")

    def fetchAllBanks(self):
        banks = self.session.query(Bank).all()
        return banks

    def fetchBank(self, player_username, sold_time):
        bank = self.session.query(Bank).filter(Bank.player_username == player_username).filter(
            Bank.sold_time == sold_time).first()
        return bank

    def deleteBank(self, player_username, sold_time):
        bankData = self.session.query(Bank).filter(Bank.player_username == player_username).filter(
            Bank.sold_time == sold_time).filter().first()
        self.session.delete(bankData)
        self.session.commit()
        print("Bank deleted successfully!")

    def createCasino(self, casino):
        self.session.add(casino)
        self.session.commit()
        print("Casino created successfully!")

    def fetchAllCasinos(self):
        casinos = self.session.query(Casino).all()
        return casinos
