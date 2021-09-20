import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
from matplotlib.patches import Patch
from pymongo import MongoClient
from pprint import pprint
import pymongo
import json

import glob

with open('../../credential.json','r') as f:
    cred = json.load(f)

#from crea_df import storico_individuale
from matplotlib.offsetbox import OffsetImage,AnnotationBbox

from matplotlib import rcParams
# figure size in inches
rcParams['figure.figsize'] = 11.7,8.27
# Set the style globally
plt.style.use('default')
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Exo 2'
rcParams['font.weight'] = '500'
#rcParams['font.monospace'] = 'Ubuntu Mono'
rcParams['font.size'] = 16
rcParams['axes.labelsize'] = 16
rcParams['axes.labelweight'] = '500'
rcParams['axes.titleweight'] = '700'
rcParams['axes.titlesize'] = 16
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['legend.fontsize'] = 12
rcParams['figure.titlesize'] = 18
current_season = '2021-22'

import os

# Stabilisci ultima giornata valida
def current_matchday(season=current_season):
    cluster = MongoClient(cred['cred'])
    db = cluster['Game']
    coll_res = db['Results']
    #giornate = len(next(os.walk('../IGNOBEL/Dati_storici/'))[2])
    #giornate = len(glob.glob('../IGNOBEL/Dati_storici/*.pkl'))
    giornate = len(list(coll_res.find({'season':current_season})))
    return giornate
    
"""def storico_IG(giornata, dict_names, path = "../IGNOBEL/Dati_storici/"):

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
    return(test_dict)"""

def storico_IG_mongo(giornata, dict_names, season = current_season):
    cluster = MongoClient(cred['cred'])
    db = cluster['Game']
    coll_res = db['Results']

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
        #G=pd.read_pickle(path+"Giornata_"+str(i)+".pkl")
        
        post = coll_res.find_one({'season':season,'matchday':i})
        G = pd.DataFrame(post['results'])
        
        for team, content in G.items():
            test_dict[dict_names[team]][i] = [i, content[0], float(content[1]), content[2], content[3]+2*content[4], content[5], content[6], content[7], dict_names[team]]
    return(test_dict)



def storico_individuale(nome, giornata):
    dict_names={
    'AS 800A': 'enzo',
    'PDG 1908': 'pietro',
    'IGNORANZA EVERYWHERE': 'mario',
    'SOROS FC': 'musci8',
    'MAINZ NA GIOIA': 'franky',
    'PALLA PAZZA': 'nanni',
    'I DISEREDATI': 'emiliano',
    'XYZ': 'luca'
    }

    test_dict = storico_IG_mongo(giornata, dict_names)
    #test_dict = storico_IG(giornata, dict_names)
    
    df = pd.DataFrame(data=test_dict[nome]).T
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header
    #df = df.reset_index()
    #df = df.drop('index',axis=1)
    return df

### Init dataframes #########################################################

def set_par(fasce = 2):

    Teams = {'luca' : ['XYZ', 'darkblue'],
             'franky' : ['Mainz Na Gioia', 'r'],
             'emiliano' : ['I Diseredati', 'skyblue'],
             'nanni' : ['Palla Pazza', 'firebrick'],
             'enzo' : ['AS 800A', 'gold'],
             'pietro' : ['PDG 1908', 'dodgerblue'],
             'musci8' : ['Soros fc', 'lightgreen'],
             'mario' : ['Ignoranza', 'pink'],
            }

    Logos = {'luca' : '../Logos/fit/luca.png',
             'franky' : '../Logos/fit/franky.png',
             'nanni' : '../Logos/fit/nanni.png',
             'pietro' : '../Logos/fit/pietro.png',
             'mario' : '../Logos/fit/mario.png',
             'enzo' : '../Logos/fit/enzo.png',
             'musci8' : '../Logos/fit/musci8.png',
             'emiliano' : '../Logos/fit/emiliano.png'}

    parameters = [
        'punti_fatti',         # fantapunti realizzati
        'punti_subiti',        # fantapunti subiti
        'goal_subiti_por',     # goal subiti dal portiere che concorre a punteggio squadra
        'cartellini',          # subiti da giocatori che concorrono a punteggio squadra (giallo=1, rosso=2)
        'bonus_panchina',      # somma dei bonus giocatori che non concorrono a punteggio squadra
        'mod_difesa',          # modificatore difesa
        'infortunati'          #infortunati giornata
        #'mod_fairplay'         # modificatore fairplay
    ]
    df = pd.DataFrame(columns=parameters)

    df_luca = df
    df_franky = df
    df_nanni = df
    df_pietro = df
    df_mario = df
    df_enzo = df
    df_musci8 = df
    df_emiliano = df

    Results = {
        'luca' : df_luca,
        'franky' : df_franky,
        'emiliano' : df_emiliano,
        'nanni' : df_nanni,
        'enzo' : df_enzo,
        'pietro' : df_pietro,
        'musci8' : df_musci8,
        'mario' : df_mario,
    }

    # Steps of scored goals
    #goal_marks=np.array([66,68,70,72,74,76,78,80,82,84,86,88,90])
    
    goal_marks = np.arange(66,100,fasce)
    
    return Teams, Logos, parameters, Results, goal_marks

