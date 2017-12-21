import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib3


path = 'https://en.wikipedia.org/wiki/Greeks_(finance)'
r = urllib3.urlopen(path).read()
soup = BeautifulSoup(r, 'lxml')

# print(soup)
# print(type(soup))
# print(soup.prettify())

table = soup.find('table', {'border':'1','cellspacing':'0','cellpadding':'10'})

greeks = []
key = []
value = []

for x,row in enumerate(table.find_all('tr')): ## primero enumero y segundo saca los valores

    # if x == 0:
        print row.get_text()
        greeks.append(row.get_text())
        print row.find_next_siblings('th')[0].get_text()
        value.append(row.find_next_siblings('th')[0].get_text())
    # else:
    #     key.append(row.get_text())
        # print row.get_text()
        # try:
        #     value.append(row.find_next_siblings('td')[0].get_text())
        # except:
        #     value.append('Null')
        #     print 'Campo Vacio'


cols = {'Cabecera': key, greeks[0]: value}

df = pd.DataFrame(data=cols)
# df.rename(columns={'Descripcion':airplane[0]}, inplace=True)
print df


# print(letters)





# from bs4 import BeautifulSoup
# import requests
# a = requests.get("http://games.espn.com/fba/scoreboard?leagueId=224165&seasonId=2017")
# soup = BeautifulSoup(a.text, 'lxml')
# # searching for the rows directly
# rows = soup.findAll('tr', {'class': 'linescoreTeamRow'})
# # you will need to isolate elements in the row for the table
# for row in rows:
#     print row.text