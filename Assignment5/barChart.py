import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('F:\\cfss\\cfss-homework-newllqllz\\assignment5\\artists.csv')
    f_albums = open('F:\\cfss\\cfss-homework-newllqllz\\assignment5\\albums.csv')  #open file

    artists_rows = csv.reader(f_artists)  #csv reader reads file in row
    albums_rows = csv.reader(f_albums)

    artists_header = artists_rows.next()  # get the header 
    albums_header = albums_rows.next()

    artist_names = []  #list of artist_names
    
    decades = range(1900,2020, 10)  #generate a range of number from 1900 to 2000 with interval 10
    decade_dict = {}  #dic for counting
    for decade in decades:
        decade_dict[decade] = 0    # initialization
    
    for artist_row in artists_rows:  # iterate to get all the names
        if not artist_row:  # check if this row is the head row
            continue
        artist_id,name,followers, popularity = artist_row   # get value
        artist_names.append(name) # add name to list

    for album_row  in albums_rows: #iterate to count number of albums by decades
        if not album_row: # should not be the head row
            continue
        artist_id, album_id, album_name, year, popularity = album_row  #get values from a row
        for decade in decades: #iterate all the decades
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):  # check if in that decade
                decade_dict[decade] += 1  # if so, count 
                break

    x_values = decades  #get a list of decades
    y_values = [decade_dict[d] for d in decades] #get a list of corresponding numbers of albums in each decade
    return x_values, y_values, artist_names

def plotBarChart():  # get data from getBarcharData and plot
    x_vals, y_vals, artist_names = getBarChartData()  #get data
    
    fig , ax = plt.subplots(1,1)   # layout
    ax.bar(x_vals, y_vals, width=10) #plot as barchart
    ax.set_xlabel('decades') #set the xlabel
    ax.set_ylabel('number of albums') #set the ylabel
    ax.set_title('Totals for ' + ', '.join(artist_names))  #set the title
    plt.show()  #show the graph


    
#plotBarChart()