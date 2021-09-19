from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
import progressbar


import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pymongo import MongoClient
from pprint import pprint
import pymongo


from webdriver_manager.chrome import ChromeDriverManager
import json
with open('credential.json','r') as f:
    cred = json.load(f)
    

#creates the variables needed to manage the database
cluster = MongoClient(cred['cred'])
# choosing database
db = cluster["Game"]
# choosing collection
collection = db["Players"]
collection_man = db['Managers']
collection_tr = db['Transfers']

collection_temp = db["tempPlayers"]
collection_man_temp = db['tempManagers']
collection_tr_temp = db['tempTransfers']

#driver = webdriver.Chrome(ChromeDriverManager().install())


options = Options()
options.headless = True
options.add_argument("--window-size=1920,10200") #this is important, to tell it how much of the webpage to import
driver = webdriver.Chrome(options=options, executable_path=r'/usr/local/bin/chromedriver')

dict_names={
    'AS 800A': 'enzo',
    'PDG 1908': 'pietro',
    'IGNORANZA EVERYWHERE': 'mario',
    'SOROS FC': 'musci8',
    'MAINZ NA GIOIA': 'franky',
    'PALLA PAZZA': 'nanni',
    'I DISEREDATI': 'emiliano',
    'XYZ': 'luca',
    'AS 800A - PRIMAVERA': 'enzo',
    'PDG 1908 - PRIMAVERA': 'pietro',
    'IGNORANZA EVERYWHERE - PRIMAVERA': 'mario',
    'SOROS FC - PRIMAVERA': 'musci8',
    'MAINZ NA GIOIA - PRIMAVERA': 'franky',
    'PALLA PAZZA - PRIMAVERA': 'nanni',
    'I DISEREDATI - PRIMAVERA': 'emiliano',
    'XYZ - PRIMAVERA': 'luca'
    }

#rivedere i vari xpath, nel caso in cui la struttura del sito e' diversa

def formazioni(competizione = 'campionato'):
    #if competizione == 'campionato':
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni?id=185855'
    driver.get(link)

    players = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text


            all_playersE = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@class='player-list-item even  ']/td[1]/span/span[2]/a")
            all_playersO = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@class='player-list-item odd  ']/td[1]/span/span[2]/a")
            all_playersEP = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even  ']/td[1]/span/span[2]/a")
            all_playersOP = driver.find_elements_by_xpath("/html/body/div[7]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd  ']/td[1]/span/span[2]/a")
            #all_playersE = driver.find_elements_by_xpath("")

            all_pl = all_playersE + all_playersO + all_playersEP + all_playersOP
            names = []
            for pl in all_pl:
                names.append((pl.text).upper())
            players[name] = names
    return pd.DataFrame.from_dict(data=players, orient='index').T

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#def infortunati(link = 'https://www.pianetafanta.it/Giocatori-Infortunati.asp'):

#    driver.get(link)
#    names = driver.find_elements_by_xpath("//*[@id='my_id_div']/div[6]/div[11]/div[2]/div/div[@class]/div/table/tbody/tr[@class]/td[2]/a/strong")

#    players = []
#    for n in names:
#        players.append(n.text.upper())

#    return players

def infortunati(giornata):
    link = 'https://www.fantacalcio.it/cartella-medica/'+str(giornata)
    driver.get(link)
    button = driver.find_element_by_id("tabAll")

    driver.execute_script("arguments[0].click();", button)

    test = driver.find_elements_by_xpath("/html/body/div[6]/div[5]/main/div/div/div/div[1]/div[2]/div[3]/div[@class]/div/div/div[2]/div/div[1]/p[@class]/span")
                                        
    all_inf = []
    for pl in test:
        all_inf.append(pl.text)
    return all_inf

def rose(link = 'https://leghe.fantacalcio.it/fantapalla-forever/area-gioco/rose?id=185855'):
    
    driver.get(link)
    rose = {}


    for j in range(1,9):
        test_1 = []
        name = (driver.find_element_by_xpath('/html/body/div[8]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li['+str(j)+']/div/div[1]/div[2]/h4').text).upper()
        players = driver.find_elements_by_xpath('/html/body/div[8]/main/div[3]/div[2]/div[1]/div[2]/div[2]/ul/li['+str(j)+']/table/tbody/tr[@class]/td[2]/a/b')
        for pl in players:
            test_1.append((pl.text).upper())

        rose[name] = test_1
        
        
    return pd.DataFrame.from_dict(data=rose, orient='index').T

