import pandas as pd

def score_request(player_1, player_2, tourn):

  db_2017 = pd.read_csv('mon_db.csv')

  interest = db_2017[(db_2017.tourney_name == tourn) & (db_2017.winner_name == player_1) & (db_2017.loser_name == player_2)]
  if interest.empty:
    interest = db_2017[(db_2017.tourney_name == tourn) & (db_2017.winner_name == player_2) & (db_2017.loser_name == player_1)]
    winner = player_2
    loser = player_1
  else:
    winner = player_1
    loser = player_2

  return 'in ' + tourn + ', ' + winner + ' beat ' + loser + ': ' + interest['score'].values[0]

pl1 = 'Roger Federer'
pl2 = 'Rafael Nadal'
tur = 'Australian Open'
topr = score_request(pl1,pl2,tur)
print(topr)
