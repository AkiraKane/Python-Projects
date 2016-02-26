import sqlite3 as sqlite
import sys


def print_results(genre, k, rows):
    print('Top %s actors who played in most %s movies' % (k, genre))
    print('Actor, %s Movies Played in' % genre)
    for row in rows:
        final = ''
        for x in row:
            if isinstance(x, unicode):
                final += x.encode('utf-8') + ', '
            else:
                final += str(x) + ' '
        print final
    print('')

#Czarnika Main
def main():
    genre = sys.argv[1]
    k = sys.argv[2]
    with sqlite.connect('si601_f15_lab4.db') as con:
        cur = con.cursor()

        cur.execute("SELECT actor, COUNT(*) as ACTOR_NUM "
                    "FROM movie_actor a, movie_genre g "
                    "WHERE g.imdb_id = a.imdb_id AND genre = ? "
                    "GROUP BY actor "
                    "ORDER BY ACTOR_NUM DESC, actor ASC LIMIT ?", (genre, k))

    rows = cur.fetchall()
    print_results(genre, k, rows)

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()