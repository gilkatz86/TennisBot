import pandas as pd

def last_match(player, tourn = None):

    db_2017 = pd.read_csv('mon_db.csv')
    if tourn == None:
        interest = db_2017[(db_2017.winner_name == player) | (db_2017.loser_name == player)]
        ind = interest.iloc[-1].name
        if db_2017.iloc[ind].winner_name == player:
            my_reply = 'In his last match, ' + player + ' beat ' + db_2017.iloc[ind].loser_name + ' in the ' + db_2017.iloc[ind,30] + ' of ' + db_2017.iloc[ind].tourney_name + ': ' + db_2017.iloc[ind].score
        else:#
            my_reply = 'In his last match, ' + player + ' lost to ' + db_2017.iloc[ind].winner_name  + ' in the ' + db_2017.iloc[ind,30] + ' of ' + db_2017.iloc[ind].tourney_name + ': ' + db_2017.iloc[ind].score
    else:
        interest = db_2017[((db_2017.winner_name == player) | (db_2017.loser_name == player)) & (db_2017.tourney_name == tourn)]
        ind = interest.iloc[-1].name
        if (db_2017.iloc[ind,30] == 'F') and (db_2017.iloc[ind].winner_name == player):
            my_reply = player + ' won the tournament, beating ' + db_2017.iloc[ind].loser_name + ' in the final: ' + db_2017.iloc[ind].score
        else:
            my_reply = player + ' lost in the ' + db_2017.iloc[ind,30] + ' to ' + db_2017.iloc[ind].winner_name + ': ' + db_2017.iloc[ind].score
    return my_reply

print(last_match('Rafael Nadal', 'Australian Open'))
