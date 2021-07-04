import matplotlib
import requests
from matplotlib.backends.backend_tkagg \
    import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkinter import messagebox as tkMessageBox, messagebox

matplotlib.use("TkAgg")
from tkinter import *

virus = Tk()
virus.title("Covid-19 Data Graphing Program")
virus.iconbitmap('covid19.ico')
virus.geometry("1280x720")

url = "https://api.covid19api.com/countries"
daily = "https://api.covid19api.com/total/dayone/country/"
summary = "https://api.covid19api.com/total/country/"
answer = requests.get(url)
result = answer.json()
lblength = len(result)

lbcountry = Label(virus, text="Countries", font="Arial")
lbcountry.pack(side="top")
lbcountry.place(x=63, y=0)

lbdata = Label(virus, text="Data Selection", font="Arial")
lbdata.pack(side="left")
lbdata.place(x=48, y=380)

countryInfo = []

lb1 = Listbox(virus, width=30, height=19, selectmode=SINGLE, exportselection=0, bg="#aaff00")
lb1.pack(side="left")
lb1.place(x=0, y=25)

for i in range(0, lblength):
    countryInfo.insert(i, result[i]["Slug"])
    lb1.insert(i, result[i]["Country"])

lb2 = Listbox(virus, width=30, height=9, selectmode=SINGLE, exportselection=0, fg="black", bg="#f236ff")
lb2.insert(0, "Confirmed")
lb2.insert(1, "Deaths")
lb2.insert(2, "Recovered")
lb2.insert(3, "Active")
lb2.insert(4, "Confirmed-Daily")
lb2.insert(5, "Deaths-Daily")
lb2.insert(6, "Recovered-Daily")
lb2.insert(7, "Active-Daily")
lb2.pack(side="left")
lb2.place(x=0, y=405)


def countryQuery(entry):
    url = 'https://covid-193.p.rapidapi.com/statistics'
    key = 'f511081e15msh908b491eabf7e58p1a20eejsn8dd4b50f0d1e'
    query = {"country": entry}
    params = {"country": entry}

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "f511081e15msh908b491eabf7e58p1a20eejsn8dd4b50f0d1e"
    }
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    """ print (result)
	print (result['response'][0]['country'])
	print (result['response'][0]['cases']['new'])
	print (result['response'][0]['cases']['active'])
	print (result['response'][0]['cases']['critical'])
	print (result['response'][0]['cases']['recovered'])
	print (result['response'][0]['cases']['total'])
	print (result['response'][0]['deaths']['new'])
	print (result['response'][0]['deaths']['total'])
	print (result['response'][0]['tests']['total'])
	print (result['response'][0]['day'])
	print (result['response'][0]['time']) """
    try:
        country = result['response'][0]['country']
        new = result['response'][0]['cases']['new']
        active = result['response'][0]['cases']['active']
        critical = result['response'][0]['cases']['critical']
        recovered = result['response'][0]['cases']['recovered']
        total = result['response'][0]['cases']['total']

        newD = result['response'][0]['deaths']['new']
        totalD = result['response'][0]['deaths']['total']

        numTest = result['response'][0]['tests']['total']

        time = result['response'][0]['time']

        resultString = 'Country Name: %s \n\nNew Cases: %s \nNew Deaths: %s \nActive Cases: %s \nCritical Cases: %s \nRecovered: %s \n\nTotal Cases: %s \nTotal Deaths: %s \nTotal Number of Tests: %s \n\nDate: %s' % (
            country, new, active, critical, recovered, total, newD, totalD, numTest, time)
        lbl1['text'] = resultString
    except:
        resultString = "!!! PLEASE ENTER\n THE NAME OF THE COUNTRY\n YOU WANT THE DATA\n OF IN ENGLISH !!!"
        lbl1['text'] = resultString


canvas = Canvas(virus, height=500, width=600)
canvas.pack()
entryText = StringVar()
entry = Entry(virus, font=('Arial', 12), textvariable=entryText, justify='center')
entry.place(x=1080, y=55)
entryText.set("Please enter country name")

dataButton = Button(virus, text="Verileri Getir", fg="white", bg="red", relief=GROOVE,
                    command=lambda: countryQuery(entry.get()))
dataButton.place(x=1138, y=90)

lbl1 = Label(virus, justify='left', width=26, height=13, fg="black", bg="#b5bbf4")
lbl1.pack(side="right")
lbl1.place(x=1080, y=127)


