"""
Get random song from a certain playlist.
Good for querying random daily songs.
https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/ used for token query
https://developer.spotify.com/documentation/general/guides/authorization/app-settings/ used to create client/secret id
"""
from random import randrange
import requests
import base64

playlistId = ""  # Playlists ID
apiUri = "https://api.spotify.com/v1"  # Spotify's base api url
clientId = ""  # Spotify app's client ID
clientSecret = ""  # Spotify app's secret ID


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


def getAccessToken():
    """
    Query access token for playlist request.
    :return:
    """
    authUri = "https://accounts.spotify.com/api/token"
    authString = f'{clientId}:{clientSecret}'
    authToken = base64.b64encode(bytes(authString, encoding='utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {authToken}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    request = requests.post(authUri, data=data, headers=headers).json()
    accessToken = request['access_token']

    return accessToken


if __name__ == '__main__':
    token = getAccessToken()
    print(getRandomSong())
