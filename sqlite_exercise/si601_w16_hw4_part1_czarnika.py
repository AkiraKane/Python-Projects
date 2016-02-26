import csv
import sqlite3 as sqlite
import json

def create_tables(cur):
    cur.execute("DROP TABLE IF EXISTS movies")
    cur.execute("DROP TABLE IF EXISTS movie_actor")
    cur.execute("DROP TABLE IF EXISTS movie_genre")
    cur.execute("CREATE TABLE movies (imdb_id text, title string, year integer, rating real)")
    cur.execute("CREATE TABLE movie_genre (imdb_id text, genre text)")
    cur.execute("CREATE TABLE movie_actor (imdb_id text, actor string)")

def open_data(con, cur):
    with open('movie_actors_data.txt','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            item = json.loads(row[0])
            #imdb_id , title , rating, genres, actors, and year
            imdb_id = item['imdb_id']
            title =  item['title']
            rating = item['rating']
            genres = item['genres']
            actors = item['actors']
            year = item['year']

            load_data(con, cur, imdb_id, title, rating, genres, actors, year)

def load_data(con, cur, imdb_id, title, rating, genres, actors, year):
    movies = [(imdb_id, title, year, rating)]
    cur.executemany("INSERT INTO movies VALUES (?,?,?,?)", movies)
    con.commit()
    movie_genre = []
    if len(genres) > 1:
        for genre in genres:
            movie_genre.append((imdb_id, genre))
        cur.executemany("INSERT INTO movie_genre VALUES (?,?)", movie_genre)
        con.commit()
    else:
        movie_genre.append((imdb_id, genres[0]))
        cur.executemany("INSERT INTO movie_genre VALUES (?,?)", movie_genre)
        con.commit()

    movie_actor =[]
    if len(actors) > 1:
        for actor in actors:
            movie_actor.append((imdb_id, actor))
        cur.executemany("INSERT INTO movie_actor VALUES (?,?)", movie_actor)
        con.commit()
    else:
        movie_actor.append((imdb_id, actors[0]))
        cur.executemany("INSERT INTO movie_actor VALUES (?,?)", movie_actor)
        con.commit()

def part_5(cur):
    cur.execute("SELECT genre, COUNT(*) as GENRE_NUM "
                    "FROM movie_genre "
                    "GROUP BY genre "
                    "ORDER BY GENRE_NUM DESC LIMIT 10")
    rows = cur.fetchall()

    print('Top 10 genres: ')
    print('Genre, Movies')
    for row in rows:
        print ','.join([str(x) for x in row])
    print('')

def part_6(cur):
    cur.execute("SELECT year, COUNT(*) as YEAR_NUM "
                "FROM movies "
                "GROUP BY year "
                "ORDER BY year ASC")
    rows = cur.fetchall()

    print('Movies broken down by year: ')
    print('Year, Movies')
    for row in rows:
        print ', '.join([str(x) for x in row])
    print('')

def part_7(cur):
    cur.execute("SELECT title, year, rating "
                "FROM movies m, movie_genre g "
                "WHERE m.imdb_id = g.imdb_id AND genre = 'Sci-Fi' "
                "GROUP BY year "
                "ORDER BY rating DESC, year DESC")
    rows = cur.fetchall()

    print('Movies broken down by year: ')
    print('Year, Movies, Rating')
    for row in rows:
        final = ''
        for x in row:
            if isinstance(x, unicode):
                final += x.encode('utf-8') + ', '
            elif isinstance(x, int):
                final += str(x) + ', '
            else:
                final += str(x) + ' '
        print final
    print('')

def part_8(cur):
    cur.execute("SELECT actor, COUNT(*) as ACTOR_NUM "
                "FROM movie_actor a, movies m "
                "WHERE m.imdb_id = a.imdb_id AND m.year >= 2000 "
                "GROUP BY actor "
                "ORDER BY ACTOR_NUM DESC, actor ASC LIMIT 10")
    rows = cur.fetchall()

    print('In and after year 2000, top 10 actors who played in most movies ')
    print('Actor, Movies')
    for row in rows:
        final = ''
        for x in row:
            if isinstance(x, unicode):
                final += x.encode('utf-8') + ', '
            else:
                final += str(x) + ' '
        print final
    print('')

def part_9(cur):
    cur.execute("SELECT DISTINCT a1.actor, a2.actor, COUNT(*) as PAIR_NUM "
                "FROM movie_actor a1, movie_actor a2 "
                "WHERE a1.imdb_id = a2.imdb_id and a1.actor < a2.actor "
                "GROUP BY a1.actor, a2.actor HAVING PAIR_NUM >= 3 "
                "ORDER BY PAIR_NUM DESC ")
    rows = cur.fetchall()

    print('Pairs of actors who co-stared in 3 or more movies ')
    print('Actor A, Actor B, Co-stared Movies')
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
    print('')
    with sqlite.connect('si601_f15_lab4.db') as con:
        cur = con.cursor()

        create_tables(cur)

        open_data(con, cur)

        part_5(cur)
        part_6(cur)
        part_7(cur)
        part_8(cur)
        part_9(cur)


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()