def confirmed():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(summary + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(0, len(result2)):
        xLine.append(j)

    for k in range(0, len(result2)):
        yLine.insert(k, result2[k]["Confirmed"])

    x = np.array(xLine)
    y = np.array(yLine)
    confirmed = f.add_subplot(111)
    confirmed.set_title(lb1.get(ACTIVE), fontsize=12)
    confirmed.set_xlabel("Day", fontsize=9)
    confirmed.set_ylabel("Number of Confirmed Cases", fontsize=9)
    confirmed.bar(x, y, color='orange', label="Confirmed Cases")
    confirmed.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def deaths():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(summary + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(0, len(result2)):
        xLine.append(j)

    for k in range(0, len(result2)):
        yLine.insert(k, result2[k]["Deaths"])

    x = np.array(xLine)
    y = np.array(yLine)
    deaths = f.add_subplot(111)
    deaths.set_title(lb1.get(ACTIVE), fontsize=12)
    deaths.set_xlabel("Day", fontsize=9)
    deaths.set_ylabel("Number of Deaths", fontsize=9)
    deaths.bar(x, y, color='red', label="Deaths")
    deaths.legend(facecolor='gray', shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def recovering():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(summary + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(0, len(result2)):
        xLine.append(j)

    for k in range(0, len(result2)):
        yLine.insert(k, result2[k]["Recovered"])

    x = np.array(xLine)
    y = np.array(yLine)
    recovering = f.add_subplot(111)
    recovering.set_title(lb1.get(ACTIVE), fontsize=12)
    recovering.set_xlabel("Day", fontsize=9)
    recovering.set_ylabel("Number of Recovering", fontsize=9)
    recovering.bar(x, y, color='green', label="Recovering")
    recovering.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def active():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(summary + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(0, len(result2)):
        xLine.append(j)

    for k in range(0, len(result2)):
        yLine.insert(k, result2[k]["Active"])

    x = np.array(xLine)
    y = np.array(yLine)
    active = f.add_subplot(111)
    active.set_title(lb1.get(ACTIVE), fontsize=12)
    active.set_xlabel("Day", fontsize=9)
    active.set_ylabel("Number of Active", fontsize=9)
    active.bar(x, y, color='purple', label="Active")
    active.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def dailyConfirmed():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(daily + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(1, len(result2)):
        xLine.append(j)

    for k in range(1, len(result2)):
        yLine.insert(k, (result2[k]["Confirmed"] - result2[k - 1]["Confirmed"]))

    x = np.array(xLine)
    y = np.array(yLine)
    dailyConfirmed = f.add_subplot(111)
    dailyConfirmed.set_title(lb1.get(ACTIVE), fontsize=12)
    dailyConfirmed.set_xlabel("Day", fontsize=9)
    dailyConfirmed.set_ylabel("Number of Daily Confirmed", fontsize=9)
    dailyConfirmed.plot(x, y, color='orange', label="Daily Confirmed Case")
    dailyConfirmed.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def dailyDeath():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(daily + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(1, len(result2)):
        xLine.append(j)

    for k in range(1, len(result2)):
        yLine.insert(k, (result2[k]["Deaths"] - result2[k - 1]["Deaths"]))

    x = np.array(xLine)
    y = np.array(yLine)
    dailyDeath = f.add_subplot(111)
    dailyDeath.set_title(lb1.get(ACTIVE), fontsize=12)
    dailyDeath.set_xlabel("Day", fontsize=9)
    dailyDeath.set_ylabel("Number of Daily Death", fontsize=9)
    dailyDeath.plot(x, y, color='red', label="Deaths")
    dailyDeath.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def dailyRecovered():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(daily + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(1, len(result2)):
        xLine.append(j)

    for k in range(1, len(result2)):
        yLine.insert(k, (result2[k]["Recovered"] - result2[k - 1]["Recovered"]))

    x = np.array(xLine)
    y = np.array(yLine)
    dailyRecovered = f.add_subplot(111)
    dailyRecovered.set_title(lb1.get(ACTIVE), fontsize=12)
    dailyRecovered.set_xlabel("Day", fontsize=9)
    dailyRecovered.set_ylabel("Number of Daily Recovered", fontsize=9)
    dailyRecovered.plot(x, y, color='green', label="Recovered")
    dailyRecovered.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def dailyActive():
    f = Figure(figsize=(10, 8), dpi=80)
    sorting = lb1.get(0, "end").index(lb1.get(ACTIVE))
    answer2 = requests.get(daily + countryInfo[sorting])
    result2 = answer2.json()

    xLine = []
    yLine = []

    for j in range(1, len(result2)):
        xLine.append(j)

    for k in range(1, len(result2)):
        yLine.insert(k, (result2[k]["Active"] - result2[k - 1]["Active"]))

    x = np.array(xLine)
    y = np.array(yLine)
    dailyActive = f.add_subplot(111)
    dailyActive.set_title(lb1.get(ACTIVE), fontsize=12)
    dailyActive.set_xlabel("Day", fontsize=9)
    dailyActive.set_ylabel("Number of Daily Active", fontsize=9)
    dailyActive.plot(x, y, color='purple', label="Daily Active")
    dailyActive.legend(shadow='true')
    canvas = FigureCanvasTkAgg(f, master=virus)
    canvas.get_tk_widget().place(x=200, y=50)


def draw():
    try:
        if lb2.get(ACTIVE) == "Confirmed":
            confirmed()
        elif lb2.get(ACTIVE) == "Deaths":
            deaths()
        elif lb2.get(ACTIVE) == "Recovered":
            recovering()
        elif lb2.get(ACTIVE) == "Active":
            active()
        elif lb2.get(ACTIVE) == "Confirmed-Daily":
            dailyConfirmed()
        elif lb2.get(ACTIVE) == "Deaths-Daily":
            dailyDeath()
        elif lb2.get(ACTIVE) == "Recovered-Daily":
            dailyRecovered()
        elif lb2.get(ACTIVE) == "Active-Daily":
            dailyActive()
    except:
        print("Select The Graphic")
        tkMessageBox.showerror(title="ERROR", message="Select The Graphic")


drawButton = Button(virus, text="Draw The Graph", width=25, fg="white", bg="black", command=draw)
drawButton.pack(side="left")
drawButton.place(x=0, y=555)


virus.mainloop()
