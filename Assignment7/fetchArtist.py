import sys
import requests
import csv
from io import open 



def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url = "https://api.spotify.com/v1/search?q="+name+"&type=artist"
    r=requests.get(url)
    data = r.json()
    id = data['artists']["items"][0]['id']
    #print type(data['artists']['items'])
    #print r['id']
    return id

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = "https://api.spotify.com/v1/artists/"+artist_id
    r = requests.get(url)
    data = r.json()
    dic = {}
    dic["followers"]=data["followers"]
    dic["genres"]=data["genres"]
    dic["id"]=data["id"]
    dic['name']=data['name']
    dic["popularity"]=data["popularity"]

    return dic

#artist_id =fetchArtistId("Beyonce")  
#print "this is the information of the artists:"
#artics_dic=fetchArtistInfo(artist_id) 
#print artics_dic




