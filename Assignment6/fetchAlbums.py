import requests
from datetime import datetime
from io import open

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = "https://api.spotify.com/v1/artists/"+artist_id+"/albums?album_type=album&market=US"
    r=requests.get(url)
    data = r.json()
    albumIds = []
    for item in data["items"]:
    	albumIds.append(item["id"])
    #print data["items"][0]["id"]
    return albumIds

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    dic = {}
    url = "https://api.spotify.com/v1/albums/"+album_id
    r = requests.get(url)
    data = r.json()
    dic["artist_id"]=data["artists"][0]["id"]
    dic["album_id"] = data["id"]
    dic["name"] = data["name"]
    dic["year"] = data["release_date"][0:4]
    dic["popularity"] = data["popularity"]
    #print dic
    return dic


#albumList = fetchAlbumIds(u'6vWDO969PvNqNYHIOW5v0m')
#al_dic=fetchAlbumInfo(albumList[3])


