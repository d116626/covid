import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
date_time = datetime.today().strftime('%Y-%m-%d-%H-%M')

import vis_layout
from manipulation import normalize_cols, remove_acentos





def all_countrys(dd,var,scale,theme,save=False):
    mask = ((dd[f'{var}']!=0) & (dd[f'{var}'] > theme['vars'][var]['since_var']))
    dd = dd[mask]
    dd['count'] = 1

    since_first_day = dd[['count','countrycode']].groupby(by = ['countrycode',]).cumsum()['count'].tolist()
    dd['since_first_day'] = since_first_day

    dd = dd.sort_values(by=['countryname'], ascending=False)
    dd = dd.sort_values(by=['date'])

    countrys = list(dd['countrycode'].unique())
    countrys.sort(reverse=True)
    

    data = []
    for geoid in countrys:
        mask = (dd['countrycode']==geoid)
        dc = dd[mask]
        dc[var] = dc[var].rolling(theme['vars'][var]['roling_window']).mean()
        mask = (dc[var].notnull())
        dc = dc[mask]
        trace = go.Scatter(
            name=dc['countryname'].str.replace('_',' ').tolist()[0],
            x=dc['since_first_day'], 
            y=dc[var],
        #     line=dict(color='#a14900', width=wid),
            line=dict(width=theme['data']['line_width']),
            mode='lines+markers',
            marker=dict(size=theme['data']['marker_size']),
            hoverlabel=dict(namelength=-1, font=dict(size=theme['data']['hoverlabel_size']))   
            )
        data.append(trace)

    layout = vis_layout.get_layout_new(theme, var, scale)
    
    
    fig = go.Figure(data=data, layout=layout)
    
    
    return fig


def unique_country(dd,themes):
    
    data=[]
    
    for var in themes['vars'].keys():
        trace = go.Bar(
            name=themes['vars'][var]['nome'],
            x=dd['date'], 
            y=dd[var],
            marker=dict(color=themes['vars'][var]['color'],),
            hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
            )
        data.append(trace)
        
    layout = vis_layout.get_layout_bar(themes)
    
    fig = go.Figure(data=data, layout=layout)
    
    return fig





def brasil_vis_cum(dd, var,scale ,themes):
    dd = dd[dd['confirmed']>0]
    
    
    if themes['vars'][var]['in_cities'][0] == 'all':
        in_cities = dd['state'].unique()
    else:
        in_cities=themes['vars'][var]['in_cities']
    
    colors =  themes['data']['colors']
    factor = int(np.ceil(len(in_cities)/len(colors)))    
    colors = factor * colors
    
    data = []
    i=0
    
    for city in in_cities:
        mask =dd['city']==city
        dc = dd[mask]
        
        dc[var] = dc[var].rolling(themes['vars'][var]['roling_window']).mean()
        mask = (dc[var].notnull())
        dc = dc[mask]
        
        
        trace = go.Scatter(
            name=city,
            x=dc['date'], 
            y=dc[var],
            line=dict(color=colors[i], width=themes['data']['line_width']),
            mode='lines+markers',
            marker=dict(size=themes['data']['marker_size']),
            hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size'])),
        )
        data.append(trace)
        i+=1

    
    layout = vis_layout.get_layout_new(themes,var,scale)

    fig = go.Figure(data=data, layout=layout)
    
    return fig


    return(fig)





