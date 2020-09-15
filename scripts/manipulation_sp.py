import pandas as pd
import numpy as np



def padronize_casos(sp_full):
    sp_full['nome_drs'] = np.where(sp_full['nome_munic']=='São Paulo','Município de São Paulo',sp_full['nome_drs'])

    cols = ['datahora','nome_munic','casos','casos_novos','obitos','obitos_novos','nome_drs']
    sp = sp_full[cols][sp_full['nome_drs'].notnull()]

    sp = sp.groupby(by=['nome_drs','datahora'], as_index=False).sum().sort_values(by=['nome_drs','datahora'])

    estado = sp.groupby(by=['datahora'], as_index=False).sum().sort_values(by=['datahora'])
    estado['nome_drs'] = 'Estado de São Paulo'
    estado = estado[sp.columns]

    sp = pd.concat([sp,estado],axis=0)
    sp['casos'] = sp['casos'].astype(int)
    sp['obitos'] = sp['obitos'].astype(int)


    dd_final_all = pd.DataFrame()

    for drs in sp['nome_drs'].unique():

        tbt = sp[sp['nome_drs']==drs]

        tbt['casos_shift'] = tbt['casos'].shift(7)
        tbt['obitos_shift'] = tbt['obitos'].shift(7)
        tbt['obitos_shift_14'] = tbt['obitos'].shift(14)
        tbt['casos_shift_14'] = tbt['casos'].shift(14)


        tbt['casos_7'] = tbt['casos'] - tbt['casos_shift']
        tbt['obitos_7'] = tbt['obitos'] - tbt['obitos_shift']
        tbt['obitos_14d'] = tbt['obitos'] - tbt['obitos_shift_14']
        tbt['casos_14d'] = tbt['casos'] - tbt['casos_shift_14']


        tbt['casos_7_shift'] = tbt['casos_7'].shift(7)
        tbt['obitos_7_shift'] = tbt['obitos_7'].shift(7)

        tbt['casos_var'] = tbt['casos_7']/tbt['casos_7_shift']
        tbt['obitos_var'] = tbt['obitos_7']/tbt['obitos_7_shift']


            
            
        dd = tbt[['datahora','nome_drs','casos','casos_novos','casos_var','obitos','obitos_novos','obitos_var','obitos_14d','casos_14d']]

        dd_final_all = pd.concat([dd_final_all,dd], axis=0)
    
    return sp_full, dd_final_all


def padronize_internacoes(sp_cv):
    sp_cv['internacoes_var'] = sp_cv['internacoes_7d']/sp_cv['internacoes_7d_l']
    sp_cv['internacoes_14d'] = sp_cv['internacoes_7d'].astype(int) + sp_cv['internacoes_7d_l'].astype(int)
    cols = ['datahora','nome_drs','leitos_pc','internacoes_var','internacoes_14d','internacoes_7d','pop']

    uti_all = sp_cv[cols]

    uti_all['nome_drs'] = uti_all['nome_drs'].apply(lambda x: x[7:] if x[:3]=='DRS' else x).str.strip()
    # uti_all['leitos_pc'] = uti_all['leitos_pc'].astype(str).str.replace(',','.').astype(float)


    df_final = uti_all[cols].copy()
    
    return sp_cv, df_final


def padronize_planosp(sp_casos,sp_internacoes, uti_final):
    
    df = pd.merge(sp_casos,sp_internacoes,on=['datahora','nome_drs'],how='outer').merge(uti_final,on=['datahora','nome_drs'],how='inner')
    mask = df['nome_drs'].str.startswith('Grande')
    df = df[np.logical_not(mask)]

    df = df[df['pop'].notnull()]

    df['leitos_pc'] = df['leitos_pc'].str.replace(',','.')

    df['pop'] = df['pop'].astype(int)

    df['internacoes_14d_pc'] = (df['internacoes_14d'] * 10**5 )/df['pop']
    df['obitos_14d_pc'] = (df['obitos_14d']  * 10**5 )/df['pop']

    return df

def uti_fase(x):
    if x>=80:
        fase=1
    elif (x <80) & (x>=75):
        fase=2
    else:
        fase = 4
    return fase

def leitos_fase(x):
    if x<=3:
        fase=1
    elif (x >3) & (x<=5):
        fase=2
    else:
        fase = 4
    return fase


def casos_fase(x):
    if x>=2:
        fase=1
    elif (x <2) & (x>=1):
        fase=3
    else:
        fase = 4
    return fase