def count_inf(I , R ):
    count = {}

    all_names = ''.join(I)
    for team in R:
        c = 0
        for player in R[team]:
            if player == None:
                continue
            if player in ''.join(I):
                c+=1
        count[team] = c
    return pd.DataFrame(data = count, index = ['tot Infortunati'])

def bonus_panchina(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)+'?id=11194'
    driver.get(link)

    all_voti = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            #name = driver.find_element_by_xpath("/html/body/div[12]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text
            Fvoto_o = driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item odd  ']/td[5]/span")
            Nvoto_o = driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item odd  ']/td[4]/span")
            Fvoto_e = driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item even  ']/td[5]/span")
            Nvoto_e = driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class = 'player-list-item even  ']/td[4]/span")
            Fvoti = Fvoto_o + Fvoto_e
            Nvoti = Nvoto_o + Nvoto_e
            tot = []
            for i in range(len(Fvoti)):
                if Fvoti[i].text != '-':
                    tot.append(max(0,float(Fvoti[i].text)-float(Nvoti[i].text)))
            all_voti[name] = [sum(tot)]
    return pd.DataFrame(data=all_voti,index = ['Bonus Panchinari'])


def goal_subiti(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)+'?id=11194'
    driver.get(link)

    all_goal = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            if len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@class='player-list-item even  out']/td[@class='cell-text cell-primary x7 smart-x9 smart-role role-p']")) == 0:

                goal = len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[1]/td[3]/ul/li[@data-original-title='Gol subito (-0.5)']"))
            else:
                goal1 = len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even in ']/td[3]/ul/li[@data-original-title='Gol subito (-0.5)']"))
                goal2 = len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd in ']/td[3]/ul/li[@data-original-title='Gol subito (-0.5)']"))
                goal = max(goal1,goal2)
            all_goal[name] = goal

    return pd.DataFrame(data=all_goal,index = ['Goal subiti'])


