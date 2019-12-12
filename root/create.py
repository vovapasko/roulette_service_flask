# creates data in db using sqlalchemy
from root.db import Database
from root.entities import Base, Player, Bank, Bet, Casino
import psycopg2

db = Database()
Base.metadata.create_all(db.engine)

player1 = Player(player_username='pashazopin1', balance=120, passwrd='passw')
player2 = Player(player_username='pashazopin2', balance=220, passwrd='mypassw')
player3 = Player(player_username='pashazopin3', balance=320, passwrd='newpassw')

db.createPlayer(player1)
db.createPlayer(player2)
db.createPlayer(player3)

bank1 = Bank(player_username='pashazopin1', sold_time='2018-06-22 14:10:25', sold_coins=100)
bank2 = Bank(player_username='pashazopin2', sold_time='2019-06-22 22:10:25', sold_coins=100)
bank3 = Bank(player_username='pashazopin3', sold_time='2019-06-22 21:10:25', sold_coins=100)

db.createBank(bank1)
db.createBank(bank2)
db.createBank(bank3)

bet1 = Bet(bet_id=1, bet_money=40, won_money=120, won_bet=False, bet_time='2019-06-22 21:10:25')
bet2 = Bet(bet_id=2, bet_money=40, won_money=120, won_bet=False, bet_time='2019-06-22 22:10:25')
bet3 = Bet(bet_id=3, bet_money=40, won_money=120, won_bet=True, bet_time='2019-06-22 23:10:25')

db.createBet(bet1)
db.createBet(bet2)
db.createBet(bet3)

casino1 = Casino(player_username='pashazopin1', bet_id=1)
casino2 = Casino(player_username='pashazopin2', bet_id=2)
casino3 = Casino(player_username='pashazopin3', bet_id=3)

db.createCasino(casino1)
db.createCasino(casino2)
db.createCasino(casino3)