### Utility functions ################################################
def get_goal(fp, goal_marks):
    '''Return number of goals given fantapoints'''
    goal_counter = 0
    for mark in goal_marks:
        if fp<mark: return goal_counter
        goal_counter = goal_counter+1
    return goal_counter

def esito(gf,gs):
    '''Return match result (V,P,S) given goal scored and conceded'''
    if gf>gs: return 'V'
    elif gf<gs: return 'S'
    else: return 'P'
    
def punti(esito):
    '''Return standing points given match result'''
    try:
        if esito=='V': return 3
        elif esito=='S': return 0
        elif esito=='P': return 1
    except ValueError:
        print('Esito non valido')

def mod_fairplay(cartellini):
    '''Return modificatore fairplay value given number of yellow/red cards'''
    if cartellini==0: return 1
    return 0

def get_team_colors(Teams):
    '''Return list of team colors by default order'''
    colors = []
    for key in Teams.keys():
        colors.append(Teams[key][1])
    return colors
    
def fattore_distacco(Total):
    pf_med = np.median(Total['punti_fatti'])
    pf_std = np.std(Total['punti_fatti'])
    dist_med = np.median(Total['distacco'])
    dist_std = np.std(Total['distacco'])
    pf_rel = (Total['punti_fatti'] - pf_med) / pf_std
    dist_rel = (Total['distacco'] - dist_med) / dist_std
    return -dist_rel-pf_rel

### Fill dataframe per partita #############################
#############################################################
# Crea calendario con dictionary del rivale per ciscauna squadra, giornata per giornata
#############################################################
def make_calendar_array(data_path = '../IGNOBEL/Dati_storici/'):
    giornate = current_matchday()
    cluster = MongoClient(cred['cred'])
    db = cluster['Game']
    coll_res = db['Results']
    # dictionary converting team names into owner names
    team2owners = {
        'XYZ': 'luca',
        'MAINZ NA GIOIA': 'franky',
        'I DISEREDATI': 'emiliano',
        'PALLA PAZZA' : 'nanni',
        'AS 800A': 'enzo',
        'PDG 1908': 'pietro',
        'SOROS FC': 'musci8',
        'IGNORANZA EVERYWHERE':'mario',
    }

    calendar = [] #array con accoppiamenti squadre giornata per giornata
    rivals = {} #dictionary con accoppiamenti singola giornata
    # Rimepi array calendar con dictionary accoppiamento per ogni owner
    for giornata in range(1,giornate+1):
        # read Dati storici
        #df = pd.read_pickle(data_path + 'Giornata_%d.pkl' % giornata)
        df = pd.DataFrame(coll_res.find_one({'season':'2021-22','matchday':giornata})['results'])
        teams = df.columns
        # accoppia teams
        for i, team in enumerate(teams):
            owner = team2owners[team]
            if i%2 == 0:
                rival_owner = team2owners[teams[i+1]]
            else:
                rival_owner = team2owners[teams[i-1]]
            rivals[owner] = rival_owner # dict accoppiamenti di giornata
        # array di accoppiamenti per giornata
        calendar.append(rivals)
        rivals = {}
    
    return calendar

#############################################################
# Aggiungi colonna avversario ai dataframes in Results
#############################################################
def add_avversario_column_to_Results(calendar, Results):
    giornate = current_matchday()
    for owner in Results.keys():
        avversari_array = []
        for giornata in range(0,giornate):
            avversario = calendar[giornata][owner]
            avversari_array.append(avversario)
        Results[owner]['avversario'] = avversari_array
    return Results
        
def fill_dataframe_partita(Results_0, giornate, parameters, goal_marks, Teams, Print = False):
    Results = Results_0
    for team, df in Results.items():
        Results[team] = Results[team][0:0]

        #Results[team] = pd.read_csv(team+'.txt', sep=' ', names=parameters, skiprows=1)

        #################### AGGIUNTO DA LUCA: CREA DIRETTAMENTE I DF USANDO LA FUNZIONE IMPORTATA, NON PIU' LETTI DA PICKLES
        #Results[team] = pd.read_pickle('Dati_individuali/'+team+'.pkl')
        Results[team] = storico_individuale(team, giornate)
        Results[team] = Results[team].drop('gg',axis=1)
        Results[team] = Results[team].drop('nome',axis=1)
        Results[team].columns = parameters
        #####################

        Results[team]['mod_fairplay'] = Results[team].apply(lambda x: mod_fairplay(x['cartellini']), axis=1)
        Results[team]['GF'] = Results[team].apply(lambda x: get_goal(x['punti_fatti'], goal_marks), axis=1)
        Results[team]['GS'] = Results[team].apply(lambda x: get_goal(x['punti_subiti'], goal_marks), axis=1)
        Results[team]['esito'] = Results[team].apply(lambda x: esito(x['GF'],x['GS']), axis=1)
        Results[team]['pti'] = Results[team].apply(lambda x: punti(x['esito']), axis=1)
        Results[team] = Results[team].assign(Team=team)   
        
        # Add avversario column to each team's dataframe
        calendar = make_calendar_array()
        Results = add_avversario_column_to_Results(calendar = calendar, Results = Results)

        if Print:
            print('###', team, '|', Teams[team], '###')
            display(Results[team])
            print('\n\n\n')
        
    return Results
       
