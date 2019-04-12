# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:03:31 2019

@author: smald
"""
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

url = 'http://sofifa.com/players?offset=0'

fifa_stats = ['Crossing', 'Finishing', 'Heading Accuracy','Short Passing','Volleys', 
              'Dribbling', 'Curve','Free Kick Accuracy', 'Long Passing', 'Ball Control',
              'Acceleration', 'Sprint Speed', 'Agility', 'Reactions','Balance', 
              'Shot Power', 'Jumping', 'Stamina', 'Strength','Long Shots',
              'Aggression', 'Interceptions', 'Positioning','Vision', 'Penalties', 'Composure', 
              'Marking', 'Standing Tackle','Sliding Tackle',
              'GK Diving', 'GK Handling', 'GK Kicking','GK Positioning', 'GK Reflexes']

def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup

soup = soup_maker(url)
table = soup.find('table',{'class':'table'})
tbody = table.find('tbody')
all_tr = tbody.findAll('tr')
all_players = []
for player in all_tr:
    player_details = {}
    player_details["shortname"] = player.select('div > a')[1].get_text(strip=True)
    soup2 = soup_maker("http://sofifa.com" + player.select('div > a')[1].get('href'))
    center = soup2.find('div',{'class':'center'})
    article = center.find('article')
    all_stats_soup = article.select('div')[25]
    list_of_stats = all_stats_soup.findAll('span',{'class':'label'})
    if len(list_of_stats) == 0:
        all_stats_soup = article.select('div')[26]
        list_of_stats = all_stats_soup.findAll('span',{'class':'label'})
    for i in range(20):
        player_details[fifa_stats[i]] = list_of_stats[i].find(text=True)
    all_stats_soup = article.select('div')[34]
    list_of_stats = all_stats_soup.findAll('span',{'class':'label'})
    if len(list_of_stats) == 5:
        all_stats_soup = article.select('div')[35]
        list_of_stats = all_stats_soup.findAll('span',{'class':'label'})
    for i in range(14):
        player_details[fifa_stats[i]] = list_of_stats[i].find(text=True)
    all_players.append(player_details)
        
df = pd.DataFrame(all_players)

df.head(20)

