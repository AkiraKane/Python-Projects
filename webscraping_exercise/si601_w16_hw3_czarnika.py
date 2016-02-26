#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import urllib2
import time
from bs4 import BeautifulSoup
import json

def step_1():
    soup = []
    response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=1&title_type=feature')
    html_doc1 = response.read().decode('utf-8')
    response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=51&title_type=feature')
    html_doc2 = response.read().decode('utf-8')
    response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=101&title_type=feature')
    html_doc3 = response.read().decode('utf-8')
    response = urllib2.urlopen('http://www.imdb.com/search/title?at=0&genres=sci_fi&sort=user_rating&start=151&title_type=feature')
    html_doc4 = response.read().decode('utf-8')

    write_html(html_doc1, html_doc2, html_doc3, html_doc4)

    soup.append(BeautifulSoup(html_doc1, 'html.parser'))
    soup.append(BeautifulSoup(html_doc2, 'html.parser'))
    soup.append(BeautifulSoup(html_doc3, 'html.parser'))
    soup.append(BeautifulSoup(html_doc4, 'html.parser'))

    return soup

def step_2(soup):
    result = []
    for temp in soup:
        rank = temp.find_all('table')[0]
        for x in rank.find_all('tr')[1:]:
            dict ={
                'Rank': 0,
                'IMDB ID': 0,
                'Title': '',
                'Year': 0,
                'Rating':0.0
            }
            for y in x.find_all('td'):
                if y.attrs['class'][0] == 'number':
                    #Rank
                    rank = y.contents[0]
                    rank = rank.replace('.', '')
                    dict['Rank'] = int(rank)
                if y.attrs['class'][0] == 'title':
                    #Title
                    a = y.find_all('a')[0]
                    dict['Title'] = a.contents[0].encode('utf-8')
                    #ID
                    span = y.find_all('span')[0]
                    span = span.attrs['data-tconst']
                    dict['IMDB ID'] = span
                    #Year
                    span = y.find_all('span')[1]
                    span = span.contents[0].replace('(', '')
                    span = span.replace(')', '')
                    dict['Year'] = int(span)
                    #Rating
                    span = y.find_all('span')[15]
                    span = span.contents[0]
                    span = span.contents[0]
                    dict['Rating'] = float(span)


            result.append(dict)
    write_tsv2(result)
    return result

def step_3(result):
    list = []
    for x in result:
        url = 'https://api.themoviedb.org/3/find/' + x['IMDB ID'] + \
              '?external_source=imdb_id&api_key=e9ca299d099f4bf49b89be0f21dfbc70'
        response = urllib2.urlopen(url)
        time.sleep(5)
        html_doc = response.read().decode('utf-8')
        list.append(x['IMDB ID'] + '\t' + html_doc)

    write_tsv3(list)

def step_4(result):
    final = []
    with open('step3_czarnika.txt','rb') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            for item in result:
                if row[0] == item['IMDB ID']:
                    temp = json.loads(row[1])
                    if row[1] != '{"movie_results":[],"person_results":[],' \
                                 '"tv_results":[],"tv_episode_results":[],"tv_season_results":[]}':
                        vote_average = temp['movie_results'][0]['vote_average']
                        item['themoviedb Rating'] = vote_average
                        item['IMDB Rating'] = item['Rating']
                        item.pop('Rating')
                        item.pop('Rank')
                        final.append(item)
        write_tsv4(final)

def write_html(html_doc1, html_doc2, html_doc3, html_doc4):
    Html_file= open("step1_top_scifi_movies_1_to_50_czarnika.html","wu")
    Html_file.write(html_doc1.encode('utf-8'))
    Html_file.close()

    Html_file= open("step1_top_scifi_movies_51_to_100_czarnika.html","w")
    Html_file.write(html_doc2.encode('utf-8'))
    Html_file.close()

    Html_file= open("step1_top_scifi_movies_101_to_150_czarnika.html","w")
    Html_file.write(html_doc3.encode('utf-8'))
    Html_file.close()

    Html_file= open("step1_top_scifi_movies_151_to_200_czarnika.html","w")
    Html_file.write(html_doc4.encode('utf-8'))
    Html_file.close()

def write_tsv2(result):
    with open('step2_top_200_scifi_movies_czarnika.tsv', 'wb') as output_file:
        keys = ['Rank', 'IMDB ID', 'Title', 'Year', 'Rating']
        dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(result)

def write_tsv3(list):
    file = open('step3_czarnika.txt', 'w')
    for item in list:
        file.write("%s\n" % item.encode('utf-8'))

def write_tsv4(result):
    with open('step4_czarnika.csv', 'wb') as output_file:
        keys = ['IMDB ID', 'Title', 'Year', 'IMDB Rating', 'themoviedb Rating']
        dict_writer = csv.DictWriter(output_file, keys, delimiter=',')
        dict_writer.writeheader()
        dict_writer.writerows(result)

#Czarnika Main
def main():
    soup = step_1()
    result = step_2(soup)
    step_3(result)
    step_4(result)


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()