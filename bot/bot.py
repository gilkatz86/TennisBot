# coding: utf-8

import os
import recastai
import pandas as pd

from flask import jsonify

def score_request(player_1, player_2, tourn):

  db_2017 = pd.read_csv('mon_db.csv')

  interest = db_2017[(db_2017.tourney_name == tourn) & (db_2017.winner_name == player_1) & (db_2017.loser_name == player_2)]
  if interest.empty:
    interest = db_2017[(db_2017.tourney_name == tourn) & (db_2017.winner_name == player_2) & (db_2017.loser_name == player_1)]
    if interest.empty:
      if (tourn == 'Australian Open') or (tourn == 'US Open'):
        tourn = 'the ' + tourn
      return 'It seems that ' + player_1 + ' and ' + player_2 + 'did not meet at ' + tourn
    winner = player_2
    loser = player_1
  else:
    winner = player_1
    loser = player_2
  if (tourn == 'Australian Open') or (tourn == 'US Open'):
    tourn = 'the ' + tourn

  return 'In ' + tourn + ', ' + winner + ' beat ' + loser + ': ' + interest['score'].values[0]

def last_match(player, tourn = None):

  db_2017 = pd.read_csv('mon_db.csv')
  if tourn == None:
    interest = db_2017[(db_2017.winner_name == player) | (db_2017.loser_name == player)]
    if interest.empty:
      return player + ' did not play a professional match this year'
    ind = interest.iloc[-1].name
    if db_2017.iloc[ind].winner_name == player:
      my_reply = 'In his last match, ' + player + ' beat ' + db_2017.iloc[ind].loser_name + ' in the ' + db_2017.iloc[ind,30] + ' of ' + db_2017.iloc[ind].tourney_name + ': ' + db_2017.iloc[ind].score
    else:
      my_reply = 'In his last match, ' + player + ' lost to ' + db_2017.iloc[ind].winner_name  + ' in the ' + db_2017.iloc[ind,30] + ' of ' + db_2017.iloc[ind].tourney_name + ': ' + db_2017.iloc[ind].score
  else:
    interest = db_2017[((db_2017.winner_name == player) | (db_2017.loser_name == player)) & (db_2017.tourney_name == tourn)]
    if interest.empty:
        return player + 'did not play this tournament'
    ind = interest.iloc[-1].name
    if (db_2017.iloc[ind,30] == 'F') and (db_2017.iloc[ind].winner_name == player):
      my_reply = player + ' won the tournament, beating ' + db_2017.iloc[ind].loser_name + ' in the final: ' + db_2017.iloc[ind].score
    else:
      my_reply = player + ' lost in the ' + db_2017.iloc[ind,30] + ' to ' + db_2017.iloc[ind].winner_name + ': ' + db_2017.iloc[ind].score
  return my_reply

def head_to_head(player_1, player_2):
  db_2017 = pd.read_csv('mon_db.csv')
  pl1_win_db = db_2017[(db_2017.winner_name == player_1) & (db_2017.loser_name == player_2)]
  pl2_win_db = db_2017[(db_2017.winner_name == player_2) & (db_2017.loser_name == player_1)]
  if (len(pl1_win_db) == 0) and (len(pl2_win_db) == 0):
    return player_1 + ' and ' + player_2 + ' did not yet meet this year in an official match'
  elif len(pl1_win_db) > len(pl2_win_db):
    return 'Since the beginning of the year, ' + player_1 + ' leads the head-to-head over ' + player_2 + ' by ' + str(len(pl1_win_db)) + ' to ' + str(len(pl2_win_db))
  elif len(pl2_win_db) > len(pl1_win_db):
    return 'Since the beginning of the year, ' + player_2 + ' leads the head-to-head over ' + player_1 + ' by ' + str(len(pl2_win_db)) + ' to ' + str(len(pl1_win_db))
  else:
    return player_1 + ' and ' + player_2 + ' are tied this year, with ' + str(len(pl2_win_db)) + ' wins each.'

def player_stats(player):
  db_2017 = pd.read_csv('mon_db.csv')
  pl_win = db_2017[(db_2017.winner_name == player)]
  pl_lose = db_2017[(db_2017.loser_name == player)]
  if (pl_win.empty) and (pl_lose.empty):
      return player + ' did not yet play a professional match this year'
  return 'Since the beginning of the year, ' + player + ' won ' + str(len(pl_win)) + ' matches and lost ' + str(len(pl_lose)) + '.'