def cumulative_data(Results, giornate, Print = True):

    ### concatenate team dataframes ##################
    cdf = pd.concat(Results)
    pf_med = np.median(cdf.punti_fatti)
    pf_std = np.std(cdf.punti_fatti)
    ps_med = np.median(cdf.punti_subiti)
    ps_std = np.std(cdf.punti_subiti)
    gf_med = np.median(cdf.GF)
    gf_std = np.std(cdf.GF)

    if Print:
        print('### CUMULATIVE DATA after', giornate, 'rounds ###')
        print('Punti Fatti:\n mediana =', pf_med, '\n varianza =', pf_std, 
              #'\nPunti Subiti:\n mediana =', ps_med, '\n varianza =', ps_std, 
              '\nGoal Fatti:\n mediana =', gf_med, '\n varianza =', gf_std
             )
    return pf_med, pf_std, ps_med, ps_std, gf_med, gf_std


### values dataframe #######################
def close_games(Results, giornate, verbose=False):
    data = Results
    '''Compute close games per team and add factor to Total dataframe'''
    factor_close_games = []
    for team, df in data.items():
        df = df[df.index <= giornate]
        if verbose: print('\n###', team, '###')
        pti=0
        g = 0
        for gg in df.index:     
            if (np.abs(df['punti_fatti'][gg]-df['punti_subiti'][gg]))<=2:
                res = esito(df.GF[gg], df.GS[gg])
                if verbose: print('G', gg, '| punti fatti:', df.punti_fatti[gg], ' ( subiti:', df.punti_subiti[gg],') |', res, '(', df.GF[gg], '-', df.GS[gg], ')')
                pti = pti+punti(res)
                g = g+1
        try:
            if verbose: print('---> %d punti in %d giornate \n     (media: %.2f)' % (pti, g, pti/g))
            factor_close_games.append(pti-g)
        except:
            if verbose: print('---> No close games found')
            factor_close_games.append(0)
    return factor_close_games


def low_scoring_games(Results, giornate, verbose=False):
    data = Results
    '''Compute close games per team and add factor to Total dataframe'''
    factor_low_scoring_games = []
    for team, df in data.items():
        df = df[df.index <= giornate]
        if verbose: print('\n###', team, '###')
        pti=0
        g = 0
        for gg in df.index:     
            if df['punti_fatti'][gg] < 62:
                res = esito(df.GF[gg], df.GS[gg])
                if verbose: print('G', gg, '| punti fatti:', df.punti_fatti[gg], ' ( subiti:', df.punti_subiti[gg],') |', res, '(', df.GF[gg], '-', df.GS[gg], ')')
                pti = pti+punti(res)
                g = g+1
        try:
            if verbose: print('---> %d punti in %d giornate \n     (media: %.2f)' % (pti, g, pti/g))
            factor_close_games.append(pti-g)
        except:
            if verbose: print('---> No games found')
            factor_close_games.append(0)
    return factor_low_scoring_games


def exact_fp(Results, giornate, goal_marks, verbose=False):
    data = Results
    '''Compute close games per team and add factor to Total dataframe'''
    factor = []
    for team, df in data.items():
        df = df[df.index <= giornate]
        if verbose: print('\n###', team, '###')
        pti=0
        g = 0
        for gg in df.index:     
            if df['punti_fatti'][gg] in goal_marks:
                res = esito(df.GF[gg], df.GS[gg])
                if verbose: print('G', gg, '| punti fatti:', df.punti_fatti[gg], ' ( subiti:', df.punti_subiti[gg],') |', res, '(', df.GF[gg], '-', df.GS[gg], ')')
                if (df.GF[gg] - df.GS[gg]) <= 1:
                    res_ = esito(df.GF[gg]-1, df.GS[gg])
                    pti_ = punti(res_)
                    pti = pti+punti(res)-pti_
                g = g+1
        try:
            if verbose: print('---> %d punti rubati in %d giornate' % (pti, g))
            factor.append(pti)
        except:
            if verbose: print('---> No stolen games found')
            factor.append(0)
    return factor

