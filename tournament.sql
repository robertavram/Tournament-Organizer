
CREATE TABLE player(
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

-- Table of all tournaments
CREATE TABLE tour(
    id serial PRIMARY KEY,
    name varchar(50) UNIQUE
);

-- Table of tournament players
CREATE TABLE t_player(
    id serial PRIMARY KEY,
    t_id integer NOT NULL REFERENCES tour(id) ON DELETE CASCADE,
    player integer NOT NULL REFERENCES player(id) ON DELETE CASCADE,
    UNIQUE (t_id, player)
);

CREATE TABLE round(
    id serial PRIMARY KEY,
    t_id integer NOT NULL REFERENCES tour(id) ON DELETE CASCADE,
    r_no integer
);

-- tournament match - before the game is played
CREATE TABLE tmatch(
    id serial PRIMARY KEY,
    r_id integer NOT NULL REFERENCES round(id) ON DELETE CASCADE,
    player1 integer NOT NULL REFERENCES t_player(id) ON DELETE CASCADE,
    player2 integer REFERENCES t_player(id) ON DELETE CASCADE
);

-- match result - for every tournament match the result is stored in this table
CREATE TABLE mresult(
    tmatchid integer NOT NULL REFERENCES tmatch(id) ON DELETE CASCADE,
    winner integer REFERENCES t_player(id) ON DELETE CASCADE,
    loser integer REFERENCES t_player(id) ON DELETE CASCADE,
    draw boolean
);

-- View in which all the winners of a particular tournament are shown
-- this is useful to further count all the wins for a particular player
create view tour_win (winner, tour_id) as 
    select mresult.winner, tour.id as tour_id
            from mresult, tmatch, round, tour
            where mresult.tmatchid = tmatch.id and
                  tmatch.r_id = round.id and
                  round.t_id = tour.id;

-- View in which players are mapped to the total wins
create view tplayer_wins as
    select t_player.id, t_player.t_id, count(winner) 
        from t_player left join tour_win on t_player.id = winner
        group by t_player.id;

-- View in which players are mapped to the total matches
create view tplayer_matches as
    select t_player.id, t_player.t_id, count(tmatch) 
        from t_player left join tmatch on t_player.id = tmatch.player1 or t_player.id=tmatch.player2 
        group by t_player.id;

-- View in which players are listed next to their total matches and wins
create view t_player_wins_matches as
    select tplayer_wins.id as t_playerid, tplayer_wins.t_id as t_id, tplayer_wins.count as wins, tplayer_matches.count as matches 
        from tplayer_wins, tplayer_matches 
        where tplayer_wins.id=tplayer_matches.id;

-- View that shows the standings of players by wins only
create view standings as
    select t_player_wins_matches.t_playerid as id, player.name, wins, matches
        from player, t_player, t_player_wins_matches, tour
        where t_player_wins_matches.t_playerid = t_player.id and
        t_player.player = player.id and t_player.t_id = tour.id order by wins desc;

-- View that shows all opponents of a player, the round is present to insure proper count of opponents vs matches
-- if two players end up playing each other again in a different round
-- this is important because of the implementation of 'draw' as a result
create view opponent as
    select t_player.id, a1.player2 as opponent, a1.r_id from t_player, tmatch as a1 where t_player.id = a1.player1 
    union 
    select t_player.id, a1.player1 as opponent, a1.r_id from t_player, tmatch as a1 where t_player.id = a1.player2 order by id;

-- View that shows the wins of every opponent
create view opp_wins as
    select opponent.id, opponent.opponent, tplayer_wins.count as wins from opponent, tplayer_wins where opponent = tplayer_wins.id;

-- View 'supper standings' that shows the standings of players by wins and the sum of their opponent wins
create view sup_standings as
    select standings.id, name, standings.matches, standings.wins, sum(opp_wins.wins) as opp_wins 
        from standings left join opp_wins on standings.id=opp_wins.id 
        group by standings.id, standings.name, standings.wins, standings.matches order by wins desc, opp_wins desc;


-- insert the Default Tournament after the database is created
insert into tour(name) values ('Default Tournament');
