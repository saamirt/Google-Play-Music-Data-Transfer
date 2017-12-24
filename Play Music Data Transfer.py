from gmusicapi import Mobileclient
import getpass

def getEmail():
    user = input("Enter User/Email: ")
    if not user.endswith("@gmail.com"):
        user = user + "@gmail.com"
    return user

def login(mc):
    while 1:
        logged_in = mc.login(getEmail(),input("Enter Password: "), Mobileclient.FROM_MAC_ADDRESS)
        if not logged_in and mc.is_authenticated:
            print("You messed up, " + getpass.getuser())
            print("Enter valid credentials this time")
            continue
        break
    print("Login Successful\n")

mc = Mobileclient()

#Logging into old account
print("Log into the Play Music account that you want to retrieve songs from")
login(mc)
if not mc.is_subscribed:
    print ("This user is not subscribed")
    print ("Google Play Music empties playlists while a user is unsubscribed")
    print ("Therefore playlists transferred over will be empty\n")

songs = mc.get_all_songs()
playlists = mc.get_all_user_playlist_contents()
#radios = mc.get_all_stations()
#podcasts = mc.get_all_podcast_series()

print("I've found " + str(len(songs)) + " songs in your library")
print("I've found " + str(len(playlists)) + " user playlists in your library")
#print("I've found " + str(len(radios)) + " radios in your library")
#print("I've found " + str(len(podcasts)) + " podcasts in your library")

mc.logout()
print("Logged Out\n")

#Logging into new account
print("Log into the Play Music account that you want to transfer songs to")

while 1:
    login(mc)
    if not mc.is_subscribed:
        print("This account is not subscribed")
        print("Please log in with a subscribed account\n")
        mc.logout()
        continue
    break

#Adding songs
if songs:
    mc.add_store_tracks(list(i['storeId'] for i in songs))

#Adding playlists
if playlists:
    already_created_playlists = [i['name'] for i in mc.get_all_user_playlist_contents()]
    for i in playlists:
        name = i['name']
        suffix = ""
        num = 0
        while ((name + suffix) in already_created_playlists):
            num += 1
            suffix = " (" + str(num) + ")"
        name = name + suffix
        mc.add_songs_to_playlist(mc.create_playlist(name,i['description']),[j['trackId'] for j in i['tracks']])

mc.logout()

print("Songs and playlists have been transfered!")
