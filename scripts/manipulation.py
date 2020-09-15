import pandas as pd
import numpy as np
import geopandas as gpd
import unicodedata



def normalize_cols(df):
    return df.str.normalize('NFKD').str.replace("$","").str.replace("(","").str.replace(")","").str.replace('-','').str.replace(' ','_').str.lower().str.replace('.','')


def remove_acentos(s):
    ss =  ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    
    return ss.lower().replace(' ','_')

def manipulate_eucenter(df):
    rename_cols = {
        'dateRep':'date',
        'cases':'new_confirmed',
        'deaths':'new_deaths',
        'countriesAndTerritories':'countryname',
        'geoId':'countrycode',
        'popData2018':'population',
        'continentExp':'continent',
    }
    
    df = df.rename(columns=rename_cols)
    
    cols = ['date','countrycode','countryname','population','new_confirmed','new_deaths']
    
    df = df[cols]
    
    
    df['date'] = pd.to_datetime(df['date'])
    df      = df.sort_values(by=['countryname','date'])
    
    df['confirmed'] = df[['countryname','new_confirmed']].groupby(by='countryname').cumsum()
    
    df['deaths'] = df[['countryname','new_deaths']].groupby(by='countryname').cumsum()

    cols             = ['date','countrycode','countryname','population','confirmed','new_confirmed','deaths','new_deaths']
    df = df[cols]
    
    df = df.sort_values(by=['countryname'], ascending=False)
    df = df.sort_values(by=['date'])
    
    
    return df
    


def create_all_country_total_data(df, vars):
    df.columns = normalize_cols(df.columns)

    df['date'] = pd.to_datetime(df['date'])
    df      = df.sort_values(by=['countryname','date'])
    
    df['active'] = df['confirmed'] - df['recovered'] - df['deaths']

    df['countryname_shift'] = df['countryname'].shift(1)
    
    new_vars = []
    
    for var in vars:
        df[f'{var}_shift']   = df[f'{var}'].shift(1)
        df[f'{var}_shift'] = np.where(df['countryname_shift']!=df['countryname'], 0 , df[f'{var}_shift'])
        df[f'new_{var}']       = df[f'{var}'] - df[f'{var}_shift']
        
        new_vars.append(var)
        new_vars.append(f"new_{var}")

    cols             = ['date','countrycode','countryname','population'] + new_vars
    df               = df[cols]

    df = df.sort_values(by=['countryname'], ascending=False)
    df = df.sort_values(by=['date'])
    
    return df



def get_mytable_old_format(df):
    mask = (df['estado'].notnull()) & (df['municipio'].isnull()) & (df['codmun'].isnull())
    df = df[mask]

    vars = ['casosAcumulado','obitosAcumulado']

    df['data'] = pd.to_datetime(df['data'])
    df      = df.sort_values(by=['estado','data'])

    df['countryname_shift'] = df['estado'].shift(1)

    new_vars = []

    for var in vars:
        df[f'{var}_shift']   = df[f'{var}'].shift(1)
        df[f'{var}_shift'] = np.where(df['countryname_shift']!=df['estado'], 0 , df[f'{var}_shift'])
        df[f'new_{var}']       = df[f'{var}'] - df[f'{var}_shift']

        new_vars.append(var)
        new_vars.append(f"new_{var}")
        
    cols = ['regiao','estado','data','new_casosAcumulado','casosAcumulado','new_obitosAcumulado','obitosAcumulado','last_update']

    df = df[cols]
    df = df.rename(columns={'new_casosAcumulado':'casosNovos','new_obitosAcumulado':'obitosNovos'})

    return df


def manipule_mytable(df,config_mstable):
    df = get_mytable_old_format(df)
    rename_cols = config_mstable['rename_cols']
    df = df.rename(columns=rename_cols)

    df = df[df['deaths'].notnull()]
    try:
        df['date'] = pd.to_datetime(df['date'], format = config_mstable['date_format'][0])
    except:
        df['date'] = pd.to_datetime(df['date'], format = config_mstable['date_format'][1])

    last_update = df['last_update'].values[0]
    
    
    for col in ['confirmed','new_confirmed','deaths','new_deaths']:
        df[col] = pd.to_numeric(df[col])

    df_states         = df.sort_values(by=['date','confirmed'], ascending=False)
    df_states['city'] = df_states['state']
    
    br = df_states.groupby(by=['date'], as_index=False).sum()

    br['state']  = 'BRASIL'
    br['city']   = 'BRASIL'
    br['regiao']   = 'Brasil'
    br['last_update'] = last_update
    
    df_states        = pd.concat([df_states,br[df_states.columns]],axis=0)

    df_states         = df_states.sort_values(by=['date','confirmed'], ascending=False)

    mask   = (df_states['state']!='BRASIL') & (df_states['state']!='SP')
    not_sp = df_states[mask].groupby(by=['date'], as_index=False).sum()

    not_sp['state']  = 'BRASIL SEM SP'
    not_sp['city']   = 'BRASIL SEM SP'
    not_sp['regiao']    = 'Brasil sem SP'
    not_sp['last_update'] = last_update

    df_states        = pd.concat([df_states,not_sp[df_states.columns]],axis=0).sort_values(by=['date','confirmed'], ascending=False)
    
    return df_states

