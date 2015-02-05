import csv
import sys
import math
import Image
import matplotlib.pyplot as plt
import numpy as np


def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below
def get_avg_latlng(data):
    latitude=[]
    longitude=[]
    i=0
    for row in data:
        if row[128]=="" or row[129]=="":
            continue
        latitude.append(float(row[128]))
        longitude.append(float(row[129]))

    #print coordinate

    ave_lati =sum(latitude)/len(latitude)
    ave_longi = sum(longitude)/len(longitude)
    #print ave_longi
    return ave_lati, ave_longi
 


#print len(data[0])  #see where is the coordinate of latitude and longitude
#print data[0][130]  #try printing the latitude and longitude



##3.2
def zip_code_barchart(data):
    dic={}
    for item in data:
        #print item[28]
        for i in range(0,14,1):
            
            if item[28+7*i]!="":
                zip_code = item[28+7*i][0:5]
                if not dic.has_key(zip_code):
                    dic[zip_code]=1
                else:
                    dic[zip_code]=int(dic.get(zip_code))+1
    
    N=range(0,len(dic),1)
    ind = np.arange(85)   
    width = 1 
    #print len(N)
    #print len(dic.values())
    plt.bar(N,dic.values(),width,color='r')
    #plt.pyplot.show()
    plt.ylabel('Frequency')
    plt.title('bar chart of contractor zip codes')
    plt.xticks(ind+width/2.,dic.keys() )
    plt.savefig('f:\\testplot.png')
    plt.show()
    Image.open('f:\\testplot.png').save('f:\\cfss\\cfss-homework-newllqllz\\assignment4\\zip_code_barchart.jpg','JPEG')
    return dic


data = []
data = readCSV("F://cfss/cfss-homework-newllqllz/assignment4/permits_hydepark.csv")
print sys.argv
if len(sys.argv)>1:
	request = sys.argv[1];
	if request=="latlong":
		print "Request accepted, now printing the mean latitude and longitude:"
		print  get_avg_latlng(data)
	elif request=="hist":
		print "Request accepted, now plotting the zip_code_barchart:"
		zip_code_barchart(data)
	else:
		print "Sorry, don't understand your request"