def opponent_almost_scored(Results, giornate, goal_marks, verbose=False):
    data = Results
    '''Compute close games per team and add factor to Total dataframe'''
    factor = []
    for team, df in data.items():
        df = df[df.index <= giornate]
        if verbose: print('\n###', team, '###')
        pti=0
        g = 0
        for gg in df.index:     
            if df['punti_subiti'][gg] in goal_marks-0.5:
                res = esito(df.GF[gg], df.GS[gg])
                if verbose: print('G', gg, '| punti fatti:', df.punti_fatti[gg], ' ( subiti:', df.punti_subiti[gg],') |', res, '(', df.GF[gg], '-', df.GS[gg], ')')
                if (df.GF[gg] - df.GS[gg]) <= 1:
                    res_ = esito(df.GF[gg], df.GS[gg]+1)
                    #print('Actual Result: %s, Potential: %s' % (res, res_))
                    pti_ = punti(res_)
                    pti = pti+punti(res)-pti_
                g = g+1
        try:
            if verbose: print('---> %d punti rubati in %d giornate' % (pti, g))
            factor.append(pti)
        except:
            if verbose: print('---> No stolen games found')
            factor.append(0)
    return factor



def make_Total_df(Results, giornate, goal_marks, verbose=False):
    data = Results
    columns = list(data['luca'])
    table = [[]]
    for team,df in data.items():
        df = df[df.index <= giornate]
        values = []
        for col in columns:
            values.append(df[col].sum())
        values[len(values)-1]=team
        table.append(values)
    table=table[1:]
    Total=pd.DataFrame(table,columns=columns)
    # additional columns
    Total = Total.sort_values(by=['punti_fatti'], ascending=False)
    Total['pos'] = Total['pti'].rank(ascending=False, method='first')
    Total['rank'] = Total['punti_fatti'].rank(ascending=False, method='first')
    Total['distacco'] = np.max(Total['pti']) - Total['pti']
    Total['f_pos'] = Total['rank']-Total['pos']
    Total['f_distacco'] = fattore_distacco(Total)
    Total['x_punti_subiti'] = (Total['punti_fatti'].sum() - Total['punti_fatti'])/7
    Total['x_GS'] = (Total['GF'].sum() - Total['GF'])/7
    Total['f_GS'] = -1*(Total['GS']-Total['x_GS'])/np.std(Total['GS'])
    Total.sort_index(inplace=True)
    Total['f_close_games'] = close_games(Results, giornate)
    Total['f_stolen_games'] = exact_fp(Results, giornate, goal_marks)
    Total['f_unlucky_opponent'] = opponent_almost_scored(Results, giornate, goal_marks)
    
    # dirty hack
    Total['Team'] = Total['avversario']
    return Total


########## PLOTTING FUNCTIONS

def X_goal_subiti(Total, giornate, Teams):

    fig = plt.figure(figsize=(8,5))

    colors = get_team_colors(Teams)

    plt.bar(np.arange(0,8), Total['x_GS'], color=colors, alpha=0.35, label='Expected Goal Subiti')
    plt.bar(np.arange(0,8), Total['GS'], color=colors, alpha=0.99, width=0.5, label='GS')
    xlabels = Total['Team']
    plt.xticks(Total.index, xlabels, rotation=45, ha='right')
    plt.grid(which='both', axis='y', alpha=0.25)

    plt.ylim(ymin = np.min(Total['GS']-1))
    plt.ylabel('Goal Subiti')
    title = 'x Goal Subiti (' + str(giornate) + ' Giornate)'
    plt.title(title)

    plt.legend()

    plt.show()
    
    
def fattore_goal_subiti(Total, giornate, Teams):
    fig = plt.figure(figsize=(6,5))
    plt.grid(which='both', axis='y', ls='-', alpha=0.25)

    colors = get_team_colors(Teams)

    std = np.std(Total['GS'])
    plt.bar(np.arange(0,8), -1*(Total['GS']-Total['x_GS'])/std, color=colors, alpha=0.99, width=0.8, label='Fattore GS')
    xlabels = Total['Team']
    plt.xticks(Total.index, xlabels, rotation=45, ha='right')
    plt.axhline(y=0, xmin=-100, xmax=100, color='grey', ls='-')
    plt.ylim(-2,2)

    plt.ylabel('(xGS-GS)/std(GS) [$N\,\sigma$]')
    title = 'Fattore Goal Subiti (' + str(giornate) + ' Giornate)'
    plt.title(title)

    plt.text(x=8.25, y=+0.5, s='Fortuna', verticalalignment='bottom', horizontalalignment='right', color='grey', rotation='90')
    plt.text(x=8.25, y=-0.5, s='Sfortuna', verticalalignment='top', horizontalalignment='right', color='grey', rotation='90')


    #plt.legend()

    plt.show()
    
