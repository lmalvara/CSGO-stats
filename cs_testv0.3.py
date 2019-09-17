import PIL.Image
import PIL.ImageTk
from tkinter import *
import requests
from PIL import Image
import io
import ctypes
from collections import deque
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

profileQue = deque([None] * 2)
photos = []
graph = []
#name, kills, death, plant, defuses, winrate, hours
profileInfo = deque([None] * 2)


#add or remove left widget from grid
def moreStats_left(status):
    global profileInfo
    if status and profileInfo[1] != None:
        stats = profileInfo[1]
        print("UMM: ", stats)
        message = "Profile: " + stats[0] + "\nTotal Kills: " + str(stats[1]) + "\nTotal Deaths: " + str(stats[2]) + "\nBombs Planted: " + str(stats[3]) + "\nBombs Defused: " + str(stats[4]) + "\nWinrate: " + str(stats[5]*100) + "%" + "\nTotal Hours Played: " + str(stats[6])
        bonusStats_first.config(state='normal')
        bonusStats_first.delete('1.0', END)
        bonusStats_first.insert('1.0', message)
        bonusStats_first.grid(row=0,column=0, sticky='E', padx=2, pady=2)
        bonusStats_first.config(state='disabled')
    elif not status:
        bonusStats_first.grid_remove()


#add or remove right widget from grid
def moreStats_right(status):
    global profileInfo
    if status and profileInfo[0] != None:
        stats = profileInfo[0]
        message = "Profile: " + stats[0] + "\nTotal Kills: " + str(stats[1]) + "\nTotal Deaths: " + str(stats[2]) + "\nBombs Planted: " + str(stats[3]) + "\nBombs Defused: " + str(stats[4]) + "\nWinrate: " + str(stats[5] * 100) + "%" + "\nTotal Hours Played: " + str(stats[6])
        bonusStats_sec.config(state='normal')
        bonusStats_sec.delete('1.0', END)
        bonusStats_sec.insert('1.0', message)
        bonusStats_sec.grid(row=0,column=2, sticky='E', padx=2, pady=2)
        bonusStats_sec.config(state='disabled')
    elif not status:
        bonusStats_sec.grid_remove()


#add or remove graph widget from grid
def moreStats_graph(status):
    global profileInfo
    global graph
    print(profileInfo, "UHUHH")
    if status:
        labels = ['K/D', 'Bomb Plant', 'Defuse', 'Win %', 'Hours']
        player_One = [round(profileInfo[0][1] / profileInfo[0][2], 2), profileInfo[0][3], profileInfo[0][4], profileInfo[0][5], profileInfo[0][6]]
        player_Two = [round(profileInfo[1][1] / profileInfo[1][2], 2), profileInfo[1][3], profileInfo[1][4], profileInfo[1][5], profileInfo[1][6]]

        x = np.arange(len(labels))
        width = .4
        fig, ax = plt.subplots(figsize=(4.8,3.2))
        rects1 = ax.bar(x - width / 2, player_One, width, label=profileInfo[0][0])
        rects2 = ax.bar(x + width / 2, player_Two, width, label=profileInfo[1][0])

        ax.set_ylabel('')
        ax.set_title('Stats')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords = "offset points", ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, bonusStats_graph)
        graph = canvas
        canvas.get_tk_widget().grid()
        bonusStats_graph.grid(row=1, columnspan =4, pady=1)
    else:
        graph.get_tk_widget().destroy()
        bonusStats_graph.grid_remove()


#expand/colapse graph window
def expand_close_graph():
    if 'Show' in details_graph.get():
        if '+' in details_first.get() and '+' in details_second.get():
            root.geometry('480x572')
            details_graph.set("Close Graph")
            moreStats_graph(1)
        elif '-' in details_first.get() and '-' in details_second.get():
            root.geometry('851x572')
            details_graph.set("Close Graph")
            moreStats_graph(1)
        else:
            root.geometry('568x572')
            details_graph.set("Close Graph")
            moreStats_graph(1)

    elif 'Close' in details_graph.get():
        if '+' in details_first.get() and '+' in details_second.get():
            root.geometry('290x250')
            details_graph.set("Show Graph")
            moreStats_graph(0)
        elif '-' in details_first.get() and '-' in details_second.get():
            root.geometry('851x250')
            details_graph.set("Show Graph")
            moreStats_graph(0)
        else:
            root.geometry('568x250')
            details_graph.set("Show Graph")
            moreStats_graph(0)


