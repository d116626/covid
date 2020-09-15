import numpy as np
import pandas as pd
import geopandas as gpd
import unicodedata
from paths import *

import warnings
warnings.filterwarnings('ignore')

from scripts import io
from scripts import manipulation
from scripts import vis_html
from scripts import vis_maps

import yaml

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

def _generate_and_upload_br_map(final, estados, map_config):
    #generate map
    cols = ['Município','Estado','Confirmados', 'Óbitos', 'Data do Boletim']

    mymap =  vis_maps.get_map(final,'Confirmados', cols, estados)
    
    mymap.save(f'{map_config["path_save"]}{map_config["save_name"]}')

    print('Savin br map..')
    io.to_storage(bucket=map_config['bucket'],
              bucket_folder=map_config['bucket_folder'],
              file_name=map_config['save_name'],
              path_to_file=f'{map_config["path_save"]}{map_config["save_name"]}')

    os.remove(f'{map_config["path_save"]}{map_config["save_name"]}')

def _generate_and_upload_vale_map(vale, estados, map_config):
    #generate map
    cols = ['Município','Confirmados','Confirmados Internados','Óbitos','Óbitos Suspeitos','Suspeitos','Suspeitos Internados','Recuperados','Descartados','Data do Boletim']
    
    print('Generate and save vale map..')
    mymap =  vis_maps.get_map_vale(vale,'Confirmados', cols, estados)
    mymap.save(f'{map_config["path_save"]}{map_config["save_name"]}')

    print('Upload vale map..')
    io.to_storage(bucket=map_config['bucket'],
              bucket_folder=map_config['bucket_folder'],
              file_name=map_config['save_name'],
              path_to_file=f'{map_config["path_save"]}{map_config["save_name"]}')
    os.remove(f'{map_config["path_save"]}{map_config["save_name"]}')


def main():
    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)
    themes = yaml.load(open('../themes/custom_colorscales.yaml', 'r'), Loader=yaml.FullLoader)

    print('Loading data')
    ### br.IO TABLE ###
    brio, brio_raw = io.load_brasilIO()
    print("Br.IO table, Done!")
    
    #### MS TABLE ###
    io.update_ms_data()
    df = pd.read_csv("../data/ministerio_da_saude/last_data_ms_covid19.csv")
    df_states = manipulation.manipule_mytable(df,config['ms_table'])
    print("States table, Done!")
    
    #### VALE TABLE ###
    vale = io.read_sheets('covid19_vale_do_paraiba_e_litoral_norte').replace('',0)
    print("Vale table, Done!")


    print('\nsaving html')
    ### update numbers in the html and upload the file to storage
    vis_html.create_cards(df_states,vale,config['embed_html'])
    
    
    print('cumulative graph')
    ### generate cumulative data and upload to storage
    io.br_cumulative_generate_upload(df_states,config['br_cumulative'],themes)
    
    print('daily graph')
    ### generate daily data and upload to storage
    io.br_daily_genarete_upload(df_states,config['br_daily'],themes)


    ### LOAD DATA FOR BRASIL MAPS    
    print('\nStart Br Map')
    #minicipales data
    municipios = pd.read_csv('../data/br_municipios_ibge.csv', dtype={'geocodigo':str})
    #load shape files;
    ufs = gpd.read_file('../../mapas_brasil/estados-ibge/BRUFE250GC_SIR.shp')
    maps = gpd.read_file('../../mapas_brasil/municipios-ibge/brasil-municipios.shp')


    ### GET THE TABLE TO GENERATE THE MAP    
    final, estados = manipulation.manipulate_for_br_maps(brio, municipios, maps, df_states, ufs)

    ### generate and upload the map
    print('skip br maps')
    # _generate_and_upload_br_map(final, estados, config['br_map'])

    print('\nStart Vale Map')
    ### LOAD DATA FOR BRASIL MAPS    
    df = manipulation.manipulate_vale_data(vale)

    #load shape files
    municipios_sp = gpd.read_file('../../brasil_geodata/maps/sp_municipios.json')
    ufs = gpd.read_file('../../mapas_brasil/estados-ibge/BRUFE250GC_SIR.shp')
    
    ## Manipulate data for generate map
    config = yaml.load(open('../configs/config.yaml', 'r'), Loader=yaml.FullLoader)

    vale, estados = manipulation.manipulate_for_vale_maps(df, municipios_sp, estados)

    _generate_and_upload_vale_map(vale, estados, config['vale_map'])

    print("<--Finish--> ")

if __name__ == "__main__":
    main()