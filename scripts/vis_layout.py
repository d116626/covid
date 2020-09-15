

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline


def get_layout(themes, title='', x_name='', y_name='', tipo=None):
    
    layout = go.Layout(
        # automargin=True,
        margin=dict(l=themes['margin']['l'],
                    r=themes['margin']['r'],
                    t=themes['margin']['t'],
                    b=themes['margin']['b']),
        
        barmode=themes['barmode'],
        hovermode=themes['hovermode'],

        autosize=True,
        
        # automargin=True,
    #     title=dict(
    #         text=title,
    #         x=0.5,
    # #         y=0.9,
    #         xanchor='center',
    #         yanchor='top',
    #         font = dict(
    #             size=themes['title']['size'],
    #             color=themes['title']['color']
    #         )
    #     ),

        # xaxis_title=x_name,
        
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
            tickformat=themes['axis_legend']['tickformat']['y'],
            type=tipo,
        ),
        
        
        font=dict(
            size=themes['axis_tilte']['size'],
            color=themes['axis_tilte']['color']
        ),
        

        legend=go.layout.Legend(
            x=themes['legend']['position']['x'],
            y=themes['legend']['position']['y'],
            xanchor = themes['legend']['position']['xanchor'],
            yanchor = themes['legend']['position']['yanchor'],
            traceorder =themes['legend']['traceorder'],
            orientation=themes['legend']['orientation'],
            font=dict(
                family=themes['legend']['family'],
                size=themes['legend']['size'],
                color=themes['legend']['color']
            ),
            bgcolor=themes['legend']['bgcolor'] ,
            bordercolor=themes['legend']['bordercolor'],
            borderwidth=themes['legend']['borderwidth'],
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



def get_layout_new(themes,var, scale):

    layout = go.Layout(
        hovermode=themes['hovermode'],
        
        margin=dict(l=themes['margin']['l'],
                    r=themes['margin']['r'],
                    t=themes['margin']['t'],
                    b=themes['margin']['b']),
        
        barmode=themes['barmode'],
        autosize=True,
        
        title=dict(
            text=themes['vars'][var]['title'],
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top',
            font = dict(
                size=themes['title']['size'],
                color=themes['title']['color']
            )
        ),

        xaxis_title=themes['vars'][var]['x_title'],
        
        
        
        xaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
        gridcolor=themes['axis_legend']['gridcolor'],
        zerolinecolor=themes['axis_legend']['gridcolor'],
        linecolor=themes['axis_legend']['gridcolor'],
        # linewidth=2,
        # mirror=True,
        tickformat =themes['axis_legend']['scale'][scale]['x']['tickformat'],
        type=themes['axis_legend']['scale'][scale]['x']['type'],

        ),
        
        
        yaxis_title=themes['vars'][var]['y_title'],
        
        yaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
            gridcolor=themes['axis_legend']['gridcolor'],
            zerolinecolor=themes['axis_legend']['gridcolor'],
            # linecolor=themes['axis_legend']['gridcolor'],
            # linewidth=2,
        tickformat =themes['axis_legend']['scale'][scale]['y']['tickformat'],
        type=themes['axis_legend']['scale'][scale]['y']['type']
        ),
        
        
        font=dict(
            size=themes['axis_tilte']['size'],
            color=themes['axis_tilte']['color']
        ),
        

        legend=go.layout.Legend(
            x=themes['legend']['position']['x'],
            y=themes['legend']['position']['y'],
            xanchor = themes['legend']['position']['xanchor'],
            yanchor = themes['legend']['position']['yanchor'],
            traceorder =themes['legend']['traceorder'],
            orientation=themes['legend']['orientation'],
            font=dict(
                family=themes['legend']['family'],
                size=themes['legend']['size'],
                color=themes['legend']['color']
            ),
            bgcolor=themes['legend']['bgcolor'] ,
            bordercolor=themes['legend']['bordercolor'],
            borderwidth=themes['legend']['borderwidth'],
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




def get_layout_bar(themes):

    layout = go.Layout(
        hovermode=themes['hovermode'],

        margin=dict(l=themes['margin']['l'],
                    r=themes['margin']['r'],
                    t=themes['margin']['t'],
                    b=themes['margin']['b']),
        
        barmode=themes['barmode'],
        autosize=True,
        
        xaxis_title=themes['axis_legend']['x']['title'],
        xaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
        gridcolor=themes['axis_legend']['gridcolor'],
        zerolinecolor=themes['axis_legend']['gridcolor'],
        linecolor=themes['axis_legend']['gridcolor'],
        # linewidth=2,
        # mirror=True,
        tickformat=themes['axis_legend']['scale']['linear']['x']['tickformat'],
        type=themes['axis_legend']['scale']['linear']['x']['type'],

        ),
        
        
        yaxis_title=themes['axis_legend']['y']['title'],
        yaxis = dict(
            tickfont=dict(
                size=themes['axis_legend']['size'],
                color=themes['axis_legend']['color'],
            ),
            gridcolor=themes['axis_legend']['gridcolor'],
            zerolinecolor=themes['axis_legend']['gridcolor'],
            # linecolor=themes['axis_legend']['gridcolor'],
            # linewidth=2,
            tickformat=themes['axis_legend']['scale']['linear']['y']['tickformat'],
            type=themes['axis_legend']['scale']['linear']['y']['type'],
        ),
        
        
        font=dict(
            size=themes['axis_tilte']['size'],
            color=themes['axis_tilte']['color']
        ),

        legend=go.layout.Legend(
            x=themes['legend']['position']['x'],
            y=themes['legend']['position']['y'],
            xanchor = themes['legend']['position']['xanchor'],
            yanchor = themes['legend']['position']['yanchor'],
            traceorder =themes['legend']['traceorder'],
            orientation=themes['legend']['orientation'],
            font=dict(
                family=themes['legend']['family'],
                size=themes['legend']['size'],
                color=themes['legend']['color']
            ),
            bgcolor=themes['legend']['bgcolor'] ,
            bordercolor=themes['legend']['bordercolor'],
            borderwidth=themes['legend']['borderwidth'],
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