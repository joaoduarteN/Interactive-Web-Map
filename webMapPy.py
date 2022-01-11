import folium
from folium.map import Icon
import pandas as pd

#creating the map. putting some tiles that can be known in help(folium.Map)
map1 = folium.Map(location=[-20,-30], zoom_start = 3, tiles="Stamen Terrain")
volcTable = pd.read_csv("Volcanoes.txt")
latitude = list(volcTable["LAT"]) #creating a list out of a specific column
longitude = list(volcTable["LON"])
volcName = list(volcTable["NAME"])
elevation = list(volcTable["ELEV"])

html = """
Name:
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
<br>
Height: %s m
"""


#Define the color of the markers, according do the height
def colorDefine(elevation):
    if elevation < 2000:
        return "green"
    elif elevation >= 2000 and elevation < 3000:
        return "orange"
    elif elevation >= 3000 and elevation < 4000:
        return "darkred"
    else:
        return "black"

#Creating one feature group
group = folium.FeatureGroup(name="Volcanoes")
for lat,lon, name, elev in zip(latitude, longitude, volcName, elevation):#it makes the code iterate through both simultaneously
    frame = folium.IFrame(html = html % (str(name), str(name), str(elev)), width=250, height=150)
    group.add_child(folium.CircleMarker(location=[lat, lon], popup=folium.Popup(frame) , radius=5, 
    fill_color=colorDefine(int(elev)), color = colorDefine(int(elev)), fill_opacity = 0.85))

#Another feature group
group2 = folium.FeatureGroup(name="Population")

#Polygons to show the population of each country: "POP2005"in the json file
#Colors will fill the countries according to their population
group2.add_child(folium.GeoJson(data =open("world.json", "r", encoding="utf-8-sig").read(),
style_function=lambda x:{"fillColor":"green" if x["properties"]["POP2005"] < 10000000 
else "yellow" if 10000000 <= x["properties"]["POP2005"]< 20000000
else "orange" if 20000000 <= x["properties"]["POP2005"]< 40000000
else "red" if 40000000 <= x["properties"]["POP2005"]< 1000000000
else "darkRed"})) #in x, we find this "place" in the json file


map1.add_child(group2)
map1.add_child(group)

#Now that we have some different layers, let's add a layer control in the program:
map1.add_child(folium.LayerControl())

#just to have it on excel
volcTable.to_excel("volcTable.xlsx")
map1.save("map1.html")

