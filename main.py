import pandas as pd
from youtubesearchpython import *
import json
import numpy as np
import urllib.request
import random

df = pd.read_csv("./real.csv", index_col=[0])
df.reset_index(inplace=True)

def extract_convert(busqueda, sugs, cantida_resultados, position):
  #Extraemos los datos
  videosSearch = VideosSearch(busqueda, limit = cantida_resultados)
  results = videosSearch.result(mode = ResultMode.json)
  #lo convertimos a json para poder manipular mejor
  json_response = json.loads(results)
  text = json_response['result'][position]
  #Datos mas exactos
  video = Video.getInfo(text['link'], mode = ResultMode.json)
  miniaturahd = "https://img.youtube.com/vi/" + video['id'] + "/maxresdefault.jpg"
  canal = Channel.get(video['channel']['id'])
  datos = [
      {'Title': text['title'], 'Search sugs': busqueda, 'Link': text['link'], 'Thumbnail': miniaturahd, 'View Count:':video['viewCount']['text'],'Keywords Tags': video['keywords'], 'Duration Seconds': video['duration']['secondsText'], 'Duration Minuts': text['duration'], 'Upload Date': video['uploadDate'], 'published Time': text['publishedTime'], 'Category': video['category'], 'All Video Description': video['description'], 'Channel': text['channel']['name'],'Subscribers': canal['subscribers']['simpleText'], 'Channel Description': canal['description'], 'Banner Chanel': canal['banners'][5]['url'], 'Keywords channel': canal['keywords'], 'Channel Total Views': canal['views'], 'Channel Join': canal['joinedDate'], 'Country': canal['country'] }
  ]
  link = text['link']
  return datos, link, miniaturahd


def search_sugs():
  bus = ["Como aprender a programar python", "consejos para aprender a programar python", "secreto para aprender a programar python", "truco para aprender a programar python", "logica aprender programacion python", "conseguir aprender programacion python"]

  a = ["ciencia de datos", "python ", "data science ", "programacion ", "rapido ", "profesional ","poco tiempo ", "desde cero ", "facil " ]
  busqueda = bus[np.random.randint(0, len(bus) -1)] + " " + a[np.random.randint(0, len(a) -1)]
  suggestions = Suggestions(language = 'es', region = 'US')
  sugetions = suggestions.get(busqueda, mode = ResultMode.json)
  json_s = json.loads(sugetions)
  sugs = json_s['result']
  #neword = []
  #words = list(sugs)
  #for i in words:
  #  neword.append(i[len(busqueda):])

  #busqueda = a[0][np.random.randint(0, 4)], a[1][np.random.randint(0, 4)], a[2][np.random.randint(0, 4)], neword[np.random.randint(0, len(neword))]
  return busqueda, sugs


def thunbnail(miniaturahd, link):
  urllib.request.urlretrieve(miniaturahd,"./thunbnail/" + link[32:] + ".jpg")
cantida = 0
repeat = 0

while cantida < 3:
  busqueda, sugs = search_sugs()
  if repeat > 1 and sugs != None:
    busqueda = sugs[random.randint(0, len(sugs)-1)]
    repeat = 0
  try:
    datos, link, miniaturahd = extract_convert(busqueda, sugs, 7, 0)
    datos2, link2, miniaturahd2 = extract_convert(busqueda, sugs, 7, 1)
    datos3, link3, miniaturahd3 = extract_convert(busqueda, sugs, 7, 2)
  except TypeError:
    print("Object found none type error")
  if miniaturahd and miniaturahd2 and miniaturahd3:
    try:
      thunbnail(miniaturahd, link)
      thunbnail(miniaturahd2, link2)
      thunbnail(miniaturahd3, link3)
    except urllib.error.HTTPError:
      print("Thunbnail no found Error 404 ")

  #Position 1 yt search
  df_new = pd.DataFrame(datos)
  #2
  df_new2 = pd.DataFrame(datos2)
  #3
  df_new3 = pd.DataFrame(datos)
  df_link = list(df["Link"])



  if link in df_link:
    repeat += 1
  else:
    df = pd.concat([df, df_new]).reset_index(drop=True)    

  if link2 in df_link:
    repeat += 1
  else:
    df = pd.concat([df, df_new2]).reset_index(drop=True)

  if link3 in df_link:
    repeat += 1
    print("Doble detect")
  else:
    df = pd.concat([df, df_new3]).reset_index(drop=True)

  cantida += 1
  print("Search Done: {}, Element Repeat: {}".format(cantida, repeat))


print(df.info())
df.to_csv('trending_yt.csv', index=None)