def punti_VS_fantapunti(Total, giornate, Teams):    
    ### Punti fatti vs classifica ###############
    fig = plt.figure(figsize=(8,5))

    colors = get_team_colors(Teams)
    x = Total['punti_fatti']
    y = Total['pti']

    plt.bar(np.arange(0,8), x, color=colors, alpha=0.99, label='Expected Goal Subiti')
    plt.ylabel('Fantapunti')
    plt.ylim(np.min(x)-10, np.max(x)+10)
    xlabels = Total['Team']
    plt.xticks(Total.index, xlabels, rotation=45, ha='right')

    # secondary y axis
    ax2 = plt.twinx()
    ax2.set_ylabel('Fantapunti')
    ax2.tick_params(axis='y', colors='k')
    ax2.yaxis.label.set_color('k')
    ax2.plot([],[])

    plt.bar(np.arange(0,8), y, color='w', edgecolor=colors, alpha=1, width=0.4, lw=2, label='GS')


    #plt.xticks(Total.index, xlabels, rotation=45, ha='right')
    plt.grid(which='both', axis='y', alpha=0.25)

    #plt.ylim(ymin = np.min(Total['GS']-1))
    plt.ylabel('Punti in classifica')
    title = 'PUNTI vs FANTAPUNTI | ' + str(giornate) + ' Giornate'
    plt.title(title)

    #legend
    legend_elements = [
        Patch(facecolor='k', edgecolor='k', label='Fantapunti'),
        Patch(facecolor='w', edgecolor='k', label='Punti'),
    ]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05,1))

    plt.show()
    

def fantapunti_stats(Total, giornate, Teams, pf_std, pf_med):    
    fig = plt.figure(figsize=(6,5))
    plt.grid(which='both', axis='y', ls='-', alpha = 0.25)

    colors = get_team_colors(Teams)

    std = pf_std*giornate
    med = pf_med*giornate

    plt.bar(np.arange(0,8), (Total['punti_fatti']-med)/std, color=colors, alpha=0.99, width=0.8, label='')
    xlabels = Total['Team']
    plt.xticks(Total.index, xlabels, rotation=45, ha='right')
    plt.axhline(y=0, xmin=-100, xmax=100, color='grey', ls='-')
    #plt.ylim(-2,2)

    plt.ylabel('(fantapunti_fatti-median)/std [$N\,\sigma$]')
    title = 'Fantapunti Fatti (' + str(giornate) + ' Giornate)'
    plt.title(title)

    plt.show()
    
def fattore_close_games(Total, giornate, Teams):        
    fig = plt.figure(figsize=(6,5))
    plt.grid(which='major', axis='y', ls='-', alpha=0.25)

    colors = get_team_colors(Teams)

    plt.bar(np.arange(0,8), Total['f_close_games'], color=colors, alpha=0.99, width=0.8, label='')
    xlabels = Total['Team']
    plt.xticks(Total.index, xlabels, rotation=45, ha='right')
    plt.axhline(y=0, xmin=-100, xmax=100, color='grey', ls='-')

    ylim = np.max(np.abs(Total['f_close_games']))*1.1
    #plt.ylim(-2.1,2.1)

    plt.ylabel('Punti guadagnati risp. a solo pareggi')
    title = 'Fattore Close Games (' + str(giornate) + ' Giornate)'
    plt.title(title)

    plt.text(x=8.25, y=+0.5, s='Fortuna', verticalalignment='bottom', horizontalalignment='right', color='grey', rotation='90')
    plt.text(x=8.25, y=-0.5, s='Sfortuna', verticalalignment='top', horizontalalignment='right', color='grey', rotation='90')

    plt.show()
    
    
def get_bigradient_colors(Total, Teams, max_f, min_f):
    colors = []
    edgecolors = []
    for key in Teams.keys():
        x = Total[Total['Team']==key]['IndiceFortuna'].sum()
        if Total[Total['Team']==key]['IndiceFortuna'].sum() >= 0:
            x = (max_f - Total[Total['Team']==key]['IndiceFortuna'].sum())/max_f
            s = (x,1,x)
            colors.append(s)
            edgecolors.append('g')
            #edgecolors.append('limegreen')
        else: 
            x = -(Total[Total['Team']==key]['IndiceFortuna'].sum() - min_f)/min_f
            s=(1,x,x)
            colors.append(s)
            #edgecolors.append('orangered')
            edgecolors.append('r')
    return colors, edgecolors

# Take negative and positive data apart and cumulate
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d 




def calc_fortuna(df, giornate, tot_giornate):
    '''
    keys = ('f_pos', 'f_distacco', 'f_GS', 'f_close_games', 'f_stolen_games', 'f_unlucky_opponent')
    scaling = (0.5, 1, 1, 0.5, 0.25*tot_giornate/giornate, 0.25*tot_giornate/giornate)
    cols = ['dodgerblue', 'purple', 'r', 'gold', 'c', 'lime']
    factors = []
    df['IndiceFortuna'] = [0,0,0,0,0,0,0,0]
    ### build fortuna
    for col,scale in zip(keys,scaling):
        factors.append(df[col]*scale)
        df['IndiceFortuna'] = df['IndiceFortuna'] + df[col]*scale
    return df, factors
    '''
    
    keys = ('f_pos', 'f_distacco', 'f_GS', 'f_close_games')
    scaling = (0.5, 1, 1, 0.5)
    cols = ['dodgerblue', 'purple', 'r', 'gold']
    factors = []
    df['IndiceFortuna'] = [0,0,0,0,0,0,0,0]
   ### build fortuna
    for col,scale in zip(keys,scaling):
        factors.append(df[col]*scale)
        df['IndiceFortuna'] = df['IndiceFortuna'] + df[col]*scale
    return df, factors


