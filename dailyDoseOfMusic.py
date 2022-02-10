"""
Get random song from a certain playlist.
Good for querying random daily songs.
"""
from random import randrange
import requests

playlistId = ""  # Playlists ID
token = ""  # Bearer token to query playlist information
apiUri = "https://api.spotify.com/v1"  # Spotify's base api url


def getRandomSong():
    """
    Query all of the playlist's songs.
    Get a randrange integer from the size of the playlist.
    Return the name and the link of the random song from the playlist.
    :return:
    """
    songs = queryAllPlaylistSongs()
    randInt = randrange(0, len(songs) - 1)
    if randInt < 0:
        randInt = 0
    randSong = songs[randInt]
    try:
        trackUrl = randSong['track']['external_urls']['spotify']
    except KeyError:
        trackUrl = "too bad, local song :D"
    artistNameList = []
    for artist in randSong['track']['artists']:
        artistNameList.append(artist['name'])
    artistNameString = ', '.join(artistNameList)
    songName = randSong['track']['name']
    fullName = f"{artistNameString} - {songName} ({trackUrl})"
    return fullName


def queryAllPlaylistSongs():
    """
    Query all of the playlist's songs.
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    songLists = []
    request = requests.get(f"{apiUri}/playlists/{playlistId}/tracks", headers=headers).json()

    while request['next']:
        songLists.append(request['items'])
        request = nextPage(request['next'])
    songLists.append(request['items'])
    actualSongList = []
    for songList in songLists:
        for song in songList:
            actualSongList.append(song)
    return actualSongList


def nextPage(uri):
    """
    Since Spotify does not want to return all of the songs in one request we have to check the next pages as well.
    Beats me why they cant just send all of the data in 1 page...
    :param uri:
    :return:
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {token}"
    }
    request = requests.get(uri, headers=headers).json()
    return request


if __name__ == '__main__':
    print(getRandomSong())
