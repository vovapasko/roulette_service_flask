# creates data in db using sqlalchemy
from root import tools
from root.db import Database
from root.entities import Base, Player, Bank, Bet, Casino
import psycopg2

from root.tools import get_bet_id

db = Database()
Base.metadata.create_all(db.engine)

#
# player1 = Player(player_username='pashazopin1', balance=120, passwrd='passw')
# player2 = Player(player_username='pashazopin2', balance=220, passwrd='mypassw')
# player3 = Player(player_username='pashazopin3', balance=320, passwrd='newpassw')
#
# with db:
#     db.createPlayer(player1)
#     db.createPlayer(player2)
#     db.createPlayer(player3)
#
# bank1 = Bank(player_username='pashazopin1', sold_time='2018-06-22 14:10:25', sold_coins=100)
# bank2 = Bank(player_username='pashazopin2', sold_time='2019-06-22 22:10:25', sold_coins=100)
# bank3 = Bank(player_username='pashazopin3', sold_time='2019-06-22 21:10:25', sold_coins=100)
# #
# with db:
#     db.createBank(bank1)
#     db.createBank(bank2)
#     db.createBank(bank3)
# # #
# bet1id = get_bet_id()
# bet2id = get_bet_id()
# bet3id = get_bet_id()
# bet1 = Bet(bet_id=bet1id, bet_money=40, won_money=120, won_bet=False, bet_time='2019-06-22 21:10:25', bet_color='red', bet_number=None)
# bet2 = Bet(bet_id=bet2id, bet_money=40, won_money=120, won_bet=False, bet_time='2019-06-22 22:10:25', bet_color='black', bet_number=None)
# bet3 = Bet(bet_id=bet3id, bet_money=40, won_money=120, won_bet=True, bet_time='2019-06-22 23:10:25', bet_color='red', bet_number=None)
#
# with db:
#     db.createBet(bet1)
#     db.createBet(bet2)
#     db.createBet(bet3)
#
# casino1 = Casino(player_username='pashazopin1', bet_id=bet1id)
# casino2 = Casino(player_username='pashazopin2', bet_id=bet2id)
# casino3 = Casino(player_username='pashazopin3', bet_id=bet3id)
#
# with db:
#     db.createCasino(casino1)
#     db.createCasino(casino2)
#     db.createCasino(casino3)

# with db:
#     bets = db.fetchAllCasinoPlayerBets('user')
#     print()