def C_factor(Results, Total, giornate, tot_giornate, goal_marks, Teams):
    
    cols = ['dodgerblue', 'purple', 'r', 'gold', 'c', 'lime']
    keys = ('f_pos', 'f_distacco', 'f_GS', 'f_close_games', 'f_stolen_games', 'f_unlucky_opponent')
    scaling = (0.5, 1, 1, 0.5, 0.25*tot_giornate/giornate, 0.25*tot_giornate/giornate)
    
    #--- Fortuna Total
    Total, __factors__ = calc_fortuna(Total, giornate, tot_giornate)
    matchday = giornate
    data_per_round = make_Total_df(Results, giornate, goal_marks, verbose=False)
    __df__, __factors__ = calc_fortuna(data_per_round, giornate, tot_giornate)



    # re-shape data for positive-negative bar plot
    __data__ = np.array(__factors__)
    #print(__data__)
    data_shape = np.shape(__data__)
    #print(data_shape)
    cumulated_data = get_cumulated_array(__data__, min=0)
    cumulated_data_neg = get_cumulated_array(__data__, max=0)
    # Re-merge negative and positive data.
    row_mask = (__data__<0)
    cumulated_data[row_mask] = cumulated_data_neg[row_mask]
    data_stack = cumulated_data
    #print(np.shape(data_stack))



    fig = plt.figure(figsize=(8,5))
    plt.grid(which='major', axis='y', ls='-', alpha=0.25)
    xlabels = __df__['Team']
    plt.xticks(__df__.index, xlabels, rotation=45, ha='right')
    plt.axhline(y=0, xmin=-100, xmax=100, color='grey', ls='-')

    max_f = max(__df__['IndiceFortuna'])
    min_f = np.min(__df__['IndiceFortuna'])
    colors, edgecolors = get_bigradient_colors(Total, Teams, max_f, min_f)
    plt.bar(np.arange(0,8), __df__['IndiceFortuna'], color='black', edgecolor=edgecolors, lw=0, alpha=0.15, width=0.9, label='')

    #print(np.arange(0, data_shape[0]))

    for i in np.arange(0, data_shape[0]):
        plt.bar(np.arange(data_shape[1]), __data__[i], bottom=data_stack[i], color=cols[i],alpha=0.99, width=0.5, label=keys[i])

    plt.legend()

    for i, f in enumerate(list(np.round(__df__['IndiceFortuna'],decimals=1))):
        if f<0: 
            va = 'top'
            offset = -0.2
        else: 
            va = 'bottom'
            offset = 0.2
        plt.annotate(f, (i, f+offset), horizontalalignment='center', verticalalignment=va)

    plt.ylim(min_f-2, max_f+2)

    plt.ylabel('Indice Fortuna')
    title = 'C Factor (' + str(matchday) + '° Giornata)'
    plt.title(title)
    plt.show()
    
    
def offset_image(Logos, x,y, name, ax, zoom):
    img = plt.imread(Logos[name])
    im = OffsetImage(img, zoom=zoom)
    im.image.axes = ax

    ab = AnnotationBbox(im, (x, y),  xybox=(0., 0.), frameon=False,
                        xycoords='data',  boxcoords="offset points", pad=0)

    ax.add_artist(ab)

def C_factor_logos(Total, giornate, Teams, tot_giornate, Logos):
    
    Total, __factors__ = calc_fortuna(Total, giornate, tot_giornate)
    
    fig = plt.figure(figsize=(10,6))
    ax=fig.add_subplot(111)

    plt.grid(which='major', axis='y', ls='-', alpha=0.25)
    xlabels = Total['Team']
    plt.xticks(Total.index, xlabels, rotation=45, ha='right')
    plt.axhline(y=0, xmin=-100, xmax=100, color='grey', ls='-')

    max_f = max(Total['IndiceFortuna'])
    min_f = np.min(Total['IndiceFortuna'])
    colors = get_team_colors(Teams)
    ax.bar(np.arange(0,8), Total['IndiceFortuna'], color=colors, lw=0, alpha=0.99, width=0.8, label='')

    for i, f in enumerate(list(np.round(Total['IndiceFortuna'],decimals=1))):
        if f<0: 
            va = 'top'
            offset = -0.1
        else: 
            va = 'bottom'
            offset = 0.1
        plt.annotate(f, (i, f+offset), horizontalalignment='center', verticalalignment=va, weight='bold')
        offset_image(Logos, i,f-4*offset, Total['Team'].iat[i], ax, zoom=0.15)

    plt.ylim(min_f-1, max_f+1)
    plt.ylabel('Indice Fortuna')
    title = 'C FACTOR | ' + str(giornate) + ' Giornate'
    plt.title(title, fontsize=20)




    ax.tick_params(axis='x', which='major')
    #for i, team in enumerate(Teams.keys()):
    #    offset_image(i, team, ax)

    plt.savefig('Plots/C_fact_Total.png')
    #plt.show()

