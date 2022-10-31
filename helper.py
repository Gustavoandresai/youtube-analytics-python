from youtubesearchpython import *
import json

def process_results(search, number_result):
     #Exactact data
    videosSearch = VideosSearch(search, limit = number_result)
    results = videosSearch.result(mode = ResultMode.json)
    #Convert to json for handle it better
    json_response = json.loads(results)
    data = json_response['result']
    datos = {}
    none = 0
    for idx, text in enumerate(data):
        #text = json_response['result'][idx]
    #data more exactly

        video = Video.getInfo(text['link'], mode = ResultMode.json)
        miniaturahd = "https://img.youtube.com/vi/" + video['id'] + "/maxresdefault.jpg"
        canal = Channel.get(video['channel']['id'])
        #If any data is not found, leave the box blank
        try:
            datos[idx] = {'Title': text['title'], 'Search': search, 'Link': text['link'], 'Thumbnail': miniaturahd, 'View Count:':video['viewCount']['text'],'Keywords Tags': video['keywords'], 'Duration Seconds': video['duration']['secondsText'], 'Duration Minuts': text['duration'], 'Upload Date': video['uploadDate'], 'published Time': text['publishedTime'], 'Category': video['category'], 'All Video Description': video['description'], 'Channel': text['channel']['name'],'Subscribers': canal['subscribers']['simpleText'], 'Channel Description': canal['description'], 'Banner Chanel': canal['banners'][5]['url'], 'Keywords channel': canal['keywords'], 'Channel Total Views': canal['views'], 'Channel Join': canal['joinedDate'], 'Country': canal['country'] }
        except TypeError:
            none += 1
            print(TypeError)
            print('\n we have', none, ' blank boxes nonetype')
        #link = text['link']
    return datos


def count_words(value):
     #create a cycle For count the words and get what are de the most used word
    diccionario = dict()
    for i in range(len(value)):
        cadena = value[i]
        palabras = cadena.split(" ")
        for p in palabras:
            diccionario[p] = diccionario.get(p, 0) + 1
    return diccionario

def count_words2(value):
     #create a cycle For count the words and get what are de the most used word
    diccionario = dict()
    for i in range(len(value)):
        cadena = value[i]
        palabras = str(cadena).split("'")
        for p in palabras:
            diccionario[p] = diccionario.get(p, 0) + 1
    diccionario.pop(", ")
    del diccionario['[']
    del diccionario[']']

    return diccionario