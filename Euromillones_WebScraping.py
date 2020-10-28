# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 08:05:45 2020

@author: Javier Plo
@author: Elena Segundo
"""

""" Acciones previas"""

""" 1- pip install Beautifulsoup4 """
""" 2- pip install requests"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import pandas as pd

urlbase = 'https://www.euromillones.com.es/historico/euromillones-anos-anteriores.html'

# Descargamos la página inicial
page0 = requests.get(urlbase)
soup0 = BeautifulSoup(page0.content,features="lxml")

# Guardamos los enlaces a los sorteos para cada año  
myLinks = []
target0 = soup0.body.table
for link in target0.find_all('a'):
    myLinks.append(link.get('href'))

# Creamos la lista en la que guardaremos los datos   
data = []

# Para cada año, accedemos a la página que contiene los sorteos
for link in myLinks:
    
    link = urljoin(urlbase, link)
    page = requests.get(link)
    # Descargamos la página
    soup = BeautifulSoup(page.content,features="lxml")
    
    # Guardamos el año para añadirlo a los registros
    yeartitle = soup.table.caption.text
    year = yeartitle[-4:]
    
    # Accedemos a la tabla de los sorteos
    table = soup.table.find('tbody')
    
    # Obtenemos todas las filas de la tabla. Cada fila corresponde a un sorteo.
    rows = table.find_all('tr')
    
    semana = 1
    
    for row in rows:
        # Ignoramos las filas que no nos interesan
        cadenas = ["*", "SEM.", "NÚMEROS", "Lluvia de Millones"]
        if row.find('td') and any(cadena in row.td.text for cadena in cadenas) == False:            
     
            sorteo = [year]
            
            # Algunas semanas tienen más de un sorteo a la semana
            if ((row.find('td', attrs={'rowspan':'2'}) != None) or (int(year) < 2011) or (int(year) == 2011 and int(semana) < 19)) or (row.find('td', attrs={'rowspan':'4'}) != None):
                semana = row.td.text
            else:
                sorteo.append(semana)
            
            # Obtenemos todas las columnas de la fila
            cols = row.find_all('td')
            for ele in cols:
                numero = ele.text
                if numero != '\n':
                    sorteo.append(numero)
            
            # Algunos años no tienen campo "Semana" (aquellos que solo tienen un sorteo por semana)
            # Añadimos un valor igual al número de sorteo que corresponde al número de semana
            if len(sorteo) == 10:
                sorteo.insert(1, sorteo[1])
                
            # Algunos años no tienen campo "ElMillon"
            if len(sorteo) < 12:
                sorteo.append('')
            
            # Guardamos los resultados de la fila a la lista 'data'
            data.append(sorteo)        
 
# Creamos el dataframe en el que guardaremos los datos    
df = pd.DataFrame(data, columns=["Anyo","Semana","Sorteo","Fecha","Numero1","Numero2","Numero3","Numero4","Numero5","Estrella1","Estrella2","ElMillon"])


print(df.head(10))
            
# Guardamos los datos en un fichero csv
df.to_csv('Resultados_Euromillones.csv', index=False)