def C_factor_logos_2(Total, giornate, Teams, tot_giornate, Logos):
    
    Total, __factors__ = calc_fortuna(Total, giornate, tot_giornate)
    
    df = Total
    df = df.sort_values('IndiceFortuna', ascending=True)
    
    fig = plt.figure(figsize=(6,8))
    ax=fig.add_subplot(111)

    plt.grid(which='major', axis='y', ls='-', alpha=0.25)
    ax.tick_params(left=False)
    #plt.axhline(y=0, xmin=-100, xmax=100, color='grey', ls='-')

    max_f = max(df['IndiceFortuna'])
    min_f = np.min(df['IndiceFortuna'])
    colors = get_team_colors(Teams)

    for team in df['Team']:
        df_ = df[df.Team == team]
        ax.barh(team.upper(), df_['IndiceFortuna'], color=Teams[team][1], lw=0, alpha=0.99, label='')

    #for i, f in enumerate(list(np.round(Total['IndiceFortuna'],decimals=1))):
        f = df_['IndiceFortuna'].iat[0]
        if f<0: 
            va = 'right'
            offset = -0.1
            color = 'r'
        else: 
            va = 'left'
            offset = 0.1
            color = 'tab:green'
        plt.annotate('%.1f' % f, (f+offset, team.upper()), color=color, verticalalignment='center', horizontalalignment=va, weight='bold')
        offset_image(Logos,-5*offset,team.upper(), team, ax, zoom=0.125)
                    
    plt.xlim(min_f-2, max_f+2)
    plt.xlabel('Indice Fortuna')
    title = 'C FACTOR | ' + str(giornate) + ' Giornate'
    #plt.title(title, fontsize=20, )
    plt.grid(axis='both', lw=0)

    ax.set_title('C FACTOR', fontweight='bold', loc='left')
    ax.set_title('Giornata: ' + str(giornate), fontweight='100', loc='right')


    ax.tick_params(axis='y', which='major')
    #for i, team in enumerate(Teams.keys()):
    #    offset_image(i, team, ax)


    #plt.show()

    plt.savefig('Plots/C_fact_Total.png')
    #plt.show()

def partial_totals(Results, giornate, tot_giornate, goal_marks):
    #--- build partial Total entries
    #print('... Filling Total df per round ...')
    Tot_per_round = []
    for gg in Results['luca'].index:
        data_per_round = make_Total_df(Results=Results, giornate = gg, goal_marks = goal_marks, verbose=False)
        #print(data_per_round.dtypes)
        __df__, __factors__ = calc_fortuna(data_per_round, giornate, tot_giornate)
        Tot_per_round.append(__df__)
    
    return Tot_per_round

def fortuna_evo(Results, Teams, Tot_per_round,  title='Indice Fortuna Evolution', ylabel='Indice Fortuna'):

    giornate = Results['luca'].index
    gg = max(giornate)
    ggfig = max(12,gg)
    fig = plt.figure(figsize=(ggfig*0.6,6))
    ax=fig.add_subplot(111)

    data = []
    for team in Teams.keys():
        dd = pd.DataFrame()
        score = 0
        scores = []
        for df in Tot_per_round:
            _ = df[df['Team'] == team]
            score = _['IndiceFortuna'].sum()
            #print(team, score)
            scores.append(score)
        dd['score'] = scores
        dd['Team'] = team
        data.append(dd)

    data = sorted(data,key=lambda x:x.at[gg-1,'score'].min(axis=0), reverse=True)

    for df in data:
        team = df['Team'].unique()[0]
        color = Teams[team][1]
        score = df.at[gg-1, 'score']
        score_prev = df.at[gg-2, 'score']
        diff = score - score_prev
        if diff > 0: sign='+'
        else: sign=''
        label = '%.1f (%s%.1f) | %s' % (score, sign, diff, team)
        p = ax.plot(giornate, df['score'], color=color, ls='-', lw=2, label=label)
        

    plt.xticks(np.arange(0,ggfig+1))
    ax.grid(axis='x', linestyle='-', linewidth=5, alpha=0.2)
    ax.grid(axis='y', alpha=0.2)
    plt.axhline(0, color='grey')
    plt.xlabel('Giornata')
    plt.ylabel(ylabel)
    plt.title(title)

    plt.legend(loc="left")
    plt.savefig('Plots/C_fact_Historic.png')
    #plt.show()
    
    
    
