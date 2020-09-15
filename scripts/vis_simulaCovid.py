# matplotlib
from matplotlib import pyplot as plt
from matplotlib.dates import date2num, num2date
from matplotlib import dates as mdates
from matplotlib import ticker
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# scipy specifics
from scipy import stats as sps
from scipy.stats import dirichlet
from scipy.interpolate import interp1d

# GAMs and sklearn
from sklearn.utils import resample

import pandas as pd
import numpy as np


import plotly.graph_objs as go
from scripts import vis_layout



def plot_rt(result, ax, state_name):
    
    """
    Function to plot Rt

    Arguments
    ----------
    result: expected value and HDI of posterior

    ax: matplotlib axes 

    state_name: state to be considered

    See also
    ----------
    This code is heavily based on Realtime R0
    by Kevin Systrom
    https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb
    """
#     result.index = result['last_updated']
    result.index = pd.to_datetime(result['last_updated'])

    ax.set_title(f"{state_name}")
    
    # Colors
    ABOVE = [1,0,0]
    MIDDLE = [1,1,1]
    BELOW = [0,0,0]
    cmap = ListedColormap(np.r_[
        np.linspace(BELOW,MIDDLE,25),
        np.linspace(MIDDLE,ABOVE,25)
    ])
    color_mapped = lambda y: np.clip(y, .5, 1.5)-.5
    
    index = result['Rt_most_likely'].index.get_level_values('last_updated')
    values = result['Rt_most_likely'].values
    
    # Plot dots and line
    ax.plot(index, values, c='k', zorder=1, alpha=.25)
    ax.scatter(index,
               values,
               s=40,
               lw=.5,
               c=cmap(color_mapped(values)),
               edgecolors='k', zorder=2)
    
    # Aesthetically, extrapolate credible interval by 1 day either side
    lowfn = interp1d(date2num(index),
                     result['Rt_low_95'].values,
                     bounds_error=False,
                     fill_value='extrapolate')
    
    highfn = interp1d(date2num(index),
                      result['Rt_high_95'].values,
                      bounds_error=False,
                      fill_value='extrapolate')
    
    extended = pd.date_range(start=pd.Timestamp('2020-03-01'),
                             end=index[-1]+pd.Timedelta(days=1))
    
    ax.fill_between(extended,
                    lowfn(date2num(extended)),
                    highfn(date2num(extended)),
                    color='k',
                    alpha=.1,
                    lw=0,
                    zorder=3)

    ax.axhline(1.0, c='k', lw=1, label='$R_t=1.0$', alpha=.25);
    
    # Formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}"))
    ax.yaxis.tick_right()
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.margins(0)
    ax.grid(which='major', axis='y', c='k', alpha=.1, zorder=-2)
    ax.margins(0)
    ax.set_ylim(0.0, 5.0)
    ax.set_xlim(pd.Timestamp('2020-03-01'), result.index.get_level_values('last_updated')[-1]+pd.Timedelta(days=1)) 
    
    
    



def plot_rt_bars(df, title, place_type='state'):
    
    
    line_color = '#E0E0E0'
    bar_color  = '#D8514E'
    
    # df['color'] = np.where(df['Rt_most_likely'] > 1.2,
    #                        'rgba(242,185,80,1)',
    #                        np.where(df['Rt_most_likely'] > 1, 
    #                                 'rgba(242,185,80,1)',
    #                                 '#0A96A6'))

    fig = go.Figure(go.Bar(x=df[place_type],
                          y=df['Rt_most_likely'],
                          marker_color=bar_color,
                          error_y=dict(
                            type='data',
                            symmetric=False,
                            array=df['Rt_most_likely'] - df['Rt_low_95'],
                            arrayminus=df['Rt_most_likely'] - df['Rt_low_95'])))
    
    fig.add_shape(
        # Line Horizontal
            type="line",
            x0=-1,
            x1=len(df[place_type]),
            y0=1,
            y1=1,
            line=dict(
                color=line_color,
                width=2,
                dash="dash",
            ),
    )

    fig.update_layout({'template': 'plotly_white', 
                       'title': title})
    
    return fig.update_layout(hovermode = 'x unified')


def plot_rt_plotly(dd, themes):
    colors =  themes['data']['colors']
    factor = int(np.ceil(len(dd['nome_municipio'])/len(colors)))    
    colors = factor * colors
    
    data = []
    i=0
    
    for city in dd['nome_municipio'].unique():
        mask =dd['nome_municipio']==city
        dc = dd[mask]

        
        
        trace = go.Scatter(
            name=city,
            x=dc['last_updated'], 
            y=dc['Rt_most_likely'],
            line=dict(color=colors[i], width=themes['data']['line_width']),
            mode='lines+markers',
            marker=dict(size=themes['data']['marker_size']),
            hoverlabel=dict(namelength=-1, font=dict(size=themes['data']['hoverlabel_size'])),
        )
        data.append(trace)
        i+=1

    
    layout = vis_layout.get_layout_new(themes,var = 'Rt_most_likely',scale='linear')

    fig = go.Figure(data=data, layout=layout)
    
    return fig
