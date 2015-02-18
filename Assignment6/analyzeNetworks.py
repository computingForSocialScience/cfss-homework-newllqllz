import sys
import requests
import csv
import pandas as pd
import numpy as np
import networkx as nx

def readEdgeList(filename):
	edgeData = pd.read_csv(filename)
	#print edgeData
	#print type(edgeData)
	if edgeData.columns.size>2:
		edgeData = edgeData.ix[:,:2]
	return edgeData

def degree(edgeList, in_or_out):
	if in_or_out =='in':
		print edgeList['1'].value_counts()
	elif in_or_out=='out':
		print edgeList['0'].value_counts()
	else:
		print "Parameters wrong, you should type in either 'in' or 'out' "

def combineEdgelists(edgeList1, edgeList2):
	edgeList = edgeList1.append(edgeList2)
	edgeList = edgeList.drop_duplicates()
	return edgeList

def pandasToNetworkX(edgeList):
	edgeRecords = edgeList.to_records(index=False) #list-like object containing tuples
	#print edgeRecords
	G = nx.DiGraph()
	for sender,receiver in edgeRecords:
		G.add_edge(sender,receiver,count=1)
	#print len(G.nodes())
	return G
	
def randomCentralNode(inputDiGraph):  #choose a random point based on the centrality
	originalDic =  nx.eigenvector_centrality(inputDiGraph)  
	SumOfCentraility = 0.0
	TempCList = originalDic.values()
	nc_dict={}
	for x in TempCList:
		SumOfCentraility +=x
	for key in originalDic.keys():
		nc_dict[key] = (originalDic[key])/SumOfCentraility
	#print "SumOfCentraility is %d" % SumOfCentraility
	#print nc_dict.values()
	point = np.random.choice(nc_dict.keys(), p=nc_dict.values())
	return point

#degree(readEdgeList("F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\edgeData.csv"),'out')
#pandasToNetworkX(readEdgeList("F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\edgeData.csv"))
#randomCentralNode(pandasToNetworkX(readEdgeList("F:\\cfss\\cfss-homework-newllqllz\\Assignment6\\edgeData.csv")))