#%%
# importer les packages
from download import download
import pandas as pd
import folium
from openrouteservice import convert
import openrouteservice
import json
from ipywidgets import interact
#%%
# importer la base de données coordonnées.csv
geo = pd.read_csv('./coordonnées.csv')
geo = geo.rename(columns={' NOMGARE ':'NOM GARE'})

# Crée une liste qui contient le nom de toutes les villes
villes = sorted(geo.NOMGARE.unique())

def itineraire(DEPART, ARRIVEE):
    i=geo.loc[geo['NOMGARE'] == DEPART].index[0]
    j=geo.loc[geo['NOMGARE'] == ARRIVEE].index[0]
    
    # Résolution du problème de la distance différente entre
    # l'aller et le retour avec une boucle
    if i < j:

        x = [geo['X'][i], 
             geo['Y'][i]]
        
        y = [geo['X'][j], 
             geo['Y'][j]]

        coor = [x, y]

        client = openrouteservice.Client(key='5b3ce3597851110001cf6248a649f5b5021e4f02b016b51649758663')  # Specify your personal API key

        m = folium.Map(
                        location=[43.1837661, 3.0042121],
                        zoom_start=10,
                        control_scale=True)

        for i in range(0, len(coor)-1):
            coord = coor[i], coor[i+1]
            res = client.directions(coord)

            with(open('test.json', '+w')) as f:
                f.write(json.dumps(res, indent=4, sort_keys=True))

                geometry = client.directions(coord)['routes'][0]['geometry']
                decoded = convert.decode_polyline(geometry)

                folium.GeoJson(decoded).add_child(folium.Popup(max_width = 300)).add_to(m)

                folium.Marker(
                            coord[0][::-1],
                            popup=DEPART,
                            tooltip=DEPART
                             ).add_to(m)

                folium.Marker(
                            coord[1][::-1],
                            popup=ARRIVEE,
                            tooltip=ARRIVEE
                             ).add_to(m)
        return m

    elif i > j:

        y = [geo['X'][i],
             geo['Y'][i]]
        
        x = [geo['X'][j],
             geo['Y'][j]]

        coor = [x, y]

        client = openrouteservice.Client(key='5b3ce3597851110001cf62486f5564a064e34f3895221e5a0d9a2405')
        m = folium.Map(
                        location=[43.1837661, 3.0042121],
                        zoom_start=10,
                        control_scale=True)

        for i in range(0, len(coor)-1):
            coord = coor[i], coor[i+1]
            res = client.directions(coord)

            with(open('test.json', '+w')) as f:
                f.write(json.dumps(res, indent=4, sort_keys=True))

                geometry = client.directions(coord)['routes'][0]['geometry']
                decoded = convert.decode_polyline(geometry)

                folium.GeoJson(decoded).add_child(folium.Popup(max_width = 300)).add_to(m)

                folium.Marker(
                            coord[0][::-1],
                            popup=DEPART,
                            tooltip=DEPART
                             ).add_to(m)

                folium.Marker(
                            coord[1][::-1],
                            popup=ARRIVEE,
                            tooltip=ARRIVEE
                             ).add_to(m)
        return m
    
    else :
        print("Veuilliez entrer deux sorties différentes")  

interact(itineraire, DEPART = villes, ARRIVEE = villes)