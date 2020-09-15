import folium
import folium



import branca.colormap as cm
import branca

def get_map(dd_final, variavel, cols ,ufs):
    
    #min and max color map range
    minn = min(dd_final[variavel])
    maxx = max(dd_final[variavel])

    #create a equal divised range
    indexx = [minn]
    n_divisions = 4
    factor = round(((maxx - minn)/n_divisions))
    for i in range(1,n_divisions):
        number  = minn+i*factor
        indexx.append(number)
    indexx.append(maxx)

    #add the colors to colormap
    # ['#DB4325','#ECA14D','#E6E1BC','#5BC2AF','#096264']
    colors = ['#E6E1BC','#ECA14D','#F9A602','#F05E23','#883002']
    colormap = colormap = cm.LinearColormap(colors=colors, index=indexx,vmin=round(minn),vmax=maxx)

    mymap = folium.Map(location=[-15.734392, -54.026147], 
                    zoom_start=5, min_zoom=4, max_zoom=12,
                    tiles='CartoDB positron')

    #legend caption

    colormap.caption = "Número de Casos Confirmados"


    #add color in polygons
    style_function = lambda x: {"weight":3, 
                                'color':'black',
                                'fillColor':'rgba(0,0,0,0)', 
                                'fillOpacity':0.75}

    #add edge in map
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.5, 
                                    'weight': 3}
    

    
    NIL=folium.features.GeoJson(
            ufs,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            #show the chosen variables
            tooltip=folium.features.GeoJsonTooltip(
                fields=cols[1:],
    #             aliases=['Neighborhood','% of foreign resident population'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                sticky=True
            )
        )
        
    mymap.add_child(NIL)


    #add color in polygons
    style_function = lambda x: {"weight":0.5, 
                                'color':'black',
                                'fillColor':colormap(x['properties'][variavel]), 
                                'fillOpacity':0.75}

    #add edge in map
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    
    NIL=folium.features.GeoJson(
            dd_final,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            #show the chosen variables
            tooltip=folium.features.GeoJsonTooltip(fields=cols,
    #             aliases=['Neighborhood','% of foreign resident population'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                sticky=True
            )
    )
    
    
    colormap.add_to(mymap)
    mymap.add_child(NIL) 

    return(mymap)


def get_map_vale(dd_final,variavel,cols, ufs):
    
    #min and max color map range
    minn = min(dd_final[variavel])
    maxx = max(dd_final[variavel])

    #create a equal divised range
    indexx = [minn]
    n_divisions = 4
    factor = round(((maxx - minn)/n_divisions))
    for i in range(1,n_divisions):
        number  = minn+i*factor
        indexx.append(number)
    indexx.append(maxx)

    #add the colors to colormap
    # ['#DB4325','#ECA14D','#E6E1BC','#5BC2AF','#096264']
    colors = ['#E6E1BC','#ECA14D','#F9A602','#F05E23','#883002']
    colormap = colormap = cm.LinearColormap(colors=colors, index=indexx,vmin=round(minn),vmax=maxx)


    #create map
    mymap = folium.Map(location=[-23.234392, -45.026147], 
                    zoom_start=7, min_zoom=4, max_zoom=10,
                    tiles='CartoDB positron')
    #legend caption

    colormap.caption = "Número de Casos Confirmados"


    #add color in polygons
    style_function = lambda x: {"weight":3, 
                                'color':'black',
                                'fillColor':'rgba(0,0,0,0)', 
                                'fillOpacity':0.75}

    #add edge in map
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.5, 
                                    'weight': 3}
    
    NIL=folium.features.GeoJson(
            ufs,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            #show the chosen variables
            tooltip=folium.features.GeoJsonTooltip(
                fields=['Estado','Confirmados', 'Óbitos', 'Data do Boletim'],
    #             aliases=['Neighborhood','% of foreign resident population'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                sticky=True
            )
        )
        
    mymap.add_child(NIL)




    #add color in polygons
    style_function = lambda x: {"weight":0.5, 
                                'color':'black',
                                'fillColor':colormap(x['properties'][variavel]), 
                                'fillOpacity':0.75}

    #add edge in map
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    
    # print(minn,maxx)
    
    NIL=folium.features.GeoJson(
            dd_final,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            #show the chosen variables
            tooltip=folium.features.GeoJsonTooltip(fields=cols,
    #             aliases=['Neighborhood','% of foreign resident population'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                sticky=True
            )
    )
    
    
    colormap.add_to(mymap)
    mymap.add_child(NIL)
    
    
    
    vale = dd_final.copy()
    mask = vale['Óbitos']>0
    vale_obitos = vale[mask]

    vale_obitos['coords'] = vale_obitos['geometry'].apply(lambda x: x.representative_point().coords[:])
    vale_obitos['coords'] = [coords[0] for coords in vale_obitos['coords']]

    vale_obitos['lat'] = vale_obitos['coords'].apply(lambda x: x[0])
    vale_obitos['lng'] = vale_obitos['coords'].apply(lambda x: x[1])

    locations = vale_obitos[['lng', 'lat']]
    locationlist = locations.values.tolist()

    municipio = vale_obitos['Município'].to_list()
    obitos = vale_obitos['Óbitos'].to_list()
    
    # icon_url = "https://cdn3.iconfinder.com/data/icons/pictomisc/100/skull-512.png"
    # icon = folium.CustomIcon(icon_url,icon_size=(14, 14))

    # import base64
    # from io import BytesIO
    
    # encoded = base64.b64encode(open('../icon/skull-solid.svg', 'rb').read())
    # decoded = base64.b64decode(encoded)
    # icon_url = '../icon/skull-solid.svg'
    # icon = folium.features.CustomIcon(icon_url, icon_size=(50,50))


    for i in range(0, len(locationlist)):
        
        text = "<b>Município:</b> " + str(municipio[i]) \
        + '<br>''<br>'+ "<b>Óbitos:</b> "+ str(obitos[i]) \
        
        size=0.5
        popup = text
    #     iframe = folium.IFrame(text,width=400*size, height=300*size,     ratio='70%')
    #     popup = folium.Popup(iframe,    max_width='100%')
        
        folium.Marker(locationlist[i], 
                    popup=popup, 
                    icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(mymap)






    return(mymap)



