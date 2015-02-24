#===============================================================================
# a = [0,1,2,3,4]
# b = [0,1]
# c = [4]
# d = [1,0]
# 
# print list(set(a)-set(b)-set(c))
# 
# print (set(b) == set(d))
# 
# dd = {3:[set([2,5,3]),set([1,3,4])],
#       2:[[1,2]],
#       1:[[2],[1]]}
# 
# print (set([3,2,4]) in dd[3])
#===============================================================================

#===============================================================================
# import psycopg2
# 
# 
# def connect():
#     """Connect to the PostgreSQL database.  Returns a database connection."""
#     
#     return psycopg2.connect("dbname=tournament")
# 
# db = connect();
# c = db.cursor();
# c.execute("select opponent.id, opponent from opponent, round, tour where opponent.r_id = round.id and round.t_id = tour.id and tour.name = 'Private Tournament'")
# 
# a = c.fetchall()
# db.close()
# print a
#===============================================================================


a = [1,2,3,4]
print a[:len(a)-1]