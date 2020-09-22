#!/home/m/anaconda3/bin/python

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
pd.options.display.max_columns = 999
pd.options.display.max_rows = 999
pd.options.display.max_colwidth = 100

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

import requests

from os import listdir
import unicodedata

from paths import *
from scripts.manipulation import remove_acentos
from scripts.manipulation import normalize_cols
from scripts import scrap_data
from scripts import manipulation
from scripts import io
from scripts import vis_graphs
from scripts import vis_maps

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

import yaml
from subprocess import call
import geopandas as gpd



def run_corona_mundo():
    
    # LOAD and SAVE DATA from WORDMETERS
    new_data, df_final = scrap_data.load_data()
    df_wordmeters = io.load_total_table()
    df_wordmeters = manipulation.create_all_country_total_data(df_wordmeters, vars = ['confirmed','deaths','recovered','active'])

    ### Generate Graphs for Multiple Countrys
    df = df_wordmeters.copy()

    codes = ['BR','IT','ES','US','CN','KR','DE','FR','UK','IN', 'TR','MX','RU']
    mask_countrys = df['countrycode'].isin(codes)

    from scripts import vis_layout
    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)

    themes = themes['all_countrys']
    for var in themes['vars'].keys():
        for scale in themes['axis_legend']['scale'].keys():
            fig = vis_graphs.all_countrys(df[mask_countrys], var, scale, themes, save=False)
            
    #         plot(fig, filename=f"../images/multipleCountry/{var}_{scale}.html", auto_open=False)
            plot(fig, filename=f"../../sample_pages/pages/covid-19/images/multipleCountry/{var}_{scale}.html", auto_open=False)



    ## By Country

    df = df_wordmeters.copy()

    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['unique_country_daily']

    codes = ['BR','IT','ES','US','CN','KR','DE','FR','UK','IN', 'TR','MX','RU']

    # codes =['BR']
    for countrycode in codes:
        mask = ((df['countrycode']==countrycode) & (df['confirmed']>0))
        fig = vis_graphs.unique_country(df[mask],themes)
    #     plot(fig, filename=f"../images/singleCountry/{countrycode}.html", auto_open=False)
        plot(fig, filename=f"../../sample_pages/pages/covid-19/images/singleCountry/{countrycode}_daily.html", auto_open=False)


    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['unique_country_cum']
    # codes =['BR']
    for countrycode in codes:
        mask = ((df['countrycode']==countrycode) & (df['confirmed']>0))
        fig = vis_graphs.unique_country(df[mask],themes)
    #     plot(fig, filename=f"../images/singleCountry/{countrycode}.html", auto_open=False)
        plot(fig, filename=f"../../sample_pages/pages/covid-19/images/singleCountry/{countrycode}_cum.html", auto_open=False)

