import pandas as pd
import numpy as np
import bs4 as bs
import urllib.request


path = 'https://es.wikipedia.org/wiki/Boeing'
sauce = urllib.request.urlopen(path).read()
soup = bs.BeautifulSoup(sauce, 'lxml')

# print(soup)
# print(type(soup))
# print(soup.prettify())

table = soup.find('table', {'class':'infobox'})

airplane = []
key = []
value = []

for x,row in enumerate(table.find_all('th')): ## primero enumero y segundo saca los valores

    if x == 0:
        airplane.append(row.get_text())
    else:
        key.append(row.get_text())
        try:
            value.append(row.find_next_siblings('td')[0].get_text())
        except:
            value.append('Null')
            print('Campo Vacio')


cols = {'Cabecera': key, airplane[0]: value}

df = pd.DataFrame(data=cols)
# df.rename(columns={'Descripcion':airplane[0]}, inplace=True)
print(df)


# print(letters)



