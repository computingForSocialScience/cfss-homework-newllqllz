import sys
import requests
import csv
import pandas as pd
import numpy as np

def getDepthEdges(artistID, depth):
	networkTuple=[]
	networkList =[[] for i in range(depth)]
	index0 =0
	index1 =0

	def CheckAlreadyThere(artistFrom, artistTowards):
		for tup in networkTuple:
			if (artistFrom in tup):
				if (artistTowards in tup):
					return True
		return False

	for d in range(1,depth+1):
		print 'd= %d' % d
		if d ==1:
			networkList[0].append(artistID)
			
			for artist in getRelatedArtists(artistID):
				networkTuple.append((artistID,artist))
				networkList[0].append(artist)			
		else:		
			for index in range(0,len(networkList[d-2])):  
				tempList = getRelatedArtists(networkList[d-2][index])  #get all the related artists for each artist in this layer
				for artist in tempList: #find for every artists pair, if there is already a tie
					#print "I am working"
					if not CheckAlreadyThere(networkList[d-2][index],artist):
						networkTuple.append((networkList[d-2][index],artist))
						networkList[d-1].append(artist)
	return networkTuple


def getRelatedArtists(artistID):
	url = "https://api.spotify.com/v1/artists/"+artistID+"/related-artists"
	r=requests.get(url)
	data = r.json()

	relatedAritstsList =[]
	for artist in data['artists']:
		relatedAritstsList.append(artist['id'])
		
	return relatedAritstsList


def getEdgeList(artistID, depth):
	depthEdges = getDepthEdges(artistID, depth)  #get tuples of edges
	return pd.DataFrame(depthEdges)


def writeEdgeList(artistID, depth, filename):
	edgeData = getEdgeList(artistID,depth)
	edgeData.to_csv(filename,index=False)
	print "writting out successfully to the file: %s" % filename

#getRelatedArtists('2mAFHYBasVVtMekMUkRO9g')
#print len(getDepthEdges('2mAFHYBasVVtMekMUkRO9g',1))
#print getEdgeList('2mAFHYBasVVtMekMUkRO9g',2)

#writeEdgeList('2mAFHYBasVVtMekMUkRO9g',2,'F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\edgeData.csv')