def manipulate_for_br_maps(df,municipios,maps, df_states,ufs):
    
    df['city_ibge_code'] = df['city_ibge_code'].astype(int)
    municipios['geocodigo'] = municipios['geocodigo'].astype(int)
    maps['CD_GEOCMU'] = maps['CD_GEOCMU'].astype(int)
    
    cols = ['geocodigo','state','city','nome_uf','nome_mesorregiao','nome_municipio','confirmed','deaths','date']

    dd   = pd.merge(df,municipios, left_on='city_ibge_code', right_on='geocodigo', how = 'left')[cols]

    

    final = pd.merge(dd,maps, left_on='geocodigo', right_on='CD_GEOCMU', how='left').drop(['CD_GEOCMU','NM_MUNICIP'],1)

    final     =  final[final['geometry'].notnull()]
    final     = gpd.GeoDataFrame(final)
    final.crs = {'init' :'epsg:4326'}

    rename_cols = {
        'nome_municipio':'Município',
        'nome_uf'       : 'Estado',
        'confirmed'     : 'Confirmados',
        'deaths'        : 'Óbitos',
        'date'          : 'Data do Boletim'
        }
    final = final.rename(columns=rename_cols)


    mask    = df_states['date'] == max(df_states['date'])
    estados = df_states[mask]


    ff      = final[['state','Estado']].drop_duplicates()
    estados = pd.merge(estados,ff,on='state', how='inner')

    estados['NM_ESTADO'] = estados['Estado'].str.upper()
    estados = pd.merge(estados,ufs, on = 'NM_ESTADO')

    estados     = gpd.GeoDataFrame(estados)
    estados.crs = {'init' :'epsg:4326'}
    
    rename_cols = {
        'confirmed' : 'Confirmados',
        'deaths'    : 'Óbitos',
        'new_confirmed' : 'Novos Casos',
        'new_deaths': 'Novas Mortes',
        'date'      : 'Data do Boletim'
        }
    
    estados = estados.rename(columns=rename_cols)
    
    estados['Data do Boletim'] = estados['Data do Boletim'].astype(str)
    
    return final, estados

def manipulate_vale_data(df):
    cols = ['suspeitas','suspeitas_internados','confirmados_internados','confirmados','descartados','mortes','recuperados']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
       
    df['internados'] = df['suspeitas_internados'] + df['confirmados_internados'].fillna(0)
 
    df = df.fillna('-').replace('','-')
    
    df['ocupacao_uti'] = df['ocupacao_uti'].apply(lambda x: f"{x}%" if x!='-' else '-')
    df['ocupacao_enfermaria'] = df['ocupacao_enfermaria'].apply(lambda x: f"{x}%" if x!='-' else '-')
    
    df['nome_municipio'] = df['municipio']
    
    return df

def manipulate_for_vale_maps(df, municipios_sp, estados, config):
    
    vale = pd.merge(df,municipios_sp[['nome_municipio','geometry']],on='nome_municipio', how='left')
    vale = vale[vale['geometry'].notnull()]
    vale = gpd.GeoDataFrame(vale)
    vale.crs = {'init' :'epsg:4326'}
    
    col_rename =config['col_rename']

    vale = vale.rename(columns=col_rename)
    vale['Estado'] = 'São Paulo'
    return vale, estados    

def create_br_not_sp(df):
    
    ### GET ONLY DA STATES TO MAKE THE BRASIL DATA
    mask = df['place_type'] == 'state'
    df['city'] = np.where(mask,df['state'],df['city'] )

    ### SUM STATES DATA
    mask = (df['place_type']=='state')
    df_brasil = df[mask].groupby(by=['date'], as_index=False).sum()

    ### FILL DATA FOR BRASIL
    df_brasil['city']                      = 'BRASIL'
    df_brasil['city_ibge_code']            = 0
    df_brasil['estimated_population_2019'] = 209*10**6
    df_brasil['death_rate']                = np.nan
    df_brasil['is_last']                   = [False for i in range(len(df_brasil)-1)] + [True]
    df_brasil['place_type']                = 'country'
    df_brasil['state']                     = 'BR'


    ### SUM STATES DATA
    mask = (df['place_type']=='state') & (df['state']!='SP')
    not_sp = df[mask].groupby(by=['date'], as_index=False).sum()

    ### FILL DATA FOR BRASIL
    not_sp['city']                      = 'Exceto SP'
    not_sp['city_ibge_code']            = 1
    not_sp['estimated_population_2019'] = 209*10**6 - 45919049
    not_sp['death_rate']                = np.nan
    not_sp['is_last']                   = [False for i in range(len(not_sp)-1)] + [True]
    not_sp['place_type']                = 'state'
    not_sp['state']                     = 'not_sp'

    df = pd.concat([df_brasil[df.columns],not_sp[df.columns],df],axis=0)

    df['confirmed_shift'] = df['confirmed'].shift(1)
    df['deaths_shift']    = df['deaths'].shift(1)

    df['countryname']       = df['city']
    df['countryname_shift'] = df['countryname'].shift(1)



    df['confirmed_shift'] = np.where(df['countryname_shift']!=df['countryname'], 0 , df['confirmed_shift'])
    df['new_confirmed']       = df['confirmed'] - df['confirmed_shift']

    df['deaths_shift'] = np.where(df['countryname_shift']!=df['countryname'], 0 , df['deaths_shift'])
    df['new_deaths']   = df['deaths'] - df['deaths_shift']
    ''
    cols = ['city','city_ibge_code', 'date', 'confirmed','new_confirmed','deaths','new_deaths', 'estimated_population_2019','place_type','state']
    df   = df[cols]

    return df