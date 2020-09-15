from bs4 import BeautifulSoup
from requests import get

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math 
import os

from scripts.vis_graphs import normalize_cols






# Function for remove comma within numbers
def removeCommas(string): 
    string = string.replace(',','')
    return string 

def load_data():
    # Test if we can scrap info from worldometers
    # The communication with website is ok if the response is 200
    headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    worldometers = "https://www.worldometers.info/coronavirus/#countries"
    response = get(worldometers, headers=headers)

    # Scrap all content from the website
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # After inspect the website content, data are stored inside tag 'tbody' and table header is 'thead'
    table_contents = html_soup.find_all('tbody')
    table_header = html_soup.find_all('thead')

    # Header for the table
    header = []
    for head_title in table_header[0].find_all('th'):    
        header.append(str(head_title.contents))

    # Save value into columns
    CountryName = []
    TotalCases = []
    NewCases = []
    TotalDeaths = []
    NewDeaths = []
    TotalRecovered = []
    ActiveCases = []
    SeriousCritical = []

    for row in table_contents[0].find_all('tr'):
        cells = row.find_all('td')

        if len(cells[1].find_all('a')) >= 1:
            CountryName.append(cells[1].find_all('a')[0].contents[0])
        elif len(cells[1].find_all('span')) >= 1:
            CountryName.append(cells[1].find_all('span')[0].contents[0])   
        else:
            CountryName.append(cells[1].contents[0])
        
        if len(cells[2].contents) >=1:
            TotalCases.append(cells[2].contents[0])
        else:
            TotalCases.append(0)
        
        if len(cells[3].contents) >= 1:
            NewCases.append(cells[3].contents[0])
        else:
            NewCases.append(0)
            
        
        if len(cells[4].contents) >= 1:
            TotalDeaths.append(cells[4].contents[0])
        else:
            TotalDeaths.append(0)

        
        if len(cells[5].contents) >= 1:
            NewDeaths.append(cells[5].contents[0])
        else:
            NewDeaths.append(0)
        
        if len(cells[6].contents) >= 1:
            TotalRecovered.append(cells[6].contents[0])
        else:
            TotalRecovered.append(0)
            
        if len(cells[7].contents) >= 1:
            ActiveCases.append(cells[7].contents[0])
        else:
            ActiveCases.append(0)
        
        if len(cells[8].contents) >= 1:
            SeriousCritical.append(cells[8].contents[0])
        else:
            SeriousCritical.append(0)
            
            
    CaseTable = pd.DataFrame({header[1]: CountryName,
                            header[2]: TotalCases,
                            header[3]: NewCases,
                            header[4]: TotalDeaths,
                            header[5]: NewDeaths,                          
                            header[6]: TotalRecovered,
                            header[7]: ActiveCases,
                            header[8]: SeriousCritical,
                            })  

    caseTableSimple = CaseTable[[CaseTable.columns[0], CaseTable.columns[1], CaseTable.columns[3], CaseTable.columns[5]]]
    caseTableSimple.columns = ['Country/Region', 'Confirmed', 'Deaths', 'Recovered']
    # Set data type as string first for manuipulation
    caseTableSimple = caseTableSimple.astype({'Country/Region':str,'Confirmed':str,'Deaths':str, 'Recovered':str})
    # Remove the last row of total number (changed on 20200310, worldmeter moved this row as next tbody)
    #caseTableSimple = caseTableSimple.iloc[:-1,:]
    # Remove lead and tail space for each element
    caseTableSimple = caseTableSimple.apply(lambda x: x.str.strip())
    # Remove comma for each element
    caseTableSimple = caseTableSimple.applymap(removeCommas)
    # Replace empty str with zero. This include row of 'Diamond Princess' (its name is empty)
    caseTableSimple = caseTableSimple.replace('', '0')
    # After string manipulation, convert data type as correct type
    caseTableSimple = caseTableSimple.astype({'Country/Region':'str',
                                            'Confirmed':'int',
                                            'Deaths':'int',
                                            # 'Recovered':'int',                                          
                                            })
    
    caseTableSimple['Recovered'] = pd.to_numeric(caseTableSimple['Recovered'], errors='coerce')
    # Data for these countries come from other source
    removeRegion = []
    for i in removeRegion:
        caseTableSimple.drop(caseTableSimple[caseTableSimple['Country/Region'] == i].index, axis=0, inplace=True)

    # Change Country name the same as my old data 
    if 'S. Korea' in list(caseTableSimple['Country/Region']):
        caseTableSimple = caseTableSimple.replace('S. Korea', 'South Korea')

    # Add column 'Province/State' with empty value
    caseTableSimple['Province/State'] =''

    # In my old data, 'Diamond Princess' is represented by 'Yokohama' in the column of 'Province/State'
    if 'Diamond Princess' in list(caseTableSimple['Country/Region']):
        caseTableSimple.at[caseTableSimple.loc[caseTableSimple['Country/Region'] == 'Diamond Princess',].index, 'Province/State'] = 'Yokohama'
        caseTableSimple['Country/Region'].replace({'Diamond Princess':'Japan'}, inplace=True)

    # In my old data, 'Belgium' has 'Brussels' in the column of 'Province/State'
    if 'Belgium' in list(caseTableSimple['Country/Region']):
        caseTableSimple.at[caseTableSimple.loc[caseTableSimple['Country/Region'] == 'Belgium',].index, 'Province/State'] = 'Brussels'

    # In my old data, I used 'Macau' not 'Macao'
    if 'Macao' in list(caseTableSimple['Country/Region']):
        caseTableSimple.at[caseTableSimple.loc[caseTableSimple['Country/Region'] == 'Macao',].index, 'Province/State'] = 'Macau'
        caseTableSimple['Country/Region'].replace({'Macao':'Macau'}, inplace=True)

    # In my old data, 'Hong Kong' has 'Hong Kong' in the column of 'Province/State'
    if 'Hong Kong' in list(caseTableSimple['Country/Region']):
        caseTableSimple.at[caseTableSimple.loc[caseTableSimple['Country/Region'] == 'Hong Kong',].index, 'Province/State'] = 'Hong Kong'

    # In my old data, 'Taiwan' has 'Taiwan' in the column of 'Province/State'
    if 'Taiwan' in list(caseTableSimple['Country/Region']):
        caseTableSimple.at[caseTableSimple.loc[caseTableSimple['Country/Region'] == 'Taiwan',].index, 'Province/State'] = 'Taiwan'

    # In my old data, I used 'United Arab Emirates' not 'UAE'
    if 'UAE' in list(caseTableSimple['Country/Region']):
        caseTableSimple['Country/Region'].replace({'UAE':'United Arab Emirates'}, inplace=True)

    if 'Réunion' in list(caseTableSimple['Country/Region']):
        caseTableSimple['Country/Region'].replace({'Réunion':'Reunion'}, inplace=True)
        
    if 'Curaçao' in list(caseTableSimple['Country/Region']):
        caseTableSimple['Country/Region'].replace({'Curaçao':'Curacao'}, inplace=True)

    # In my old data I used US time as Last Update time
    currentTime = datetime.now()
    lastUpdateTime = currentTime.strftime('%m/%d/%Y %H:%M')

    # Remove the first number (This only works for month number less than 10)
    lastUpdateTime[1:]
    caseTableSimple['Last Update'] = lastUpdateTime[1:]

    # Reorder list as all old data
    columnList = caseTableSimple.columns.tolist()
    columnList =[columnList[i] for i in [4, 0, 5, 1, 2, 3]]
    caseTableSimple = caseTableSimple[columnList]







    finalTable = caseTableSimple.copy()
    # finalTable



    finalTable['Confirmed'] = finalTable['Confirmed'].fillna(0).astype(int)
    finalTable['Deaths'] = finalTable['Deaths'].fillna(0).astype(int)
    finalTable['Recovered'] = finalTable['Recovered'].fillna(0).astype(int)

    mask = ((finalTable['Country/Region'].notnull()) | (finalTable['Province/State'].notnull()) | (finalTable['Last Update'].notnull()) |
            (finalTable['Recovered'].notnull()) | (finalTable['Deaths'].notnull()) | (finalTable['Confirmed']))
    finalTable = finalTable[mask]

    finalTable['Country/Region'] = finalTable['Country/Region'].replace('USA','US')








    timeStampe = currentTime.strftime('%m_%d_%Y_%H_%M')

    finalTable.to_csv('../data/web_data/{}_webData.csv'.format(timeStampe), index=False)
    finalTable.to_csv('../data/web_data/last_capure.csv', index=False)

    date_time = currentTime.strftime('%Y-%m-%d-%H-%M')



    ########### CONSOLIDADE DATA ##############


    new_data = pd.read_csv('../data/web_data/last_capure.csv')
    new_data = new_data.groupby(by=['Country/Region','Last Update'], as_index=False).sum()

    date_day = timeStampe = currentTime.strftime('%Y-%m-%d')

    new_data['date'] = date_day

    new_data = new_data.rename(columns={'Country/Region':'countryname','Last Update':'Date_last_updated_AEDT'})


    cols = ['Date_last_updated_AEDT', 'date', 'countryname', 'Confirmed', 'Deaths', 'Recovered']
    new_data = new_data[cols]



    last_data = pd.read_csv('../data/cumulative_data/covid_last.csv')
    mask = last_data['date']!=date_day
    last_data = last_data[mask]

    final_data = pd.concat([new_data,last_data],axis=0)

    
    final_data['Date_last_updated_AEDT'] = pd.to_datetime(final_data['Date_last_updated_AEDT'])
    
    final_data.to_csv('../data/cumulative_data/{}.csv'.format(date_time), index=False)
    final_data.to_csv('../data/cumulative_data/covid_last.csv'.format(date_time), index=False)



    ### PADRONIZA DOS DADOS    
    codes = pd.read_csv('../data/country_codes.csv')
    # codes = codes[['CountryCode','CountryName']].drop_duplicates()
    # codes.columns = normalize(codes.columns)


    df = final_data.copy()
    df.columns = normalize_cols(df.columns)

    df = pd.merge(df,codes,on='countryname', how='left')
    country_rename = {'US':'United States', 'UK':'United Kingdom', "Brazil":"Brasil"}
    df['countryname'] = df['countryname'].replace(country_rename)


    df_pop = pd.read_csv('../data/world_population.csv')

    df = pd.merge(df,df_pop,on='countryname', how='left')
    df = df[df['population'].notnull()]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return new_data, df