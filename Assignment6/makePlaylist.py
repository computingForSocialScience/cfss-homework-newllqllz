from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
import sys
import requests
import csv
import random
from io import open

if __name__ == '__main__':
	artistList  =[]
	overallNetwork=pd.DataFrame()
	NumOfArtist = len(sys.argv)  # infact it's num of artist +1
	for i in range(1,NumOfArtist):
		artistList.append(sys.argv[i])
	for artist in artistList:
		writeEdgeList(fetchArtistId(artist), 2, "F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\"+artist+".csv")

	for i in range(0,NumOfArtist-1): #combine edges
		if i==0:
			overallNetwork.append(readEdgeList("F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\"+artistList[i]+".csv"))
			

		else:
			overallNetwork = combineEdgeLists(pd.DataFrame(overallNetwork), readEdgeList("F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\"+artistList[i]+".csv"))


	FinalArtistDic = {}
	i = 0
	while i<30:
		point = randomCentralNode(pandasToNetworkX(overallNetwork))
		if not FinalArtistDic.has_key(point):
			FinalArtistDic[point]=1
			i +=1
		if i>50:
			break
		
	FinalArtistList = FinalArtistDic.keys()
	
	outFile=open('F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\playlist.csv','w',encoding='utf-8')
	outFile.write(u'ARTIST_NAME,ALBUM_NAME,TRACK_NAME\n')
	for artist in FinalArtistList:
		tempList = fetchAlbumIds(artist)

		ranNum = len(tempList)-1
		randomAlbum = tempList[random.randint(0,ranNum)]
		album_name = fetchAlbumInfo(randomAlbum)['name']
		artist_name = fetchArtistInfo(artist)['name']
		TrackUrl = "https://api.spotify.com/v1/albums/"+randomAlbum+"/tracks?limit=1"
		track_name = requests.get(TrackUrl).json()['items'][0]['name']
		outFile.write("\""+artist_name+"\""+","+"\""+album_name+"\""+","+"\""+track_name+"\""+"\n")
	outFile.close()
		