def run_corona_br():
    from scripts.manipulation import remove_acentos
    from scripts.manipulation import normalize_cols
    from scripts import scrap_data
    from scripts import manipulation
    from scripts import io
    from scripts import vis_graphs
    from scripts import vis_maps
    ## Estados
    from scripts.io import read_sheets
    from scripts import manipulation
    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)

    io.update_ms_data()
    print('io done!')

    df = pd.read_csv("../data/ministerio_da_saude/last_data_ms_covid19.csv")

    df_states = manipulation.manipule_mytable(df,config['ms_table'])

    print("States table, Done!")
    
    
    
    ###Multiple
    from scripts import vis_graphs

    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['brasil_vis_cumulative']

    for var in themes['vars'].keys():
        for scale in themes['axis_legend']['scale'].keys():
            fig = vis_graphs.brasil_vis_cum(df_states, var,scale, themes)
            
            plot(fig, filename=f"../../sample_pages/pages/covid-19/images/brasil/cumulative/{var}_{scale}.html", auto_open=False)


    ## Diario
    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['brasil_vis_daily']

    codes = df_states['state'].unique()

    for state in codes:
        mask = ((df_states['state']==state) & (df_states['confirmed']>0))
        fig = vis_graphs.unique_country(df_states[mask], themes)

        plot(fig, filename=f"../../sample_pages/pages/covid-19/images/brasil/daily/{state}_daily.html", auto_open=False)
        
        
    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['brasil_vis_cum']


    for state in codes:
        mask = ((df_states['state']==state) & (df_states['confirmed']>0))
        fig = vis_graphs.unique_country(df_states[mask], themes)

        plot(fig, filename=f"../../sample_pages/pages/covid-19/images/brasil/daily/{state}_cum.html", auto_open=False)
        
        
        
    from scripts import io

    call('rm ../data/brIO/caso_full.csv', shell=True)

    call('cd ../data/brIO/', shell=True)
    call('wget https://data.brasil.io/dataset/covid19/caso_full.csv.gz -P ../data/brIO/' , shell=True)
    print('brIO downloaded')
    call('gunzip ../data/brIO/caso_full.csv.gz' , shell=True)


    brio, brio_raw = io.load_brasilIO()

    print("Br.IO table, Done!")
    
    
    
    ### Load Cities
    cities = io.load_cities(brio_raw)
    
    
    from scripts import vis_graphs

    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['cities']

    for var in themes['vars'].keys():
        for scale in themes['axis_legend']['scale'].keys():
            fig = vis_graphs.brasil_vis_cum(cities, var,scale, themes)
            
            plot(fig, filename=f"../../sample_pages/pages/covid-19/images/vale/cumulative/{var}_{scale}.html", auto_open=False)


    import unidecode

    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['cities_vis_daily']

    codes = ['São Paulo', 'Taubaté', 'São José dos Campos']

    for state in codes:
        mask = ((cities['city']==state) & (cities['confirmed']>0))
        fig = vis_graphs.unique_country(cities[mask], themes)
        plot(fig, filename=f"../../sample_pages/pages/covid-19/images/vale/daily/{unidecode.unidecode(state.replace(' ','_').lower())}_daily.html", auto_open=False)

        
    themes = yaml.load(open('../themes/sample_pages.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['cities_vis_cum']
    for state in codes:
        mask = ((cities['city']==state) & (cities['confirmed']>0))
        fig = vis_graphs.unique_country(cities[mask], themes)
        plot(fig, filename=f"../../sample_pages/pages/covid-19/images/vale/daily/{unidecode.unidecode(state.replace(' ','_').lower())}_cum.html", auto_open=False)
        print(unidecode.unidecode(state.replace(' ','_').lower()))
        
        
        


def _generate_and_upload_br_map(final, estados, map_config):
    #generate map
    cols = ['Município','Estado','Confirmados', 'Óbitos', 'Data do Boletim']

    print('Generate and save br map..')
    mymap =  vis_maps.get_map(final,'Confirmados', cols, estados)
    mymap.save(f'{map_config["path_save"]}{map_config["save_name"]}')

    print('Upload br map..')
    io.to_storage(bucket=map_config['bucket'],
                bucket_folder=map_config['bucket_folder'],
                file_name=map_config['save_name'],
                path_to_file=f'{map_config["path_save"]}{map_config["save_name"]}')

    os.remove(f'{map_config["path_save"]}{map_config["save_name"]}')
    
def _generate_and_upload_vale_map(vale, estados, map_config,config):
    #generate map
    cols = list(config['vale_map']['col_rename'].values())
    cols.remove('Fonte')
    
    print('Generate and save vale map..')
    mymap =  vis_maps.get_map_vale(vale,'Confirmados', cols, estados)
    mymap.save(f'{map_config["path_save"]}{map_config["save_name"]}')

    print('Map Done!')
#     io.to_storage(bucket=map_config['bucket'],
#               bucket_folder=map_config['bucket_folder'],
#               file_name=map_config['save_name'],
#               path_to_file=f'{map_config["path_save"]}{map_config["save_name"]}')
    
#     os.remove(f'{map_config["path_save"]}{map_config["save_name"]}')
#     return(mymap)

def run_coronaBR():
    brio, brio_raw = io.load_brasilIO()

    import yaml

    from scripts.io import read_sheets
    from scripts import manipulation
    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)

    # io.update_ms_data()

    df = pd.read_csv("../data/ministerio_da_saude/last_data_ms_covid19.csv")


    df = df.drop_duplicates(subset = ['regiao', 'estado', 'data', 'casosAcumulado', 'obitosAcumulado', 'last_update'])


    df_states = manipulation.manipule_mytable(df,config['ms_table'])

    vale = read_sheets('covid19_vale_do_paraiba_e_litoral_norte').replace('',0)
    print("Vale table, Done!")
    
    br = io.load_total_table()
    br = manipulation.create_all_country_total_data(br, vars = ['confirmed','deaths','recovered','active'])
    
    
    from scripts import vis_html

    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)

    vis_html.create_cards(df_states,vale, br ,config['embed_html'])


    #     io.to_storage(bucket='sv-covid19',
    #               bucket_folder='site/full',
    #               file_name=files[model],
    #               path_to_file=path+files[model])
        
    # print("Embed link uploaded")
    
    from scripts import vis_graphs

    themes = yaml.load(open('../themes/custom_colorscales.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['brasil_vis_cumulative']

    for var in themes['vars'].keys():
        for scale in themes['axis_legend']['scale'].keys():
            fig = vis_graphs.brasil_vis_cum(df_states, var,scale, themes)
            
            plot(fig, filename=f"../site/sv_br_vale/coronavirus/images/cumulative/brasil_por_estado_{var}.html", auto_open=False)


    themes = yaml.load(open('../themes/custom_colorscales.yaml', 'r'), Loader=yaml.FullLoader)
    themes = themes['brasil_vis_daily']

    codes = ['BRASIL','SP']

    for state in codes:
        mask = ((df_states['state']==state) & (df_states['confirmed']>0))
        fig = vis_graphs.unique_country(df_states[mask], themes)

        plot(fig, filename=f"../site/sv_br_vale/coronavirus/images/daily/{state}.html", auto_open=False)
        
        
        
        
    #####MAPS
    print('Start Br Map')
    #minicipales data
    municipios = pd.read_csv('../data/br_municipios_ibge.csv', dtype={'geocodigo':str})
    df = brio.copy()

    #load shape files;
    ufs = gpd.read_file('../../mapas_brasil/estados-ibge/BRUFE250GC_SIR.shp')
    maps = gpd.read_file('../../mapas_brasil/municipios-ibge/brasil-municipios.shp')


    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)

    #prepare data for map
    final, estados = manipulation.manipulate_for_br_maps(brio, municipios, maps, df_states.drop(['regiao'],1), ufs)

    # _generate_and_upload_br_map(final, estados, config['br_map'])
    
    
    
    ### VALE MAPS
    from scripts.io import read_sheets
    from scripts import manipulation
    #download and manipulate vale data
    df = read_sheets('covid19_vale_do_paraiba_e_litoral_norte')
    df = manipulation.manipulate_vale_data(df)

    #load shape files
    municipios_sp = gpd.read_file('../../brasil_geodata/maps/sp_municipios.json')
    ufs = gpd.read_file('../../mapas_brasil/estados-ibge/BRUFE250GC_SIR.shp')
    
    
    ## Manipulate data for generate map
    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)

    vale, estados = manipulation.manipulate_for_vale_maps(df, municipios_sp, estados,config['vale_map'])

    _generate_and_upload_vale_map(vale, estados, config['vale_map'], config)
    
    
    
    #https://pypi.org/project/ftpretty/
    from ftpretty import ftpretty
    import ftplib
    import yaml
    import os
    credentials = yaml.load(open('../../credentials/ftp_credentials.yaml', 'r'), Loader=yaml.FullLoader)
    
    host = credentials['ftp']['host']
    user = credentials['ftp']['user']
    pw   = credentials['ftp']['pw']

    f = ftpretty(host, user, pw)

    local_folder  = '../site/sv_br_vale/coronavirus'
    remote_folder = 'public_html/coronavirus'

    f.upload_tree(local_folder, remote_folder)
    
    print('DONE')

