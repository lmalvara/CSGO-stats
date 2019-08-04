import requests
from tkinter import *
import tkinter as tk
import threading

def getSteamID(search):
    # search custom steam id
    url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=12A1D1DE83F9932934EDD6DF2BA00463&vanityurl=' + search
    status = False
    r = requests.get(url)
    steamIDRequest = r.json().get('response')

    # check if search is a valid ID
    if steamIDRequest['success'] == 1:
        steamID = steamIDRequest['steamid']
        status = True
    else:
        status = False

    if status:
        url = 'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=12A1D1DE83F9932934EDD6DF2BA00463&steamid=' + steamID
        profile = requests.get(url)
        if not profile:
            print('profile is private!')
        if profile:
            print(profile.json())
            allStats = profile.json().get('playerstats')
            print(allStats['stats'][0])
    else:
        print('invalid username, please try again')

    return 0

root = Tk()
root.geometry("500x400")

titleFrame = Frame(root, bg="#111111")
titleFrame.grid(row=0, sticky='N, E, S, W')

searchbar = Entry(titleFrame)
searchbar.grid(row=2, column = 0, sticky='N, E, S, W')

def getInput():
    string = searchbar.get()
    if string:
       getSteamID(string)
    else:
        print('Enter a steam ID')

searchButton = Button(titleFrame, text = 'Search' ,height=1, width=6)
searchButton.grid(row=2, column = 1, sticky='E')
searchButton.config(command = getInput)
getInput()

root.mainloop()
