import pandas as pd

def head_to_head(player_1, player_2):
  db_2017 = pd.read_csv('mon_db.csv')
  pl1_win_db = db_2017[(db_2017.winner_name == player_1) & (db_2017.loser_name == player_2)]
  pl2_win_db = db_2017[(db_2017.winner_name == player_2) & (db_2017.loser_name == player_1)]
  print(len(pl2_win_db))
  if len(pl1_win_db) == 0 and len(pl2_win_db) == 0:
    return player_1 + ' and ' + player_2 + ' did not yet meet this year in an official match'
  elif len(pl1_win_db) > len(pl2_win_db):
    return 'Since the beginning of the year, ' + player_1 + ' leads the head-to-head over ' + player_2 + ' by ' + str(len(pl1_win_db)) + ' to ' + str(len(pl2_win_db))
  elif len(pl2_win_db) > len(pl1_win_db):
    return 'Since the beginning of the year, ' + player_2 + ' leads the head-to-head over ' + player_1 + ' by ' + str(len(pl2_win_db)) + ' to ' + str(len(pl1_win_db))
  else:
    return player_1 + ' and ' + player_2 + ' are tied this year, with ' + str(len(pl2_win_db)) + ' wins each.'

print(head_to_head('Kei Nishikori', 'Grigor Dimitrov'))
