#!/usr/bin/python3
import pandas as pd
import numpy as np
import pandas_gbq
import pydata_google_auth
import gspread
from gcloud import storage
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import os
from os import listdir
import requests
import json
from scripts.manipulation import normalize_cols
from scripts import vis_graphs
from datetime import datetime
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../credentials/gabinete_sv_credentials.json"



def _get_credentials_gbq():

    SCOPES = [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/drive',
    ]

    credentials = pydata_google_auth.get_user_credentials(
        SCOPES,
        # Set auth_local_webserver to True to have a slightly more convienient
        # authorization flow. Note, this doesn't work if you're running from a
        # notebook on a remote sever, such as over SSH or with Google Colab.
        auth_local_webserver=True,
    )

    return      credentials


def to_gbq(df, 
            table_name, 
            schema_name = 'simula_corona',
            project_id  = 'robusta-lab',
            **kwargs):
    """
    write a dataframe in Google BigQuery
    """
    
    destination_table = f'{schema_name}.{table_name}'

    pandas_gbq.to_gbq(
        df,
        destination_table,
        project_id,
        credentials = _get_credentials_gbq(),
        **kwargs
    )

def read_gbq(query, 
            project_id='robusta-lab', 
            **kwargs):
    """
    write a dataframe in Google BigQuery
    """

    return pandas_gbq.read_gbq(
        query,
        project_id,
        credentials=_get_credentials_gbq(),
        **kwargs)
    
    


def to_storage(bucket,bucket_folder,file_name,path_to_file):
    
    client = storage.Client(project='gavinete-sv')
    bucket = client.get_bucket(f'{bucket}')
    blob   = bucket.blob(f'{bucket_folder}/{file_name}')
    blob.upload_from_filename(f'{path_to_file}')
    
    print('Done!')
    
    

def read_sheets(sheet_name, workSheet=0):


    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('../../credentials/gabinete-sv-9aed310629e5.json', scope)
    gc          = gspread.authorize(credentials)
    if workSheet==0:
        wks         = gc.open(sheet_name).sheet1
    else:
        wks = gc.open(sheet_name).worksheet(workSheet)
        
    data        = wks.get_all_values()
    headers     = data.pop(0)

    return pd.DataFrame(data, columns=headers)


def load_brasilIO():
    ####### IMPORT DATA ######
    brio = pd.read_csv('https://data.brasil.io/dataset/covid19/caso_full.csv.gz')


    mask = ((brio['is_last']==True) & (brio['place_type']=='city') & (brio['last_available_confirmed_per_100k_inhabitants'].notnull()))
    cols = ['city_ibge_code','city','last_available_confirmed','last_available_deaths','date','state']
    df_final = brio[mask][cols]
    df_final = df_final.rename(columns={'last_available_confirmed':'confirmed','last_available_deaths':'deaths'})

    return df_final, brio


def load_wcota():
    df          = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
    df['state'] = df['state'].str.replace('TOTAL','BRASIL')
    # df.to_csv('brasil_states.csv', index=False)
    dd          = df.drop(['country','deaths'],1)
    
    return dd


def load_total_table():
    final_data = pd.read_csv('../data/cumulative_data/covid_last.csv')
    codes = pd.read_csv('../data/country_codes.csv')

    df = final_data.copy()
    df.columns = normalize_cols(df.columns)

    df = pd.merge(df,codes,on='countryname', how='left')
    country_rename = {'US':'United States', 'UK':'United Kingdom', "Brazil":"Brasil"}
    df['countryname'] = df['countryname'].replace(country_rename)


    df_pop = pd.read_csv('../data/world_population.csv')

    df = pd.merge(df,df_pop,on='countryname', how='left')
    mask = ((df['population'].notnull()) & (df['countrycode'].notnull()))
    df = df[mask]
    
    return df



