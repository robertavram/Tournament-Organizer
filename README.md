# Tournament

Tournament is python code that allows you to store tournaments, players, matches and match results in a Postgresql database. Tournament also allows you to see the ranking of the players after a specific round in a tournament, and can plan the next round's pairings based on the swiss pairing system. The pairing system pairs players as close in rank as possible while prioritizing the best players to have the closest in rank opponents.
the system supports matches ending in a draw, and uneven number of players.

Instalation guide:

  - Make sure you have python installed
  - Make sure you have [psycopg2] installed
  - Open a terminal or command line and go to the project's directory, run:
  
       ``` $ psql ```
  - Create a database called "tournament"
  
      ```  => \create database tournament```
  - Connect to the database
  
      ```  => \c tournament```
  - Import tournament.sql
  
       ``` tournament=> \i tournament.sql```

  

>You should now be able to run "test.py" and "test_extra_credit.py"

>"test_extra_credit.py" creates two new tournaments called "World Cup" and "Private Tournament" - the tournaments have 10 resp 7 players. The test plays log2(number of players) rounds for each tournament. The first round pairs are assigned randomly and the following rounds the players are paired by their rankings.




### Version
0.0.1

### Tech

Tournament uses [psycopg2] two work.


License
----

MIT


**Free Software**

[psycopg2]:https://pypi.python.org/pypi/psycopg2