def internacoes_fase(x,y):
    if x>=1.5:
        fase=1
    elif (x <1.5) & (x>=1):
        fase=2
    elif (x <1) & (y>=40):
        fase=3
    elif (x <1) & (y<40):
        fase=4
    return fase

def obitos_fase(x,y):
    if x>=2:
        fase=1
    elif (x <2) & (x>=1):
        fase=2
    elif (x <1) & (y>=5):
        fase=3
    elif (x <1) & (y<5):
        fase=4
    return fase

def add_fases(df):
    O = df['uti_var'].apply(lambda x: uti_fase(x))

    L = df['leitos_pc'].str.replace(',','.').astype(float).apply(lambda x: leitos_fase(x))


    c1 = (O*4 + L)/5

    df['Capacidade Hospitalar'] = c1
    # df['Capacidade Hospitalar'] = c1.astype(int)





    NC = df['casos_var'].apply(lambda x: casos_fase(x))

    NI = df.apply(lambda x: internacoes_fase(x['internacoes_var'],x['internacoes_14d_pc']), axis=1)

    NO = df.apply(lambda x: obitos_fase(x['obitos_var'],x['obitos_14d_pc']), axis=1)

    c2 = (NC + 3*NI + NO)/5

    df['Evolução da Pandemia'] = c2

    df['casos_var'] = df['casos_var'].round(2).astype(str)
    df['obitos_var'] = df['obitos_var'].round(2).astype(str)
    df['internacoes_var'] = df['internacoes_var'].round(2).astype(str)
    df['uti_var'] = df['uti_var'].round(2).astype(str)

    df['Classif. Final'] = df[['Capacidade Hospitalar','Evolução da Pandemia']].min(axis=1)

    # df['Classif. Final'] = df['Classif. Final'].astype(int).astype(str)
    # df['Evolução da Pandemia'] = df['Evolução da Pandemia'].astype(int).astype(str)
    # df['Capacidade Hospitalar'] = df['Capacidade Hospitalar'].astype(int).astype(str)

    df['Classif. Final'] = df['Classif. Final'].round(1).astype(str)
    df['Evolução da Pandemia'] = df['Evolução da Pandemia'].round(1).astype(str)
    df['Capacidade Hospitalar'] = df['Capacidade Hospitalar'].round(1).astype(str)

    df['internacoes_14d_pc'] = df['internacoes_14d_pc'].round(1).astype(str)
    df['obitos_14d_pc'] = df['obitos_14d_pc'].round(1).astype(str)
    
    return df





def add_fases_only_evolution(df):

    NC = df['casos_var'].apply(lambda x: casos_fase(x))

    NI = df.apply(lambda x: internacoes_fase(x['internacoes_var'],x['internacoes_14d_pc']), axis=1)

    NO = df.apply(lambda x: obitos_fase(x['obitos_var'],x['obitos_14d_pc']), axis=1)

    c2 = (NC + 3*NI + NO)/5

    df['Evolução da Pandemia'] = c2

    df['casos_var'] = df['casos_var'].round(2).astype(str)
    df['obitos_var'] = df['obitos_var'].round(2).astype(str)
    df['internacoes_var'] = df['internacoes_var'].round(2).astype(str)


    # df['Classif. Final'] = df['Classif. Final'].astype(int).astype(str)
    # df['Evolução da Pandemia'] = df['Evolução da Pandemia'].astype(int).astype(str)
    # df['Capacidade Hospitalar'] = df['Capacidade Hospitalar'].astype(int).astype(str)

    df['Evolução da Pandemia'] = df['Evolução da Pandemia'].round(1).astype(str)

    df['internacoes_14d_pc'] = df['internacoes_14d_pc'].round(1).astype(str)
    df['obitos_14d_pc'] = df['obitos_14d_pc'].round(1).astype(str)
    
    
    
    cols = ['datahora','nome_drs','Evolução da Pandemia','casos_var','internacoes_var','obitos_var']



    cols_rename ={
        'datahora':'Data',
        'nome_drs':'DRS',
        'casos_var':'Variação de casos',
        'obitos_var':'Variação de óbitos',
        'leitos_pc':'Leitos COVID/100 mil hab',
        'internacoes_var':'Variação internações',
        'internacoes_14d_pc':'Internações / 100 mil habitantes nos ultimos 14 dias',
        'uti_var':'Ocupação leitos UTI COVID',
        'obitos_14d_pc':'Óbitos / 100 mil habitantes nos ultimos 14 dias'

    }




    df = df[cols].rename(columns=cols_rename).sort_values(by='DRS')
        
    return df