def modificatore(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)+'?id=11194'
    driver.get(link)

    all_mod = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            all_mod[name] = 0
            temp = driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[3]/tbody/tr/td[1]/span")
            if len(temp)>0 and temp[0].text == 'Modificatore Difesa':
                mod = float(driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[3]/tbody/tr/td[2]/span").text)
                all_mod[name] = float(mod)
    return pd.DataFrame(data=all_mod, index = ['Modificatore'])


def scarica_voti(giornata, stagione):
    data = pd.read_excel('http://www.fantacalcio.it/Servizi/Excel.ashx?type=1&g='+str(giornata)+'&t=1601872625000&s='+stagione,skiprows = [0,1,2,3,4])
    data = data[data.Nome != 'Nome']
    data = data.dropna()
    data.index = list(range(len(data)))
    return data

def cartellini(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)+'?id=11194'
    driver.get(link)

    all_cart = {}
    for l in [2,3,4,5]:
        for k in [1,2]:
            name = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            gialli = len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@data-id]/td[3]/ul/li[@data-original-title='Ammonizione (-0.25)']"))
            gialliPE= len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even in ']/td[3]/ul/li[@data-original-title='Ammonizione (-0.25)']"))
            gialliPO= len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd in ']/td[3]/ul/li[@data-original-title='Ammonizione (-0.25)']"))
            rossi =  len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[1]/tbody/tr[@data-id]/td[3]/ul/li[@data-original-title='Espulso (-0.5)']"))
            rossiPE=len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item even in ']/td[3]/ul/li[@data-original-title='Espulso (-0.5)']"))
            rossiPO=len(driver.find_elements_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[2]/tbody/tr[@class='player-list-item odd in ']/td[3]/ul/li[@data-original-title='Espulso (-0.5)']"))
            all_cart[name] = [gialli+gialliPE+gialliPO, rossi]
    return pd.DataFrame(data=all_cart,index = ['C. gialli','C. rossi'])

def fantapunti_subiti(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)+'?id=11194'
    driver.get(link)

    all_punti = {}
    for l in [2,3,4,5]:
        name={}
        punti={}
        for k in [1,2]:
            name[k] = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            punti[k] = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[4]/tfoot/tr/td[2]/div").text[:-7]
        all_punti[name[1]]=float(punti[2])
        all_punti[name[2]]=float(punti[1])
            
    return pd.DataFrame(data=all_punti,index = ['Fantapunti Subiti'])  

def fantapunti_fatti(giornata):
    link = 'https://leghe.fantacalcio.it/fantapalla-forever/formazioni/'+str(giornata)+'?id=11194'
    driver.get(link)

    all_punti = {}
    for l in [2,3,4,5]:
        name={}
        punti={}
        for k in [1,2]:
            name[k] = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[1]/div["+str(k)+"]/div/div[2]/h4").text.upper()
            punti[k] = driver.find_element_by_xpath("/html/body/div[8]/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/div["+str(l)+"]/div[2]/div["+str(k)+"]/table[4]/tfoot/tr/td[2]/div").text[:-7]
        all_punti[name[1]]=float(punti[1])
        all_punti[name[2]]=float(punti[2])
            
    return pd.DataFrame(data=all_punti,index = ['Fantapunti Fatti'])

def IGNOBEL_tot(giornata):
    V = bonus_panchina(giornata) 
    G = goal_subiti(giornata)
    M = modificatore(giornata) 
    C = cartellini(giornata)
    while True:
        I=infortunati(giornata)
        if len(I)>0:
            break
    CI = count_inf(I, rose())
    F = fantapunti_fatti(giornata)
    S = fantapunti_subiti(giornata)
    output = pd.concat([F,S,G,C,V,M,CI], axis = 0)
    #output = pd.concat([F,S,G,C,V,M], axis = 0).T
    return output

def storico_IG(giornata, dict_names, path = "Dati_storici/"):

    test_dict={
        'enzo':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'pietro':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'mario':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'musci8':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'franky':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'nanni':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'emiliano':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']},
        'luca':{0:['gg','pf','ps','gs','c','pan','mod','inf','nome']}}
    for i in range(1,giornata+1):
        G=pd.read_pickle(path+"Giornata_"+str(i)+".pkl")
        for team, content in G.items():
            test_dict[dict_names[team]][i] = [i, content[0], float(content[1]), content[2], content[3]+2*content[4], content[5], content[6], content[7], dict_names[team]]
    return(test_dict)

def storico_individuale(nome, giornata, dict_names = dict_names):

    test_dict = storico_IG(giornata, dict_names)
    
    df = pd.DataFrame(data=test_dict[nome]).T
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header
    #df = df.reset_index()
    #df = df.drop('index',axis=1)
    return df

def aggiorna_database(giornata):
    nomi=[
        'enzo',
        'pietro',
        'mario',
        'musci8',
        'franky',
        'nanni',
        'emiliano',
        'luca'
    ]
    for name in nomi:
        df = storico_individuale(name, giornata)
        df.to_pickle("Dati_individuali/"+ name +".pkl")
    print("Dati aggiornati fino alla "+str(giornata)+" giornata")
    
import time

def scarica_stats(stagione):
    link='https://www.fantacalcio.it/statistiche-serie-a/'+stagione+'/fantacalcio/medie'
    driver.get(link)
    button = driver.find_element_by_id("toexcel")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(5)
    for file in os.listdir('./'):
        if 'Statistiche_Fantacalcio' in file:
            data = pd.read_excel(file,skiprows=[0])
            data = data[data.Nome != 'Nome']
            data = data.dropna()
            data.index = list(range(len(data)))
            os.remove(file)
            
    
    return data

def scarica_quot(stagione):
    driver.get('https://www.fantacalcio.it/quotazioni-fantacalcio')
    button = driver.find_element_by_id("toexcel")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(5)
    for file in os.listdir('./'):
        if 'Quotazioni_Fantacalcio' in file:
            data = pd.read_excel(file,skiprows=[0])
            data.index = list(range(len(data)))
            os.remove(file)
    return data

def rose_complete():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    # The ID and range of a sample spreadsheet.
    sheetId = '1uxUNBIjPzIJznquQ1rtHEiWE8iq_TNsJ3m9x8AAO0n0'
    SAMPLE_SPREADSHEET_ID_input = sheetId #'1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    SAMPLE_RANGE_NAME = 'ROSE!A1:P26'
    
    #global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'my_json_file.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    if not values_input and not values_expansion:
        print('No data found.')
        
    df=pd.DataFrame(values_input[1:], columns=values_input[0])
    
    return df



def rose_MDB():
    df0 = pd.DataFrame()
    for manager_dict in collection_man.find():
        man = manager_dict['owner']
        sq = []
        team_name = collection_man.find_one({'owner': man})['team_name']
        for pl in collection.find({'info.current_team.owner': man}):
            sq.append(pl['name'])
        df = pd.DataFrame(data = {team_name:sq})
        df0 = pd.concat([df0,df],axis=1)
    return df0



def stats_by_team_NO_INFO(stagione, dic = dict_names, primavera = False):
    if primavera:
        Rose = rose_MDB() 
    else:
        Rose = rose()
    stats = scarica_stats(stagione)
    nomi = list(stats.Nome)
    
    stats.index = nomi
    
    quot = scarica_quot()
    nomi_Q = list(quot.Nome)
    quot.index = nomi_Q
    ids = list(quot.Id)
    
    stats_teams = []
    for name in nomi_Q:
        for team, squad in Rose.items():
            team_name = 'svincolato'
            allenatore = None
            if name in list(squad):
                
                team_name = team
                allenatore = dic[team_name]
                break #might not be necessary
        
        temp = list(stats.T[name]) + list(quot.T[name][4:7])  +[team_name, allenatore]
        col = list(stats.columns) + list(quot.columns)[4:7] +['Nome Squadra', 'Allenatore']
        stats_teams.append(temp)
    return pd.DataFrame(data= stats_teams, columns = col, index = ids)

def find_missing_players(collection, database):
    missing_pl = []
    all_pl = list(database.Id)
    our_pl = []
    posts = collection.find()
    for pl in posts:
        our_pl.append(pl['_id'])
    our_pl
    for pl in all_pl:
        if pl in our_pl:
            continue
        else:
            missing_pl.append(pl)
    return missing_pl

def personal_info(Id, database):
    gioc = database[database.Id == Id]
    Name = list(gioc.Nome)[0]
    name = Name.replace(' ','-').lower()
    name = name.replace('.','').lower()
    Id = str(list(gioc['Id'])[0])
    team = list(gioc['Squadra'])[0].lower()
    link = 'https://www.fantacalcio.it/squadre/'+team+'/'+name+'/'+Id
    #print(link)
    driver.get(link)
    string = driver.find_element_by_xpath("/html/body/div[6]/div[5]/main/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/ul[1]/li[3]")
    classe = string.text[16:26]
    eta = string.text[28:30]
    full_name = driver.find_element_by_xpath("/html/body/div[6]/div[5]/main/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/ul[1]/li[1]").text
    nationality = driver.find_element_by_xpath("/html/body/div[6]/div[5]/main/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div[2]/div/ul[1]/li[2]").text
    
    return classe, eta, full_name[5:], nationality[12:]


#def info_missing_players(collection, database):
#    missing_ids = find_missing_players(collection, database)
#    all_pl = []
#    for idx in progressbar.progressbar(missing_ids):
#        infos = personal_info(idx, database)
#        dic = {}
#        dic['Id'] = idx
#        dic['Classe'] = infos[0]
#        dic['Eta\''] = infos[1]
#        dic['Nome Completo'] = infos[2]
#        dic['Nazionalita\''] = infos[3]
#        all_pl.append(dic)
#    return pd.DataFrame(all_pl, index = missing_ids)

def info_missing_players(collection, database):
    missing_ids = find_missing_players(collection, database)
    all_pl = []
    for k in progressbar.progressbar(range(len(missing_ids))):
        idx = missing_ids[k]
        try:
            infos = personal_info(idx, database)
        except:
            k = k-1
            continue
        dic = {}
        dic['Id'] = idx
        dic['Classe'] = infos[0]
        dic['Eta\''] = infos[1]
        dic['Nome Completo'] = infos[2]
        dic['Nazionalita\''] = infos[3]
        all_pl.append(dic)
    return pd.DataFrame(all_pl, index = missing_ids)