#expand/colapse left window
def expand_close_window_first():
    #expand left side
    if '+' in details_first.get() and '+' in details_second.get():
        if 'Show' in details_graph.get():
            root.geometry('568x250')
        else:
            root.geometry('568x572')
        details_first.set('Left -')
        moreStats_left(1)

    #colapse left side
    elif '-' in details_first.get() and '-' in details_second.get():
        if 'Show' in details_graph.get():
            root.geometry('568x250')
        else:
            root.geometry("568x572")
        details_first.set('Left +')
        moreStats_left(0)
    elif '-' in details_first.get():
        if 'Show' in details_graph.get():
            root.geometry('290x250')
        else:
            root.geometry("480x572")
        details_first.set('Left +')
        moreStats_left(0)
    elif '+' in details_first.get():
        if 'Show' in details_graph.get():
            root.geometry("851x250")
        else:
            root.geometry("851x572")
        details_first.set('Left -')
        moreStats_left(1)


#expand/colapse right window
def expand_close_window_sec():
    #expand right side
    if '+' in details_first.get() and '+' in details_second.get():
        if 'Show' in details_graph.get():
            root.geometry('568x250')
        else:
            root.geometry('568x572')
        details_second.set('Right -')
        moreStats_right(1)

    #colapse left side
    elif '-' in details_first.get() and '-' in details_second.get():
        if 'Show' in details_graph.get():
            root.geometry('568x250')
        else:
            root.geometry("568x572")
        details_second.set('Right +')
        moreStats_right(0)
    elif '-' in details_second.get():
        if 'Show' in details_graph.get():
            root.geometry('290x250')
        else:
            root.geometry("480x572")
        details_second.set('Right +')
        moreStats_right(0)
    elif '+' in details_second.get():
        if 'Show' in details_graph.get():
            root.geometry("851x250")
        else:
            root.geometry("851x572")
        details_second.set('Left -')
        moreStats_right(1)


#returns link to full size steam pfp
def getSteamPFP(id):
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=12A1D1DE83F9932934EDD6DF2BA00463&steamids=' + id
    steamProfile = requests.get(url)
    steamPFP = steamProfile.json().get('response')
    steamPFP = steamPFP['players'][0].get('avatarmedium')
    return(steamPFP)


#function to get users steam id
def getSteamID(search):
    global profileInfo
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
            MessageBox(None, 'Profile is private!', 'Alert!', 0)

            profileInfo.append(None)
            profileInfo.popleft()

        #steam profile is public
        if profile:
            print(profile.json())
            allStats = profile.json().get('playerstats')

            kills = allStats['stats'][0].get('value')
            deaths = allStats['stats'][1].get('value')
            plant = allStats['stats'][3].get('value')
            defuse = allStats['stats'][4].get('value')
            winrate = round(allStats['stats'][5].get('value') / allStats['stats'][45].get('value'), 2)
            time = round(allStats['stats'][2].get('value')/3600)

            mini_message = search + ": \nK/D: " + str(round(kills/deaths, 2)) +"\nWinrate: " + str(winrate) + "\n" + str(time) + " hours Played"

            #send player_stats which contains the keys statistics
            player_stats = [search, kills, deaths, plant, defuse, winrate, time]

            profileInfo.append(player_stats)
            profileInfo.popleft()


            #print(allStats['stats'][0])
            printInfo(mini_message, getSteamPFP(steamID), player_stats)
    else:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Enter a Valid Steam ID.', 'Alert!', 0)

    return 0


