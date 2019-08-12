import PIL.Image
import PIL.ImageTk
from tkinter import *
import requests
from PIL import Image, ImageTk
import io
import ctypes
from collections import deque
profileQue = deque([None] * 2)
photos = []


def expand_Window():
    #location = '200x200+' + str(root.winfo_x()+300) + '+' + str(root.winfo_y())
    root.geometry('600x185')


#returns link to full size steam pfp
def getSteamPFP(id):
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=12A1D1DE83F9932934EDD6DF2BA00463&steamids=' + id
    steamProfile = requests.get(url)
    steamPFP = steamProfile.json().get('response')
    steamPFP = steamPFP['players'][0].get('avatarmedium')
    return(steamPFP)


#function to get users steam id
def getSteamID(search):
    # search custom steam id
    url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=12A1D1DE83F9932934EDD6DF2BA00463&vanityurl=' + search

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

        #steam profile is private
        if not profile:

            printInfo('', getSteamPFP(steamID), profile)
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, 'Profile is private!', 'Alert', 0)

        #steam profile is public
        if profile:
            print(profile.json())
            allStats = profile.json().get('playerstats')
            title = allStats['stats'][0].get('name')
            data = allStats['stats'][0].get('value')
            temp = title + ': ' + str(data)
            print(allStats['stats'][0])
            printInfo(temp, getSteamPFP(steamID), profile)
    else:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Enter a Valid Steam ID', 'Alert', 0)

    return 0


def printInfo(info, image_url, status):

    global profileQue
    global photos


    infoBox.config(state='normal')
    tempInfoBox = Canvas(infoBox, bd=0, highlightthickness=0, relief='ridge', bg='green', width=280, height=64)


    #print pfp and 'PRIVATE' text
    if not status:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))
        ph = PIL.ImageTk.PhotoImage(img)
        photos.append(ph)
        tempInfoBox.create_image(0, 0, image=photos[-1], anchor=NW)
        tempInfoBox.create_text(165, 30, text="PRIVATE", fill='yellow', font=('', 12))

    #print pfp and stats
    if status:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))
        ph = PIL.ImageTk.PhotoImage(img)
        photos.append(ph)
        tempInfoBox.create_image(0, 0, image=photos[-1], anchor=NW)
        tempInfoBox.create_text(165, 30, text=info, fill='yellow', font=('', 12))


    #create & add created text widget to que, delete old
    infoBox.window_create('1.0', window=tempInfoBox)
    profileQue.append(tempInfoBox)
    old = profileQue.popleft()
    if old != None:
        infoBox.delete(old)

    infoBox.config(state='disabled')
    return 0


#function to get string from searchbar
def getInput(event):
    global searchbar
    string = searchbar.get()
    if string and len(string) < 33:
       getSteamID(string)

    elif string and len(string) > 32:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Invalid Steam ID, must be 32 characters or less', 'Alert', 0)

    else:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Enter a Steam ID', 'Alert', 0)


#create Tkinter UI
root = Tk()
root.geometry("290x185")
#root.resizable(0, 0)
root.config(bg='grey20')

#Create 3 Frames
titleFrame = Frame(root, bg="#111111")
titleFrame.grid(row=0)

bodyFrame = Frame(root, bg="red")
bodyFrame.grid(row=1)

bottomFrame = Frame(root, bg='green')
bottomFrame.grid(row=2)

#Top Frame
searchLabel = Label(titleFrame, text = "Search: ", bg = '#111111', fg='grey90', relief = 'solid', bd=-1)
searchLabel.grid(row=0, column=0)

searchbar = Entry(titleFrame, width = 33, bg='grey40', fg= 'grey90')
searchbar.grid(row=0, column=1)

searchButton = Button(titleFrame, text = 'Go!' ,height=1, width=5, relief = 'raised', bd = 3, bg='green', fg='grey90', cursor='hand2')
searchButton.grid(row=0, column=2)
searchButton.bind('<Button-1>', getInput)
root.bind('<Return>', getInput)

#Body Frame
#canvas = Canvas(bodyFrame, bd=5, bg= 'grey20', cursor = "arrow", highlightthickness=0, width=243, height=100)
#canvas.grid(expand=TRUE,fill=BOTH)
infoBox = Text(bodyFrame, wrap=WORD,height=8, width=35, bd=-1, cursor = "arrow", highlightthickness=0, bg='blue', fg='black')
#canvas.create_window((0, 0), window=infoBox)
infoBox.grid(row=0, column=0, sticky='W')
infoBox.config(state='disabled')

#Bottom Frame
b = Button(bottomFrame, text="Expand window", command=expand_Window, cursor='hand2')
b.grid()


root.mainloop()