from tournament import *
from random import randint
from math import log, ceil

def setupTournament(tname):
    createTournament(tname)
    return
    
def registerPlayers(tournament="Default Tournament", tplayers = 10):
    """Registers a list of randomly generated names. """
    
    # Potential first names:
    pFN =["Eden ", "Sharilyn ", "Merissa ", "Dalia ",
          "Ema ", "Dede ", "Raul ", "Genaro ", "Raelene ", "Merrie "]
    
    # Potential last names:
    pLN = ["Alcantar", "Armstrong", "Brafford", 
           "Loughran", "Stager", "Saia", "Lyall",
           "Tuma", "Mccarville", "Sollars"]
    
    for i in range(tplayers):
        name = pFN[randint(0,9)] + pLN[randint(0,9)]
        registerPlayer(name, tournament)
    return


def gameon(lpp, tournament):
    """Play the games with a random winner or loser"""
    print lpp;
    
    for pair in lpp:
        
        #Random winner and loser
        if not pair[1]:
            
            #Making sure that if the pair contains a bye we don't put the by as winner.
            reportMatch(pair[0], pair[1], tournament)
            continue
        
        if randint(0, 1):
            reportMatch(pair[0], pair[1], tournament, True)
        else:
            r_win = randint(0, 1)
            r_loser = (r_win+1) % 2
            reportMatch(pair[r_win], pair[r_loser], tournament)
    
def testReportMatches(tournament="Default Tournament", tot_players=4):
    """ Registers players in a tournament, 
        figures out the minimum number of rounds to be played in order to find a winner,
        makes the pairings based on swissSupPairings,
        plays the games using gameon,
        prints the final results"""
        
    deleteMatches(tournament)
    deletePlayers(tournament)
    
    #Register n players
    registerPlayers(tournament, tot_players)
    
    rounds = int(ceil(log(tot_players, 2)))
    
    for i in range(rounds):
        pairings = swissSupPairings(tournament)
        gameon(pairings, tournament)
    
    standings = playerSupStandings(tournament)
    print "\n FINAL RESULT  FOR '{0}'\n".format(tournament)
    for row in standings:
        print row
    

if __name__ == '__main__':
    
    tournaments = [["World Cup", 10], ["Private Tournament", 7]]
    for t in tournaments:
        print "\n\n TESTING TOURNAMENT '{0}' WITH {1} PLAYERS".format(t[0], t[1])
        setupTournament(t[0])
        testReportMatches(t[0], t[1])
        
    print "Success!  All tests pass!"