def tournament_summary(tourn):
  db_2017 = pd.read_csv('mon_db.csv')
  tourn_sf_temp = db_2017[(db_2017.tourney_name == tourn)]
  tourn_sf = tourn_sf_temp[(tourn_sf_temp.iloc[:,30] == 'SF')]
  tourn_f_temp = db_2017[(db_2017.tourney_name == tourn)]
  tourn_f = tourn_f_temp[(tourn_f_temp.iloc[:,30] == 'F')]
  winner = tourn_f.iloc[0].winner_name
  if tourn_sf.iloc[0].winner_name == winner:
      i = 0
  else:
      i = 1
  return tourn_sf.iloc[i].winner_name + ' (beat ' + tourn_sf.iloc[i].loser_name + ') won in the final against ' + tourn_sf.iloc[1-i].winner_name + ' (beat ' + tourn_sf.iloc[1-i].loser_name + '): ' + tourn_f.iloc[0].score

def bot(payload):
  connect = recastai.Connect(token=os.environ['REQUEST_TOKEN'], language=os.environ['LANGUAGE'])
  request = recastai.Request(token=os.environ['REQUEST_TOKEN'])

  message = connect.parse_message(payload)

  response = request.converse_text(message.content, conversation_token=message.sender_id)

  #print(response.memory)
  #print(response.action.slug)
  if response.action is None:
    replies = [{'type': 'text', 'content': r} for r in response.replies]
    connect.send_message(replies, message.conversation_id)
    return jsonify(status=200)

  if (response.action.slug == 'get-score'):
    leng = len(response.memory)

    tournament = response.get_memory('tournament')
    player_1 = response.get_memory('player_1')
    player_2 = response.get_memory('player_2')

    if (player_1 is None) and (player_2 is None):
      #In this case tournament must exist
      my_reply = tournament_summary(tournament.value)
      replies = [{'type':'text', 'content':my_reply}]
      response.set_memory({})
      #replies = [{'type':'text', 'content':'Which player are you interested in?'}]
    elif (player_1 is None) and not(player_2 is None):
      if tournament is None:
        my_reply = last_match(player_2.value)
        replies = [{'type':'text', 'content': my_reply}]
        response.set_memory({})
      else:
        my_reply = last_match(player_2.value, tournament.value)
        replies = [{'type':'text', 'content': my_reply}]
        response.set_memory({})
    elif (player_2 is None) and not(player_1 is None):
      if tournament is None:
        my_reply = last_match(player_1.value)
        replies = [{'type':'text', 'content': my_reply}]
        response.set_memory({})
      else:
        my_reply = last_match(player_1.value, tournament.value)
        replies = [{'type':'text', 'content': my_reply}]
        response.set_memory({})
    else:
      if tournament is None:
        replies = [{'type':'text', 'content':"What tournament are we talking about?"}]
      else:
        my_reply = score_request(player_1.value, player_2.value, tournament.value)
        replies = [{'type':'text', 'content': my_reply}]
        response.set_memory({})

#    if not(turn_exist):
#      replies = [{'type':'text', 'content':"What tournament are we talking about?"}]
#    elif not(pl1_exist) and not(pl2_exist):
#      replies = [{'type':'text', 'content':'Which player are you interested in?'}]
#    elif not(pl1_exist):
#      replies = [{'type':'text', 'content':'Who was the adversary?'}]
#    elif not(pl2_exist):
#      replies = [{'type':'text', 'content':'Who was the adversary?'}]
#    else: #All the necessary information exists
#      if response.memory[0].name == 'tournament':
#        tourn_index = 0
#        pl1_index = 1
#        pl2_index = 2
#      elif response.memory[1].name == 'tournament':
#        tourn_index = 1
#        pl1_index = 0
#        pl2_index = 2
#      else:
#        tourn_index = 2
#        pl1_index = 1
#        pl2_index = 0
#      my_reply = score_request(response.memory[pl1_index].value, response.memory[pl2_index].value, response.memory[tourn_index].value)
#      replies = [{'type':'text', 'content': my_reply}]
  elif (response.action.slug == 'get-head-to-head'):
    if len(response.memory) == 1:
      #my_reply = 'Who would you like to compare ' + response.memory[0].value + ' to?'
      my_reply = player_stats(response.memory[0].value)
      replies = [{'type': 'text', 'content': my_reply}]
      response.set_memory({})
    elif len(response.memory) == 2:
      my_reply = head_to_head(response.memory[0].value, response.memory[1].value)
      replies = [{'type': 'text', 'content': my_reply}]
      response.set_memory({})
  else:
    replies = [{'type': 'text', 'content': r} for r in response.replies]
  connect.send_message(replies, message.conversation_id)

  return jsonify(status=200)