def padronize_planosp_names(df):
    
    cols = ['datahora','nome_drs','Capacidade Hospitalar','uti_var','leitos_pc','Evolução da Pandemia','casos_var','internacoes_var','internacoes_14d_pc','obitos_var','obitos_14d_pc']

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

    # df = pd.concat([df.tail(1),df.head(17)],axis=0).reset_index(drop=True)
    cols_rename ={
        'datahora':'Data',
        'nome_drs':'DRS',
        'casos_var':'Variação de casos',
        'obitos_var':'Variação de óbitos',
        'leitos_pc':'Leitos COVID/100 mil hab',
        'internacoes_var':'Variação internações',
        'internacoes_14d_pc':'Internações / 100 mil habitantes nos ultimos 14 dias',
        'uti_var':'Ocupação leitos UTI COVID',
        'obitos_14d_pc':'Óbitos / 100 mil habitantes nos ultimos 14 dias'

    }




    df = df[cols].rename(columns=cols_rename).sort_values(by='DRS')
    
    return df


def cases_color(val):
    
    for i in range(0,20,1):
        if val == str(i/10):
            color = 'red'
        else:
            pass
    for i in range(20,30,1):
        if val == str(i/10):
            color = 'orange'
        else:
            pass
    for i in range(30,40,1):
        if val == str(i/10):
            color = 'yellow'
        else:
            pass
    for i in range(40,50,1):
        if val == str(i/10):
            color = 'green'
        else:
            pass
        
    return 'background-color: %s' % color


def padronize_planosp_parameters(sp_casos,sp_internacoes):
    mask = (sp_casos['casos_var'].notnull()) & (sp_casos['obitos_var'].notnull()) & (sp_casos['obitos_var']!= np.inf)
    aux_df = sp_casos[mask]

    final = pd.merge(aux_df,sp_internacoes,on=['datahora','nome_drs'],how='outer')
    mask = final['nome_drs'].str.startswith('Grande')
    final = final[np.logical_not(mask)]
    final['leitos_pc'] = final['leitos_pc'].str.replace(',','.')

    final = final[(final['leitos_pc'].notnull()) & (final['casos_var'].notnull())]

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

    final['nome_drs'] = final['nome_drs'].map(rename_drs)


    # mask  = final['nome_drs'].isin(['a'])
    # mask = np.logical_not(mask)

    final['pop'] = final['pop'].astype(int)

    final['internacoes_14d_pc'] = (final['internacoes_14d'] * 10**5 )/final['pop']
    final['obitos_14d_pc'] = (final['obitos_14d']  * 10**5 )/final['pop']
    final['casos_14d_pc'] = (final['casos_14d']  * 10**5 )/final['pop']
    
    mask = final['nome_drs'].notnull()
    final = final[mask].sort_values(by=['nome_drs','datahora'])


    final['casos_mm7'] = final[['nome_drs','casos_novos']].groupby(by='nome_drs', as_index=False).rolling(7).mean()['casos_novos'].tolist()
    final['obitos_mm7'] = final[['nome_drs','obitos_novos']].groupby(by='nome_drs', as_index=False).rolling(7).mean()['obitos_novos'].tolist()

    final['casos_pm'] = (final['casos_novos']  * 10**6 )/final['pop']
    final['obitos_pm'] = (final['obitos_novos']  * 10**6 )/final['pop']
    final['leitos_pc'] = final['leitos_pc'].astype(float)
    
    
    return final


def padronize_casos_sp(casos,pop,final):
    cols = ['datahora','codigo_ibge','nome_munic','casos_novos','obitos_novos','nome_drs']
    ssp = casos[cols][casos['nome_drs'].notnull()]

    ssp = ssp.merge(pop, on='codigo_ibge', how='left')

    ssp['casos_pm'] = (ssp['casos_novos'].astype(float)  * 10**6 )/ssp['pop'].astype(float)
    ssp['obitos_pm'] = (ssp['obitos_novos'].astype(float)  * 10**6 )/ssp['pop'].astype(float)

    ssp['nome_drs'] = ssp['nome_munic']
    ssp = ssp.drop(columns=['nome_munic','codigo_ibge'])

    cols = ['nome_drs','datahora','casos_novos','casos_pm','obitos_novos','obitos_pm', 'pop']
    ssp = ssp[cols]

    ssp = pd.concat([ssp,final[cols]], axis=0)
    
    return ssp