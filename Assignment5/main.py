import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    # YOUR CODE HERE
    ArtistIds = []
    ArtistInfos =[]
    AlbumIds =[]
    AlbumInfos =[]
    for name in artist_names:  #get id
    	ArtistIds.append(fetchArtistId(name))
    for artistId in ArtistIds:
    	ArtistInfos.append(fetchArtistInfo(artistId))
    for artistId in ArtistIds:
    	ids = fetchAlbumIds(artistId)
    	for aid in ids:
    		AlbumIds.append(aid)
    for albumId in AlbumIds:
    	AlbumInfos.append(fetchAlbumInfo(albumId))
    writeArtistsTable(ArtistInfos)
    writeAlbumsTable(AlbumInfos)
    plotBarChart()



