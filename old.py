import requests
from tkinter import *
import ctypes
from collections import deque

profile = deque([None] * 2)

#function to get users steam id
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
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Enter a Valid Steam ID', 'Alert', 0)

    return 0

#function to get string from searchbar
def getInput(event):
    global searchbar
    string = searchbar.get()
    if string and len(string) < 33:
       getSteamID(string)
    else:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Enter a Valid Steam ID', 'Alert', 0)



root = Tk()
root.geometry("254x164")
#root.resizable(0, 0)

#Create 3 Frames
titleFrame = Frame(root, bg="#111111")
titleFrame.grid(row=0, sticky='N, E, S, W')

bodyFrame = Frame(root, bg="#111111")
bodyFrame.grid(row=1, sticky='N, E, S, W')

bottomFrame = Frame(root, bg='#111111')
bottomFrame.grid(row=2, sticky='N, E, S, W')

#Top Frame
searchLabel = Label(titleFrame, text = "Search: ", bg = 'grey20', fg='grey90', relief = 'raised')
searchLabel.grid(row=0, column = 1, sticky='N, E, S, W')

searchbar = Entry(titleFrame, width = 26, bg='grey40', fg= 'grey90')
searchbar.grid(row=0, column = 2, sticky='N, E, S, W')

searchButton = Button(titleFrame, text = 'Go!' ,height=1, width=5, relief = 'raised', bd = 3, bg='green', fg='grey90')
searchButton.grid(row=0, column = 3, sticky='E')
searchButton.bind('<Button-1>', getInput)
root.bind('<Return>', getInput)

#Body Frame
infoBox = Canvas(bodyFrame, bd=5, bg= 'grey20', cursor = "arrow", highlightthickness=0, relief='ridge', width=243, height=100)
infoBox.grid(row=0, sticky='N, E, S, W')
infoBox.config(state='disabled')

#Bottom Frame
expandButton1 = Button(bottomFrame,text='left', width = 5)
expandButton1.grid(row = 0, column = 1, sticky = "W")
expandButton2 = Button(bottomFrame, text = 'center', width = 22)
expandButton2.grid(row = 0, column = 2, sticky = 'N, E, S, W')
expandButton3 = Button(bottomFrame, text = 'right', width = 5)
expandButton3.grid(row = 0, column = 3, sticky = "E")
root.mainloop()