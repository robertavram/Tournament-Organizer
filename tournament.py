#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import pairing

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    
    return psycopg2.connect("dbname=tournament")


def createTournament(tname=''):
    """Creates a tournament or returns false if the tournament name exists in the Database"""
    
    # Using a unique Name and a unique ID might seem redundant, but this function
    # could be modified later to allow same names and still preserve proper structure
    if not tname:
        raise ValueError("Please give a tournament name")
        return
    
    db = connect()
    c = db.cursor()
    
    query = """
       insert into tour(name) values (%s);
    """
    result = True
    
    try:
        c.execute(query, (tname,))
    except:
        print 'Tournament name already exists, please choose another name, meanwhile continuing'
        result = False
        
    db.commit()
    db.close()
    
    return result

def deleteMatches(tournament='Default Tournament'):
    """Remove all the match records from the database
    For one particular tournament"""
    
    db = connect()
    c = db.cursor()
    query = """
        delete from round using tour 
        where round.t_id = tour.id and tour.name = %s;
    """
    c.execute(query,(tournament,))
    db.commit()
    db.close()
    
    
    return


def deletePlayers(tournament="Default Tournament", all=False):
    """Remove all the player records from the tournament, if all is true, delete all from the database."""
    db = connect()
    c = db.cursor()
    
    if all:
        query = """
            delete from player;
        """
        c.execute(query)
    else:
        query = """
            delete from t_player using tour where t_player.t_id = tour.id and tour.name = %s;
        """
        c.execute(query, (tournament,))
    
    db.commit()
    db.close()
    return

def countPlayers(tournament="Default Tournament"):
    """Returns the number of players currently registered."""
    
    db = connect()
    c = db.cursor()
    query = """
        select count(t_player.id) from t_player, tour where t_player.t_id = tour.id and tour.name = %s;
    """
    c.execute(query, (tournament,))
    result = c.fetchone()[0]
    db.close()
    return result;
    
def enrollPlayer(c, player_id, tournament):
    query = """
        insert into t_player (t_id, player) values ((select id from tour where name = %s), %s);
    """
    result = c.execute(query, (tournament, player_id))

def registerPlayer(name, tournament="Default Tournament", existingId=False):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # For the purpose of this exercise we assume that all players are new,
    # this because the names must not be unique;
    # in real life we would ask the player for his player id (maybe present on an issued registration card)
    # and enroll him in directly in the tournament if he has been previously registered
    db = connect()
    c = db.cursor()
    
    # Check if an existing id was provided if so use that to enroll in the default tournament
    if existingId:
        player_id = existingId
    else:
        query = """
            insert into player (name) values (%s) RETURNING id;
        """
        c.execute(query, (name,))
        player_id = c.fetchone()[0]
    
    # Now enroll this player into the tournament
    enrollPlayer(c, player_id, tournament)
    
    db.commit()
    db.close()
    return


def playerStandings(tournament = "Default Tournament"):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = '''
            select t_player_wins_matches.t_playerid as id, player.name, wins, matches
            from player, t_player, t_player_wins_matches, tour
            where t_player_wins_matches.t_playerid = t_player.id and
            t_player.player = player.id and t_player.t_id = tour.id and tour.name = %s order by wins desc; 
        '''
    c.execute(query, (tournament,))
    result = c.fetchall()
    db.close()
    return result
    
def playerSupStandings(tournament="Default Tournament"):
    """Returns a list of the players, their win records their opponent's win records,
     sorted by wins and opponent wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        opp_wins: the sum of all wins of every opponent 
                  that the player has had in the current tournament
    """
    db = connect()
    c = db.cursor()
    query = """
            select sup_standings.id, sup_standings.name, sup_standings.wins, sup_standings.opp_wins 
            from sup_standings, t_player, tour where sup_standings.id = t_player.id and t_player.t_id = tour.id and tour.name=%s 
            order by wins desc, opp_wins desc nulls last;
            """
    c.execute(query, (tournament,))
    stand = c.fetchall()
    
    
    db.close()
    return stand