def premio_plot(Results, giornate, Teams, Logos, premio, Print = False):
    
    if premio == 'Porta Violata':
        par = 'goal_subiti_por'
        threshold=2
        title='Premio Porta Violata "Mario Bruno"'
        ylabel='Goal subiti dal portiere'
        integer=True
        
    elif premio == 'Panchina Oro':
        par='bonus_panchina'
        threshold=2
        title='Premio Panchina d\'Oro "Pietro Di Gangi"'
        ylabel='Bonus in Panchina'
        integer=False
    
    elif premio == 'Cartellino Facile':
        par='cartellini'
        threshold=3
        title='Premio Cartellino Facile "Palla Pazza"'
        ylabel='Cartellini'
        integer=True
        
    elif premio == 'Caduti':
        par='infortunati'
        threshold=4
        title='Premio Caduti "Luca Agozzino"'
        ylabel='Infortunati'
        integer=True
        
    elif premio == 'Catenaccio':
        par='mod_difesa'
        threshold=1.25
        title='Premio Catenaccio "Nanni Chiellini Giunta"'
        ylabel='Modificatore Difesa'
        integer=False
    
    
    gg = np.max([giornate,5])
    figsizex = np.max([gg,12])
    fig = plt.figure(figsize=(figsizex*0.6,6))
    ax=fig.add_subplot(111)  
    
    giornate_ = Results['luca'].index

    data = []
    for team, df in Results.items():
        if integer: df[par] = df[par].astype(int)
        df['cumsum'] = np.cumsum(df[par])
        score = max(df['cumsum'])
        df['score'] = score
        
        df_prev = df.drop(df.tail(1).index)         
        df_prev['cumsum_prev'] = np.cumsum(df_prev[par])
        score_prev = max(df_prev['cumsum'])
        df['score_prev'] = score_prev
                
        data.append(df)
    data = sorted(data,key=lambda x:x['score'].unique().min(axis=0), reverse=True)
    
    out = []
    for df in data:
        
        
        
        team = df['Team'].unique()[0]
        color = Teams[team][1]
        df['cumsum'] = np.cumsum(df[par])
        score = max(df['cumsum'])
        score_prev = max(df['score_prev'])
        diff = score - score_prev
        p = ax.plot(giornate_, df['cumsum'], color=color, ls='-', lw=2, label=str(score)+'   | +'+str(diff)+' |   '+str(team))
        #col = p[0].get_color()
        offset_image(Logos, giornate_[-1]+0.02*figsizex, df['cumsum'].iat[-1], team, ax, zoom=0.1)
        
        gior = df[df[par]>threshold].index
        dd = df[df.index.isin(gior)]
        marks = dd['cumsum']

        #cs = np.cumsum(dd[par])
        if integer: fs=14
        else: fs=10
        ax.scatter(gior, marks, edgecolor=color, facecolor=color, s=300, label='')
        for x,y,text in zip(gior,marks,dd[par]):
            ax.text(x, y,text, horizontalalignment='center', verticalalignment='center', color='white', fontsize=fs)
        
        dic = {}
        dic['team'] = team
        dic['points'] = score
        dic['points_last'] = diff
        out.append(dic)
        
    plt.xticks(np.arange(0,gg+1))
    ax.grid(axis='x', linestyle='-', linewidth=5, alpha=0.2)
    ax.set_xlabel('Giornata')
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=20)

    
    
    
    
    
    
    
    import matplotlib.lines
    from matplotlib.transforms import Bbox, TransformedBbox
    from matplotlib.legend_handler import HandlerBase
    from matplotlib.image import BboxImage

    class HandlerLineImage(HandlerBase):

        def __init__(self, path, space=15, offset = 10 ):
            self.space=space
            self.offset=offset
            self.image_data = plt.imread(path)        
            super(HandlerLineImage, self).__init__()

        def create_artists(self, legend, orig_handle,
                           xdescent, ydescent, width, height, fontsize, trans):

            l = matplotlib.lines.Line2D([xdescent+self.offset,xdescent+(width-self.space)/3.+self.offset],
                                         [ydescent+height/2., ydescent+height/2.])
            l.update_from(orig_handle)
            l.set_clip_on(False)
            l.set_transform(trans)

            bb = Bbox.from_bounds(xdescent +(width+self.space)/3.+self.offset,
                                  ydescent,
                                  height*self.image_data.shape[1]/self.image_data.shape[0],
                                  height)

            tbb = TransformedBbox(bb, trans)
            image = BboxImage(tbb)
            image.set_data(self.image_data)

            self.update_prop(image, orig_handle, legend)
            return [l,image]


    handles, labels = ax.get_legend_handles_labels()
    
    
    if Print:
        print(labels)

    #plt.legend([line, line2], ["", ""],
    #   handler_map={ line: HandlerLineImage("icon1.png"), line2: HandlerLineImage("icon2.png")}, 
    #   handlelength=2, labelspacing=0.0, fontsize=36, borderpad=0.15, loc=2, 
    #    handletextpad=0.2, borderaxespad=0.15)

    
    
    
    
    plt.legend()
    plt.savefig('Plots/plot_'+premio+'.png')
    #plt.show()
    return out

    