#called from getSteamID to print
def printInfo(info, image_url, status):

    global profileQue
    global photos

    infoBox.config(state='normal')
    tempInfoBox = Canvas(infoBox, bd=0, highlightthickness=0, relief='ridge', bg='green', width=280, height=100)

    #print pfp and 'PRIVATE' text
    if not status:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))
        ph = PIL.ImageTk.PhotoImage(img)
        photos.append(ph)
        tempInfoBox.create_image(0, 12, image=photos[-1], anchor=NW)
        tempInfoBox.create_text(150, 45, text="PRIVATE", fill='yellow', font=('', 12))

    #print pfp and stats
    if status:
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content))
        ph = PIL.ImageTk.PhotoImage(img)
        photos.append(ph)
        tempInfoBox.create_image(0, 12, image=photos[-1], anchor=NW)
        tempInfoBox.create_text(150, 45, text=info, fill='yellow', font=('', 12))

    #create & add created text widget to que, delete old
    infoBox.window_create('1.0', window=tempInfoBox)
    profileQue.append(tempInfoBox)
    old = profileQue.popleft()
    if old != None:
        infoBox.delete(old)

    #enable/disable extra stats button depending on if stats are in queue
    if profileInfo[0] != None and profileInfo[1] != None:
        b1.config(state='normal')
        b2.config(state='normal')
        b3.config(state='normal')
    if profileInfo[0] != None and profileInfo[1] == None:
        b1.config(state='disabled')
        b2.config(state='disabled')
        b3.config(state='normal')
    if profileInfo[0] == None and profileInfo[1] == None:
        b1.config(state='disabled')
        b2.config(state='disabled')
        b3.config(state='disabled')
    if profileInfo[0] == None and profileInfo[1] != None:
        b1.config(state='normal')
        b2.config(state='disabled')
        b3.config(state='disabled')


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
        MessageBox(None, 'Invalid Steam ID, must be 32 characters or less.', 'Alert!', 0)

    else:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Enter a Steam ID.', 'Alert!', 0)


#create Tkinter UI
root = Tk()
root.geometry("290x250")
#root.resizable(0, 0)
root.config(bg='grey20')

#Create 3 Frames
titleFrame = Frame(root, bg="grey15")
titleFrame.grid(row=0, sticky="nsew")
titleFrame.grid_rowconfigure(0, weight=1)
titleFrame.grid_columnconfigure((0,3), weight=1)

bodyFrame = Frame(root, bg="grey20")
bodyFrame.grid(row=1)
bodyFrame.grid_columnconfigure((0,2), weight=1)


bottomFrame = Frame(root)
bottomFrame.grid(row=2)

#Top Frame
searchLabel = Label(titleFrame, text = "Search: ", bg = 'grey15', fg='grey90', relief = 'solid', bd=-1)
searchLabel.grid(row=0, column=0, sticky='e')

searchbar = Entry(titleFrame, width = 33, bg='grey40', fg= 'grey90')
searchbar.grid(row=0, column=1)

searchButton = Button(titleFrame, text = 'Go!' ,height=1, width=5, bd = 3, bg='green', fg='grey90', cursor='hand2')
searchButton.grid(row=0, column=2)
searchButton.bind('<Button-1>', getInput)
root.bind('<Return>', getInput)

#Body Frame
infoBox = Text(bodyFrame, wrap=WORD,height=12, width=35, bd=-1, cursor = "arrow", highlightthickness=0, bg='blue', fg='black')
infoBox.grid(row=0, column=1, pady=2)
infoBox.config(state='disabled')

#create the text boxes to be later inserted when called for
bonusStats_first = Text(bodyFrame, wrap=WORD, height=12, width=35, bd=-1, cursor="arrow", highlightthickness=0, bg='green', fg='black')
bonusStats_sec = Text(bodyFrame, wrap=WORD, height=12, width=35, bd=-1, cursor="arrow", highlightthickness=0, bg='red', fg='black')
bonusStats_graph = Canvas(bodyFrame, height=320, width=482, bd=-1, cursor="arrow", highlightthickness=0, bg='yellow')
bonusStats_first.config(state='disabled')
bonusStats_sec.config(state='disabled')
bonusStats_graph.config(state='normal')

#Bottom Frame
details_first = StringVar()
b1 = Button(bottomFrame, textvariable=details_first, command=expand_close_window_first, cursor='hand2', bg='green', fg='grey90', activebackground='green')
details_first.set('Left +')
b1.grid(row=0, column=0, sticky='w')
b1.config(state='disabled')

details_graph = StringVar()
b2 = Button(bottomFrame, textvariable=details_graph, command=expand_close_graph, cursor='hand2', bg='yellow', activebackground='yellow')
details_graph.set("Show Graph")
b2.grid(row=0,column=1)
b2.config(state='disabled')

details_second = StringVar()
b3 = Button(bottomFrame, textvariable=details_second, command=expand_close_window_sec, cursor='hand2', bg='red', fg='grey90', activebackground='red')
details_second.set('Right +')
b3.grid(row=0, column=2, sticky='e')
b3.config(state='disabled')


root.mainloop()
