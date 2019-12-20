import sqlalchemy as db
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import root.credentials as credentials
from root.entities import Player, Bet, Bank, Casino

from sqlalchemy import update


class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    cstr = 'postgresql://{user}:{password}@{hostname}/{database}'.format(
        user=credentials.username,
        password=credentials.password,
        hostname=credentials.host,
        database=credentials.database
    )
    engine = db.create_engine(cstr)
    Session = sessionmaker(bind=engine)
    
    def __init__(self):
        #self.connection = self.engine.connect()
        self.session = None
        print("DB Instance created")

    def __enter__(self):
        if self.session is not None:
            self.session.close() 
        self.session = self.Session()
        return self.session

    def __exit__(self, type, value, trace):
        if type is not None:
            print(f'Exeption happened in transaction:\n{value}')
            print(f'Trace:\n{trace}')
            self.session.rollback()
        else:
            print('transaction complete')
            self.session.commit()
        self.session.close()
        return True

    # Player

    def createPlayer(self, player):
        self.session.add(player)
        print("Player created successfully!")

    def updatePlayer(self, player_username, player_balance, player_passwd):
        dataToUpdate = {Player.balance: player_balance, Player.passwrd: player_passwd}
        playerData = self.session.query(Player).filter(Player.player_username == player_username)
        playerData.update(dataToUpdate)
        print("Player updated successfully!")

    def updatePlayerBalance(self, player_username, new_balance):
        dataToUpdate = {Player.balance: new_balance}
        playerData = self.session.query(Player).filter(Player.player_username == player_username)
        playerData.update(dataToUpdate)
        print("Player's balance updated successfully!")

    def fetchAllPlayers(self):
        players = self.session.query(Player).all()
        return players

    def fetchPlayer(self, player_username):
        player = self.session.query(Player).filter(Player.player_username == player_username).first()
        return player

    def deletePlayer(self, player_username):
        playerData = self.session.query(Player).filter(Player.player_username == player_username).first()
        self.session.delete(playerData)
        print("Player deleted successfully!")

    # Bet
    def createBet(self, bet):
        self.session.add(bet)
        print("Bet created successfully!")

    def updateBet(self, bet_id, bet_money, won_money, won_bet, bet_time):
        dataToUpdate = {Bet.bet_money: bet_money, Bet.won_money: won_money,
                        Bet.won_bet: won_bet, Bet.bet_time: bet_time}
        betData = self.session.query(Bet).filter(Bet.bet_id == bet_id)
        betData.update(dataToUpdate)
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
        print("Bet deleted successfully!")

    # Bank
    def createBank(self, bank):
        self.session.add(bank)
        print("Bank created successfully!")

    def updateBank(self, player_username, sold_time, sold_coins):
        dataToUpdate = {Bank.sold_time: sold_time, Bank.sold_coins: sold_coins}
        betData = self.session.query(Bank).filter(Bank.player_username == player_username)
        betData.update(dataToUpdate)
        print("Bank updated successfully!")

    def updateBankWithTime(self, player_username, sold_time, sold_coins):
        dataToUpdate = {Bank.sold_coins: sold_coins}
        bankData = self.session.query(Bank).filter(Bank.player_username == player_username).filter(
            Bank.sold_time == sold_time)
        bankData.update(dataToUpdate)
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
        print("Bank deleted successfully!")

    def createCasino(self, casino):
        self.session.add(casino)
        print("Casino created successfully!")

    def fetchAllCasinos(self):
        casinos = self.session.query(Casino).all()
        return casinos

    def fetchAllCasinoPlayerBets(self, player_username):
        bets = self.session.query(Casino).filter(Casino.player_username == player_username).all()
        return bets

    def close(self):
        self.session.close()