def setPairing(player1, player2, tournament="Default Tournament"):
    """Given 2 players registered in a tournament and the tournament name,
        returns the id of the match that will have to be played.

    The function searches which round is next to be played,
    registers a new round for the tournament in the database in case it
    doesn't exist and then registers a new pair in the database.

    Returns:
      matchid: the id of the match to be played.
    """
    db = connect()
    c = db.cursor()
    
    # We look by for which round to play by checking the match count for either user..
    query1 = """
        select tplayer_matches.count from tplayer_matches, tour 
        where tour.name=%s and tour.id = t_id and tplayer_matches.id = %s;
    """
    c.execute(query1, (tournament, player1))
    round_no = c.fetchone()[0] + 1
    
    # Check if this round_no exists in this tournament already, otherwise create a new round
    check_round_q = """
        select round.id from round, tour where round.t_id = tour.id and tour.name=%s and round.r_no = %s; 
    """
    c.execute(check_round_q, (tournament, round_no))
    round_id = c.fetchone()
    
    if not round_id:
        # Create a new round
        c.execute("insert into round (t_id, r_no) values ((select id from tour where name = %s),%s) returning round.id;", (tournament, round_no))
        round_id = c.fetchone()[0]
    
    # Create a new match for this round for these players
    query2 ="""
        insert into tmatch (r_id, player1, player2) values (%s,%s,%s) returning tmatch.id;
    """
    c.execute(query2, (round_id, player1, player2))
    matchid = c.fetchone()[0]
    
    db.commit()
    db.close()
    return matchid

def setMatchResult(matchid, winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      matchid: the id of the match that was played
      winner:  the id number of the player who won if not a draw
      loser:  the id number of the player who lost if not a draw
      draw: boolean, True if it was a draw.
    """
    db = connect()
    c = db.cursor()
    query1 ="""
        insert into mresult (tmatchid, winner, loser, draw) values (%s,%s,%s,%s);
    """
    if draw:
        c.execute(query1, (matchid, None, None, draw))
    else:
        c.execute(query1, (matchid, winner, loser, draw))
    db.commit()
    db.close()
    return

def reportMatch(winner, loser, tournament="Default Tournament", draw=False):
    """Records the outcome of a single match between two players.
    
    First it creates the match, stores it, and then it sets the result

    Args:
      winner:  the id number of the player who won if any winner
      loser:  the id number of the player who lost if not draw
      draw: boolean, true or false
    """
    # Set up the match
    matchid = setPairing(winner, loser, tournament)
    
    # Store the result
    setMatchResult(matchid, winner, loser, draw)
    
    return
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ps = playerStandings()
    i = 0
    result = []
    while i < len(ps)-1:
        result.append((ps[i][0], ps[i][1], ps[i+1][0], ps[i+1][1]));
        i+=2
    return result

def get_opponent_list(tournament = "Default Tournament"):
    db = connect()
    c = db.cursor()
    query = """select opponent.id, opponent 
        from opponent, round, tour 
        where opponent.r_id = round.id and round.t_id = tour.id and tour.name = %s"""
    c.execute(query,(tournament,))
    result = c.fetchall()
    db.close()
    return result


def swissSupPairings(tournament="Default Tournament"):
    """Returns a list of pairs of players for the next round of a match.
    
    Accounts for uneven number of players, 
    When pairing, takes into consideration player's wins as well as the oponent's wins,
    Draws are not counted as wins for either player,
    
    Returns:
      A list of tuples, each of which contains (id1, id2)
        id1: the first player's unique id in relation to the tournament
        id2: the second player's unique id in relation to the tournament
    """
    print "\n NEW ROUND:"
    bye_pair = False
    standings = playerSupStandings(tournament)
    matches = get_opponent_list(tournament)
    # List of player ids
    lid = [] 
    # List of player pairs
    lpp = []
    #player matches dict
    p_matches_dict = {}
    for row in matches:
        if row[0] in p_matches_dict:
            p_matches_dict[row[0]].append(row[1])
        else:
            p_matches_dict[row[0]]=[row[1]]
            
    
    for row in standings:
        lid.append(row[0])
    
    if (len(lid)%2 == 1):
        db = connect()
        c = db.cursor()
        
        # Iterate backwards on the list and find the position of the first element that doesn't have a bye yet.
        # Make sure that the particular position is not even (has to be 1,3,5,7 etc) if even then move the element one position down and
        # add a none list element right after it
        for i in range(len(lid)-1, -1, -1):
            elm = lid[i]
            if (p_matches_dict) and (None in p_matches_dict[elm]):
                continue
            else:
                bye_pair = (lid.pop(i),None)
                break
            
            
        db.close()
    if not matches:    
        i = 0;
        while i < len(lid):
             
            # This try can be useful if somehow an uneven list gets passed through.
            try: lid[i+1]
            except:
                raise Exception("The list has an uneven number of players, make sure that you add a bye")
                break;
            pair = (lid[i], lid[i+1])
            lpp.append(pair)
            i += 2
    else:
        lpp = pairing.complex_pairing(matches, lid)
    
    if bye_pair:
        lpp.append(bye_pair)
        
    return lpp