def load_cities(brio_raw):
    #sp

    citys =[3550308]

    mask = brio_raw['city_ibge_code'].isin(citys)

    cols = ['last_available_date','city','last_available_confirmed','new_confirmed','new_deaths']

    sp = brio_raw[mask][cols]
    sp['death'] = sp['new_deaths'].cumsum()

    rename_cols = {
        'last_available_date':'date',
        'last_available_confirmed':'confirmed',
        'new_confirmed':'new_confirmed',
        'death':'deaths',
        'new_deaths':'new_deaths',
    }

    sp = sp.rename(columns = rename_cols)

    cols = ['date','city','confirmed','new_confirmed','deaths','new_deaths']

    sp = sp[cols]


    # taubate
    tb_cases = read_sheets('covid19_taubate', 'evolucao')
    tb_cases['data'] = pd.to_datetime(tb_cases['data'], format = "%d/%m/%Y")
    tb_cases = tb_cases.sort_values(by='data', ascending=True)

    for col in tb_cases.columns[1:]:
        tb_cases[col] = pd.to_numeric(tb_cases[col])

    for col in ['analise','confirmado','descartado','obito','internado','em_analise']:

        tb_cases[f'{col}_day'] = tb_cases[col] - tb_cases[col].shift(1).fillna(0)
        tb_cases[f'{col}_day'] = tb_cases[f'{col}_day'].astype(int)

    cols = ['data'] + np.sort(tb_cases.columns[1:]).tolist()
    tb_cases = tb_cases[cols]
    tb_cases['city'] = 'Taubaté'

    cols = ['data','city','confirmado', 'confirmado_day','obito','obito_day']

    tb = tb_cases[cols]

    rename_cols = {
        'data':'date',
        'confirmado':'confirmed',
        'confirmado_day':'new_confirmed',
        'obito':'deaths',
        'obito_day':'new_deaths',
    }

    tb = tb.rename(columns = rename_cols)


    sjc = read_sheets('covid19_sjc')

    cols =  ['data','confirmado','obito']
    sjc = sjc[cols]

    sjc['data'] = pd.to_datetime(sjc['data'], format = "%d/%m/%Y")


    for col in sjc.columns[1:]:
        sjc[col] = pd.to_numeric(sjc[col])


    sjc['city'] = 'São José dos Campos'

    sjc = sjc.sort_values(by='data')
    sjc = sjc.fillna(method='ffill')

    for var in ['confirmado','obito']:
        sjc[f'{var}_shift']   = sjc[f'{var}'].shift(1)
        sjc[f'new_{var}']       = sjc[f'{var}'] - sjc[f'{var}_shift']

    cols = ['data','city','confirmado','new_confirmado', 'obito', 'new_obito']
    sjc = sjc[cols]

    rename_cols = {
        'data':'date',
        'confirmado':'confirmed',
        'new_confirmado':'new_confirmed',
        'obito':'deaths',
        'new_obito':'new_deaths',
    }

    sjc = sjc.rename(columns = rename_cols)
    sjc = sjc.fillna(0)



    cities = pd.concat([sp,tb,sjc])
    cities['date'] = pd.to_datetime(cities['date'])
    cities = cities.reset_index(drop=True)
    
    return cities




def update_ms_data():

    path=os.getcwd().split('9')[0]+ '9/' + 'data/ministerio_da_saude'

    initial_files = listdir(path)

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.dir",path);
    profile.set_preference("browser.download.folderList",2);
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");
    profile.set_preference("browser.download.manager.showWhenStarting",False);
    profile.set_preference("browser.helperApps.neverAsk.openFile","application/csv,application/excel,application/vnd.msexcel,application/vnd.ms-excel,text/anytext,text/comma-separated-values,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream");
    profile.set_preference("browser.helperApps.alwaysAsk.force", False);
    profile.set_preference("browser.download.manager.useWindow", False);
    profile.set_preference("browser.download.manager.focusWhenStarting", False);
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False);
    profile.set_preference("browser.download.manager.showAlertOnComplete", False);
    profile.set_preference("browser.download.manager.closeWhenDone", True);
    profile.set_preference("pdfjs.disabled", True);

    # year = '2019'

    firefox = webdriver.Firefox(firefox_profile=profile)

    # firefox = webdriver.Firefox()
    url = 'https://covid.saude.gov.br/'

    firefox.get(url)
    # firefox.request('POST', url,)

    time.sleep(5)

    download_button = firefox.find_elements_by_xpath('/html[1]/body[1]/app-root[1]/ion-app[1]/ion-router-outlet[1]/app-home[1]/ion-content[1]/div[1]/div[2]/ion-button[1]')[0]
    download_button.click()

    time.sleep(3)

    firefox.quit()

    now_files = listdir(path)


    today = datetime.today().strftime('%Y-%m-%d-%H-%M')    
    new_file = [file for file in now_files if file not in initial_files][0]
    os.rename(path+f'/{new_file}', path+f'/{today}_ms_covid19.csv')
    df = pd.read_csv(path+f'/{today}_ms_covid19.csv', sep=';')
    df['last_update'] = datetime.today().strftime('%Y-%m-%d %H:%M')  
    df.to_csv('../data/ministerio_da_saude/last_data_ms_covid19.csv', index=False, encoding='utf-8')