from flask import Flask, render_template, request, redirect, url_for
import pymysql
from fetchAlbums import *
from fetchArtist import *
from artistNetworks import *
from analyzeNetworks import *
import random

dbname="playlists"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    sql = "SELECT id, rootArtist FROM playlist;"
    cur.execute(sql)
    playlists_dic={}
    for tup in cur.fetchall():
        #print name
        playlists_dic[tup[0]]=tup[1]
    return render_template('playlists.html',playlists=playlists_dic)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur = db.cursor()
    sql = "SELECT songOrder,artistName,albumName,trackName FROM songs WHERE playlistId = %s ;" #
    cur.execute(sql,playlistId)
    songs=[]
    for item in cur.fetchall():
        print item
        songs.append(item)
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        return(redirect("/playlists/"))



def createNewPlaylist(artist_name):
    cur = db.cursor()
    sql_create_playlists ='''CREATE TABLE IF NOT EXISTS playlist (id INTEGER PRIMARY KEY AUTO_INCREMENT,rootArtist VARCHAR(128));'''
    sql_create_songs ='''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER,artistName VARCHAR(128), albumName VARCHAR(256), trackName VARCHAR(256));'''
    cur.execute(sql_create_playlists)
    cur.execute(sql_create_songs)


    sql_insert_artist_name = "INSERT INTO playlist (rootArtist) VALUES ('%s');" % (artist_name)
    cur.execute(sql_insert_artist_name)

    sql_select_id = """SELECT id FROM playlist;"""
    cur.execute(sql_select_id)
    playlistId = cur.fetchall()[0][0]
    print playlistId
    #print type(playlistId)
    

    #get artistlist:
    depth=2
    artist_id = fetchArtistId(artist_name)
    edgelist = getEdgeList(artist_id,depth)
    FinalArtistDic = {}
    i = 0
    while i<50:
        point = randomCentralNode(pandasToNetworkX(edgelist))
        if not FinalArtistDic.has_key(point):
            FinalArtistDic[point]=1
            i +=1
        if i>2:
            break
        
    FinalArtistList = FinalArtistDic.keys()

    for artist in FinalArtistList:
        tempList = fetchAlbumIds(artist)

        ranNum = len(tempList)-1
        randomAlbum = tempList[random.randint(0,ranNum)]
        album_name = '"'+fetchAlbumInfo(randomAlbum)['name'].replace("'","")+'"'
        artist_name2 ='"'+fetchArtistInfo(artist)['name'].replace("'","")+'"'
        TrackUrl = "https://api.spotify.com/v1/albums/"+randomAlbum+"/tracks?limit=1"
        track_name ='"'+requests.get(TrackUrl).json()['items'][0]['name'].replace("'","")+'"'
        print artist_name2,'----', album_name,'----', track_name
        #couldn't get it right
        sql_insert_song_info = """INSERT INTO songs (playlistId,songOrder,artistName,albumName,trackName) VALUES ('%s','%s','%s','%s','%s');""" % (playlistId,FinalArtistList.index(artist)+1,artist_name2,album_name,track_name)
        cur.execute(sql_insert_song_info)
        
        db.commit()

    
    sql_select_songs = """SELECT * FROM songs;"""
    cur.execute(sql_select_songs)
    songs_info = cur.fetchall()
    for item in songs_info:
        print item
    cur.close()




if __name__ == '__main__':
    # cur = db.cursor()
    # sql = "SELECT songOrder,artistName,albumName,trackName FROM songs ;" #WHERE playlistId = %s
    # cur.execute(sql)
    # songs=[]
    # for item in cur.fetchall():
    #     print item
    app.debug=True
    app.run()
    #createNewPlaylist("Beyonce")