def run_coronaVale():
    from scripts.manipulation import remove_acentos
    from scripts.manipulation import normalize_cols
    from scripts import scrap_data
    from scripts import manipulation
    from scripts import io
    from scripts import vis_graphs

    sp_full = pd.read_csv('https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv', sep=';')
    sp_full['nome_drs'] = np.where(sp_full['nome_munic']=='São Paulo','Município de São Paulo',sp_full['nome_drs'])


    cols = ['datahora','nome_munic','codigo_ibge','casos','casos_novos','obitos','obitos_novos','nome_drs']

    mask = sp_full['nome_drs'].isin(['Taubaté'])
    vale = sp_full[mask][cols]


    rename_cols = {
        "casos":"casos_tbt",
        "casos_novos":"casos_novos_tbt",
        "obitos":"obitos_tbt",
        "obitos_novos":"obitos_novos_tbt",
    }
    vale_ = vale.groupby(by=['nome_drs','datahora'], as_index=False).sum()

    vale_['nome_munic'] = 'Vale'
    vale_['codigo_ibge'] = 0


    vale = pd.concat([vale,vale_], axis=0)

    vale_ = vale_.rename(columns = rename_cols).drop(columns=['nome_munic','codigo_ibge'])
    vale = vale.merge(vale_, on=['nome_drs','datahora'])


    cols = ['casos','obitos','casos_tbt','obitos_tbt']


    dd_final_all = pd.DataFrame()

    for municipio in vale['nome_munic'].unique():
        tbt = vale[vale['nome_munic']==municipio]

        for col in cols:
            

            tbt[f'{col}_shift_7'] = tbt[f'{col}'].shift(7)
            tbt[f'{col}_shift_14'] = tbt[f'{col}'].shift(14)


            tbt[f'{col}_7d'] = tbt[f'{col}'] - tbt[f'{col}_shift_7']
            tbt[f'{col}_14d'] = tbt[f'{col}'] - tbt[f'{col}_shift_14']


            tbt[f'{col}_shift_14'] = tbt[f'{col}_7d'].shift(7)

            tbt[f'{col}_var'] = tbt[f'{col}_7d']/tbt[f'{col}_shift_14']
            
            tbt = tbt.drop(columns = [f'{col}_shift_14',f'{col}_shift_7',])



    #     dd = tbt[['datahora','nome_munic',f'{col}',f'{col}_7',f'{col}_14d',f'{col}_var']]

        dd_final_all = pd.concat([dd_final_all,tbt], axis=0)


        


    vale_final = dd_final_all.copy()

    vale_final['casos_tbt'] = 100 * vale_final['casos'] / vale_final['casos_tbt'] 
    vale_final['casos_novos_tbt'] = 100 * vale_final['casos_novos'] / vale_final['casos_novos_tbt'] 
    vale_final['obitos_tbt'] = 100 * vale_final['obitos'] / vale_final['obitos_tbt'] 
    vale_final['obitos_novos_tbt'] = 100 * vale_final['obitos_novos'] / vale_final['obitos_novos_tbt'] 
    vale_final = vale_final.fillna(0)
    vale_final = vale_final.sort_values(by=['datahora','nome_munic'])
    vale_final['codigo_ibge'] = vale_final['codigo_ibge'].astype(int)
    vale_final['datahora'] = pd.to_datetime(vale_final['datahora'])
    
    
    #load br cities
    geo_sp = gpd.read_file('../../brasil_geodata/maps/sp_municipios.json')
    # cols = ['geocodigo','nome_mesorregiao','geometry']
    cols = ['geocodigo','nome_mesorregiao','nome_municipio']
    geo_sp = geo_sp[cols]
    
    
    
    #load state data
    url  = 'http://datasource.coronacidades.org/'
    data = 'br/states/rt'

    ds = pd.read_csv(f'{url}{data}')

    ds['last_updated'] = pd.to_datetime(ds['last_updated'])

    sp = ds[ds['state_num_id']==35]
    sp = sp.rename(columns={'state_num_id':'city_id'})
    sp['city_id'] = 'SP'
    sp['nome_mesorregiao'] = 'SP'
    sp['nome_municipio']   = 'Estado de SP'

    # rj = ds[ds['state']=='RJ']
    # rj = rj.rename(columns={'state':'city_id'})
    # rj['nome_mesorregiao'] = 'RJ'
    # rj['nome_municipio']   = 'Estado do RJ'

    # mg = ds[ds['state']=='MG']
    # mg = mg.rename(columns={'state':'city_id'})
    # mg['nome_mesorregiao'] = 'MG'
    # mg['nome_municipio']   = 'Estado de MG'

    # am = ds[ds['state']=='AM']
    # am = am.rename(columns={'state':'city_id'})
    # am['nome_mesorregiao'] = 'AM'
    # am['nome_municipio']   = 'Estado de AM'
    
    
    
    #load cities data
    data = 'br/cities/rt'

    df = pd.read_csv(f'{url}{data}')

    df['last_updated'] = pd.to_datetime(df['last_updated'])

    
    dd = df.merge(geo_sp, how='right', left_on = 'city_id', right_on = 'geocodigo')
    dd.head()


    regiao = 'Vale do Paraíba Paulista'
    mask = (dd['nome_mesorregiao']==regiao)
    vale = dd[mask]
    vale = vale[vale['city_id'].notnull()]

    mask = (dd['nome_municipio']=='São Paulo')
    sp_city = dd[mask]


    vale = pd.concat([vale,sp_city], 0)
    vale = pd.concat([vale,sp], 0)

    vale['geocodigo'] = vale['geocodigo'].fillna(111).astype(int)
    
    vale = vale.rename(columns={'geocodigo':'codigo_ibge','last_updated':'datahora'})
    vale['datahora'] = pd.to_datetime(vale['datahora'])
        
    
    mask = vale['datahora']== max(vale['datahora'])
    vale_rt_last = vale[mask]
    vale_rt_last = vale_rt_last.drop(columns=['datahora'])
    vale_rt_last = vale_rt_last.rename(columns={'nome_municipio':'municipio'})
    
    
    
    mask = vale_final['nome_munic']=='Vale'
    just_vale = vale_final[mask]
    just_vale = just_vale.drop(columns=['nome_munic'])
    just_vale['last_update'] = max(just_vale['datahora'])
        #upload to drive
    from scripts import io
    io.to_gbq(vale_final,'vale_covid','covid','gabinete-sv', if_exists='replace')
    io.to_gbq(just_vale,'just_vale_covid','covid','gabinete-sv', if_exists='replace')
    io.to_gbq(vale,'rt_vale_covid','covid','gabinete-sv', if_exists='replace')
    io.to_gbq(vale_rt_last,'vale_rt_last','covid','gabinete-sv', if_exists='replace')
    io.to_gbq(just_vale,'just_vale_covid','covid','gabinete-sv', if_exists='replace')
    
    
    
    
    
    from scripts import manipulation_sp

    casos_full = pd.read_csv('https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv', sep=';')
    casos, sp_casos = manipulation_sp.padronize_casos(casos_full)
    
    internacoes_full = pd.read_csv('https://github.com/seade-R/dados-covid-sp/raw/master/data/plano_sp_leitos_internacoes.csv', sep=';')
    internacoes, sp_internacoes = manipulation_sp.padronize_internacoes(internacoes_full)
        
    
    uti = pd.read_csv('../data/sp_gov/uti_ocupacao.csv', sep=';')

    uti_final = uti.copy()


    # mask =  uti_final['datahora'] == max(uti_final['datahora'])

    # uti_final = uti_final[mask]

    # uti_final['datahora'] = max(df_final['datahora'])
        
        
        
    #merge all tables
    df = manipulation_sp.padronize_planosp(sp_casos,sp_internacoes, uti_final)

    # calculate fases
    df = manipulation_sp.add_fases(df)

    # padronize names and column names
    # df = manipulation_sp.padronize_planosp_names(df)
            
        
        
        
    cols = ['datahora','nome_drs','Capacidade Hospitalar','uti_var','leitos_pc','Evolução da Pandemia','casos_var','internacoes_var','internacoes_14d_pc','obitos_var','obitos_14d_pc','Classif. Final']

    cols = ['datahora','nome_drs','Capacidade Hospitalar','uti_var','leitos_pc','Evolução da Pandemia','casos_var','internacoes_var','obitos_var','Classif. Final']



    rename_drs = {
        'Araraquara':'DRS 03 - Araraquara',
        'Araçatuba':'DRS 02 - Araçatuba',
        'Baixada Santista':'DRS 04 - Baixada Santista',
        'Barretos':'DRS 05 - Barretos',
        'Bauru':'DRS 06 - Bauru',
        'Campinas':'DRS 07 - Campinas',
        'Estado de São Paulo':'Estado de São Paulo',
        'Franca':'DRS 08 - Franca',
        'Marília':'DRS 09 - Marília',
        'Município de São Paulo':'DRS 01 - Município de São Paulo',
        'Piracicaba':'DRS 10 - Piracicaba',
        'Presidente Prudente':'DRS 11 - Presidente Prudente',
        'Registro':'DRS 12 - Registro',
        'Ribeirão Preto':'DRS 13 - Ribeirão Preto',
        'Sorocaba':'DRS 16 - Sorocaba',
        'São José do Rio Preto':'DRS 15 - São José do Rio Preto',
        'São João da Boa Vista':'DRS 14 - São João da Boa Vista',
        'Taubaté':'DRS 17 - Taubaté',
        'Estado de São Paulo':'00 - Estado de São Paulo'
    }

    df['nome_drs'] = df['nome_drs'].map(rename_drs)

    ddf = df.copy()
    
    
    cols_rename = {
        "Capacidade Hospitalar": "cap_hosp",
        "Evolução da Pandemia": "evolucao_pand",
        "Classif. Final": "classif_final",
        "nome_drs": "drs_name",
        'Data':'datahora'
    }


    ddf = df.rename(columns=cols_rename)
    mask = ddf['datahora']==max(ddf['datahora'])
    ddf['last_update'] = max(ddf['datahora'])
    ddf_last = ddf[mask].rename(columns={"drs_name":"DRS"})


        
    #upload to drive
    from scripts import io
    io.to_gbq(ddf,'plano_sp','covid','gabinete-sv', if_exists='replace')
    io.to_gbq(ddf_last,'plano_sp_last','covid','gabinete-sv', if_exists='replace')
        
        
        
    
    

def main():
    print('START')
    
    run_corona_mundo()
    print('World Data Done')
    
    # run_corona_br()
    # print('BR Data Done')

    run_coronaBR()
    print('BR Map Done')
    
    run_coronaVale()
    print('Vale Data Done')

    print(today)

if __name__ == "__main__":
    main()
