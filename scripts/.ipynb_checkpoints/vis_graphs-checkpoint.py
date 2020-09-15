import numpy as np
import pandas as pd

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline

import unicodedata

from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
date_time = datetime.today().strftime('%Y-%m-%d-%H-%M')

def normalize_cols(df):
    return df.str.normalize('NFKD').str.replace("$","").str.replace("(","").str.replace(")","").str.replace('-','').str.replace(' ','_').str.lower().str.replace('.','')


def remove_acentos(s):
    ss =  ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    
    return ss.lower().replace(' ','_')


def total_casos(df,mask_countrys, themes,escala='lin',var='cases',date=today, save=False):
    mask = df['new_{}'.format(var)]!=0
    df = df[mask]
    df['count'] = 1
    
    mask = df['confirmed'] > 100
    df = df[mask]
    df['count'] = 1

    since_first_day = df[['count','countrycode']].groupby(by = ['countrycode',]).cumsum()['count'].tolist()
    df['since_first_day'] = since_first_day
    
    dd = df[mask_countrys]
    
    dd = dd.sort_values(by=['countryname'], ascending=False)
    dd = dd.sort_values(by=['date'])
    
    data = []
            
    if escala == 'lin':
        tick = 'n'
        tipo = None
    elif escala=='log':
        tick = None
        tipo = 'log'
    
    
    if var == 'deaths':
        title = '<b>Evolução do Número de Mortes'
        var_col = 'deaths'
        var_save= 'mortes'
        y_name = "<b>MORTES CONFIRMADAS<b>"
        x_name = "<b>DIAS DESDE A PRIMEIRA MORTE<b>"
        
    if var== 'cases':
        title = '<b>Evolução do Número de Casos'
        var_col = 'confirmed'
        var_save= 'total'
        y_name = "<b>CASOS CONFIRMADOS<b>"
        x_name = "<b>DIAS DESDE O PRIMEIRO CASO<b>"
        
    if var== 'recovered':       
        title = '<b>Total de Recuperados Confirmados em {}</b>'.format(date)
        var_col = 'recovered'
        var_save= 'recuperados'
        y_name = "<b>RECUPERADOS CONFIRMADOS<b>"
        x_name = "<b>DIAS DESDE O PRIMEIRO CASO<b>"        
        
    
    countrys = list(dd['countrycode'].unique())
    countrys.sort(reverse=True)
    
    for geoid in countrys:

        mask = (dd['countrycode']==geoid)

        trace = go.Scatter(
        name=dd[mask]['countryname'].str.replace('_',' ').tolist()[0],
        x=dd[mask]['since_first_day'], 
        y=dd[mask][var_col],
    #     line=dict(color='#a14900', width=wid),
        line=dict(width=themes['data']['line_width']),
        mode='lines+markers',
        marker=dict(size=themes['data']['marker_size']),
        hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
        )
        data.append(trace)

    layout = get_layout(themes, title, x_name, y_name, tick, tipo)
    


    fig = go.Figure(data=data, layout=layout)

    
    if save==True:
        if escala == 'lin':
            plot(fig, filename="../images/multipleCountry/{}_lin.html".format(var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/multipleCountry/{}_lin.html".format(var_save), auto_open=False)
        elif escala=='log':
            plot(fig, filename="../images/multipleCountry/{}_log.html".format(var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/multipleCountry/{}_log.html".format(var_save),auto_open=False)
    else:
        pass

    return(fig)


def total_by_country(df,geoid, themes,escala='lin',var='cases', data=today, save=False):
    
    if geoid=='IT':
        mask = (df['countrycode']=='IT')
        dd = df[mask]


        mask = (dd['confirmed']>0)
        dd = dd[mask]

        mask = dd['date']>='2020-03-09'
        dd['lockdown'] = np.where(mask,1,0)

        mask = dd['date']>='2020-02-21'
        dd = dd[mask]
        
        pais = 'Itália'
        pais_save = 'italia'
        
    
    elif geoid=='CN':
        
        mask = (df['confirmed']>0)
        dd = df[mask]
        
        mask = (df['countrycode']=='CN')
        dd = df[mask]

        mask = dd['date']>='2020-01-24'
        dd['lockdown'] = np.where(mask,1,0)
        
        pais='China'
        pais_save = 'china'

    
    else:
        
        mask = (df['countrycode']==geoid)
        dd = df[mask]
        
        mask = (dd['confirmed']>0)
        dd = dd[mask]
        
        dd['lockdown']=0
        pais = dd['countryname'].tolist()[0]
        pais_save = pais
    
    
    
    if escala == 'lin':
        tick = 'n'
        tipo = None
    elif escala=='log':
        tick = None
        tipo = 'log'
    
    
    if var == 'deaths':
        title = '<b>{} - Evolução do número de Mortes'.format(pais)
        var_col = 'deaths'
        var_save= 'mortes'
        barra1 = "Mortes Diarias"
        barra2 = "Mortes Diarias no LockDown"
        y_name = "<b>Mortes Confirmadas<b>"
        nome_final = "Total de Mortes"
        
    if var== 'cases':
        title = '<b>{} - Evolução do número de Casos'.format(pais)
        var_col = 'confirmed'
        var_save= 'total'
        barra1 = "Casos Diarios"
        barra2 = "Casos Diarios no LockDown"
        y_name = "<b>Casos Confirmados<b>"
        nome_final = "Total de Casos"
        
        
    if var== 'recovered':
        title = '<b>{} - Total de Recuperados Confirmados em {}</b>'.format(pais,data)
        var_col = 'recovered'
        var_save= 'recuperados'
        barra1 = "Recuperados Diarios"
        barra2 = "Recuperados Diarios no LockDown"
        y_name = "<b>Recuperados Confirmados<b>"
        nome_final = "Total de Recuperados"
        
    if save ==True:
        largura = None
    else:
        largura = 1600

    trace1 = go.Scatter(
    name=nome_final,
    x=dd['date'], 
    y=dd[var_col],
    line=dict(width=themes['data']['line_width'], color='#3b5bff'),
    mode='lines+markers',
    marker=dict(size=themes['data']['marker_size']),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )


    mask = dd['lockdown']==0


    trace2 = go.Bar(
    name=barra1,
    x=dd[mask]['date'], 
    y=dd[mask]['new_{}'.format(var)],

    marker=dict(color='#1d8179',),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )

    mask = dd['lockdown']==1

    trace3 = go.Bar(
    name=barra2,
    x=dd[mask]['date'], 
    y=dd[mask]['new_{}'.format(var)],

    marker=dict(color='#fa7609',),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )




    data = [trace3, trace2, trace1]

    x_name = '<b>Data<b>'
    layout = get_layout(themes, title, x_name, y_name)

    fig = go.Figure(data=data, layout=layout)
    
    
    pais_save = pais_save.lower().replace(' ','_')
    
    
    if save==True:
        if escala == 'lin':
            plot(fig, filename="../images/singleCountry/{}_lin_{}.html".format(pais_save,var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/singleCountry/{}_{}_lin.html".format(pais_save,var_save), auto_open=False)
        elif escala=='log':
            plot(fig, filename="../images/singleCountry/{}_log_{}.html".format(pais_save,var_save), auto_open=False)
            plot(fig, filename="../../sample_pages/images/covid19/singleCountry/{}_{}_log.html".format(pais_save,var_save),auto_open=False)
    else:
        pass
    
    return(fig)


def bar_compare(br_it, pais='BR',pais_name='Brasil',
                pais_comp='IT',pais_comp_name='Itália',
                color='#007482',color_comp='#F29120',
                save=False,
                col='confirmed',
                themes=None):
    
    mask = (br_it['countrycode'] == pais)

    trace2 = go.Bar(
    name=pais_name,
    x=br_it[mask]['since_first_day'], 
    y=br_it[mask][col],

    marker=dict(color=color,),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )


    mask = (br_it['countrycode'] == pais_comp)

    trace3 = go.Bar(
    name=pais_comp_name,
    x=br_it[mask]['since_first_day'], 
    y=br_it[mask][col],

    marker=dict(color=color_comp,),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )


    data = [trace2,trace3]
    #     data = [trace1] 

    title  = '<b>Número Total de Confirmados (A partir do Caso 100) - {} vs {}<b>'.format(pais_name,pais_comp_name)
    x_name = '<b>Dias desde o Primeiro Caso<b>'
    y_name = '<b>Número de Confirmados<b>'
    tick   =    tickformat =themes['axis_legend']['tickformat']['y']

    layout = get_layout(themes, title, x_name, y_name, tick=tick)



    fig = go.Figure(data=data, layout=layout)
    
        
    pais_save = [pais_name,pais_comp_name]
    pais_save.sort()
    pais_save = [remove_acentos(p) for p in pais_save]
    
    if save==True:
        plot(fig, filename="../images/comparacao/comparacao_{}_vs_{}.html".format(pais_save[0],pais_save[1]), auto_open=False)
        plot(fig, filename="../../sample_pages/images/covid19/comparacao/comparacao_{}_vs_{}.html".format(pais_save[0],pais_save[1]), auto_open=False)


    else:
        pass
    
    return(fig)


def brasil_vis(dd,
               var_col,
               in_cities, 
               today,
               themes,
               save=False):

    if var_col == 'deaths':
        x_name  = '<b>DATA<b>'
        y_name  = '<b>MOTES CONFIRMADAS<b>'
        title   = '<b>EVOLUÇÃO DO NÚMERO DE MORTES<b>'
    
    elif var_col == 'confirmed':
        x_name  = '<b>DATA<b>'
        y_name  = '<b>CASOS CONFIRMADOS<b>'
        title   = '<b>EVOLUÇÃO DO NUMERO DE CASOS'


    # in_cities = ['BRASIL','SP', 'RJ']
    cities = dd['city'].unique()
    drop_cities = [city for city in cities if city not in in_cities]
    drop_cities.sort()
    # cities =  in_cities + drop_cities

    cities = in_cities

    colors =  themes['soft_colors']
    
    factor = int(np.ceil(len(cities)/len(colors)))    
    
    colors = factor * colors
    
    colors = themes['colors'] + colors
    
    
    data = []
    i=0
    for city in cities:

        if city in in_cities:
            just_legend = None
        else:
            just_legend = 'legendonly'
        
        mask = (dd['city']==city)

        trace = go.Scatter(
        name=city,
        x=dd[mask]['date'], 
        y=dd[mask][var_col],
        line=dict(color=colors[i], width=themes['data']['line_width']),
        # line=dict(width=wid),
        mode='lines+markers',
        marker=dict(size=themes['data']['marker_size']),
        hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size'])),
        visible = just_legend,
        )
        data.append(trace)
        i+=1

    
    layout = get_layout(themes, title, x_name, y_name)

    fig = go.Figure(data=data, layout=layout)


    if save==True:
        plot(fig, filename="../images/brasil/brasil_por_estado_{}.html".format(var_col), auto_open=False)
        plot(fig, filename="../../sample_pages/images/covid19/brasil/brasil_por_estado_{}.html".format(var_col), auto_open=False)
    else:
        pass

    return(fig)


def total_by_country_dash(df,geoid, themes, data=today, save=False):
    mask = (df['countrycode']==geoid)

    dd = df[mask]
    mask = (dd['confirmed']>0)
    dd = dd[mask]
    pais = dd['countryname'].tolist()[0]

    # if escala == 'lin':
    #     tick = 'n'
    #     tipo = None
    # elif escala=='log':
    #     tick = None
    #     tipo = 'log'
    

    trace2 = go.Bar(
    name='Casos Confirmados',
    x=dd[mask]['date'], 
    y=dd[mask]['new_{}'.format('cases')],

    marker=dict(color='#1d8179',),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )


    trace3 = go.Bar(
    name='Mortes Confirmadas',
    x=dd[mask]['date'], 
    y=dd[mask]['new_{}'.format('deaths')],

    marker=dict(color='#fa7609',),
    hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size']))   
    )




    data = [trace2,trace3]

    title = "<b>Evolução do Número Diario de Casos e Mortes<b>"
    x_name = '<b>Data<b>'
    y_name = "<b>Número de Individuos<b>"

    layout = get_layout(themes, title, x_name, y_name)

    fig = go.Figure(data=data, layout=layout)
    
    return(fig)

def get_layout(themes, title, x_name, y_name, tick=None, tipo=None):
    
    layout = go.Layout(
                
        barmode=themes['barmode'],
    
        title=dict(
            text=title,
            x=0.5,
    #         y=0.9,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=themes['title']['size'],
                color=themes['title']['color']
            )
        ),

        xaxis_title=x_name,
        
        xaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
        gridcolor=themes['axis_legend']['gridcolor'],
        zerolinecolor=themes['axis_legend']['gridcolor'],
        # linecolor=themes['axis_legend']['gridcolor'],
        # linewidth=2,
        # mirror=True,
        tickformat =themes['axis_legend']['tickformat']['x'],
        type=themes['axis_legend']['type']['x'],

        ),
        
        
        yaxis_title=y_name,
        
        yaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
            gridcolor=themes['axis_legend']['gridcolor'],
            zerolinecolor=themes['axis_legend']['gridcolor'],
            # linecolor=themes['axis_legend']['gridcolor'],
            # linewidth=2,
            tickformat=tick,
            type=tipo,
        ),
        
        
        font=dict(
            size=themes['axis_tilte']['size'],
            color=themes['axis_tilte']['color']
        ),
        

        legend=go.layout.Legend(
            x=themes['legend']['position']['x'],
            y=themes['legend']['position']['y'],
            traceorder="normal",
            orientation='v',
            font=dict(
                family=themes['legend']['family'],
                size=themes['legend']['size'],
                color=themes['legend']['color']
            ),
            bgcolor=themes['legend']['bgcolor'] ,
            bordercolor=themes['legend']['bordercolor'],
            borderwidth=themes['legend']['borderwidth']
        ),


        height = themes['altura'],
        width = themes['largura'],
        

        paper_bgcolor=themes['paper_bgcolor'],
        plot_bgcolor=themes['plot_bgcolor'],
        
        annotations =[dict(
            showarrow=False,
            text = f"<b>{themes['source']['text']}<b>",
            
            x = themes['source']['position']['x'],
            y = themes['source']['position']['y'],
            

            
            xref="paper",
            yref="paper",

            align="left",
            
            # xanchor='right',
            xshift=0, yshift=0,
            
            font=dict(
                family=themes['source']['family'],
                size=themes['source']['size'],
                color=themes['source']['color']
                ),
        )]
        
    )
    
    
    return layout




