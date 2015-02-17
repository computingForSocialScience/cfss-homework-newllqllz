from io import open
import csv

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    
    outFile=open('F:\\cfss\\cfss-homework-newllqllz\\assignment5\\artists.csv','w',encoding='utf-8')

    outFile.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    #writer.writerow(filed_names)  #write the first column
    data=[]
    for item in artist_info_list: 
        #iterate
        tempList = []
        tempList.append(item["id"])
        tempList.append('\"'+item["name"]+'\"')
        tempList.append(item["followers"]["total"])
        tempList.append(item["popularity"])
        data.append((tempList))
        print tempList
        line = tempList[0]+','+tempList[1]+','+str(tempList[2])+','+str(tempList[3])+'\n'
        outFile.write(line)

    outFile.close()

#listdd = [artics_dic,artics_dic]
#writeArtistsTable(listdd)
      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    outFile=open('F:\\cfss\\cfss-homework-newllqllz\\assignment5\\albums.csv','a',encoding='utf-8')  #append to what has been down

    outFile.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    #writer.writerow(filed_names)  #write the first column
    data=[]
    for item in album_info_list: 
        #iterate
        tempList = []
        tempList.append(item["artist_id"])
        tempList.append(item["album_id"])
        tempList.append('\"'+item["name"]+'\"')
        tempList.append(item["year"])
        tempList.append(item["popularity"])
        data.append((tempList))
        print tempList
        line = tempList[0]+','+tempList[1]+','+tempList[2]+','+str(tempList[3])+','+str(tempList[4])+'\n'
        outFile.write(line)

    outFile.close()

#listdd = [al_dic,al_dic]
#writeAlbumsTable(listdd)