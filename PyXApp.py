# -*- coding: utf-8 -*-

import requests
import urllib
import json
import datetime
import copy

#The urllib.request module defines functions and classes which help in opening URLs
#(mostly HTTP) in a complex world — basic and digest authentication, redirections, cookies and more.
#json loads -> returns an object from a string representing a json object.
def latestRates(baseCurr,date,symbols): 
    if date is not None and not symbols:
        url = "https://api.fixer.io/"+date+"?base="+baseCurr
        print("not none")
        print("Url Check 1 - "+str(url))
    elif date is not None and symbols:
        print("symbols")
        url = "https://api.fixer.io/"+date+"?base="+baseCurr+"&symbols="+symbols
        print("Url Check 1 - "+str(url))
        symbols=""
    elif symbols:
        print("symbols")
        url = "https://api.fixer.io/latest?base="+baseCurr+"&symbols="+symbols
        print("Url Check 1 - "+str(url))
        symbols=""
    else:
        url = "https://api.fixer.io/latest?base="+baseCurr
        print("Url Check 1 - "+str(url))
        print("none")
    try:
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            print(data)
            
            base = data["base"]
            print(base)
            
            date = data["date"]
            print(date)
            
            rates = data["rates"]
            print(rates)
    except:
        print("An error occurred while attempting to fetch the currency details.")
    
    return rates.items()

def currencyList():
    with urllib.request.urlopen("https://api.fixer.io/latest") as url:
        data = json.loads(url.read().decode())
        rates = data["rates"]
    return rates.keys()
    

import tkinter
from tkinter import messagebox

labels = []
root = tkinter.Tk()
root.title("Forex Rates")
root.geometry("600x500")
app = tkinter.Frame(root)

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = tkinter.Canvas(root)
app = tkinter.Frame(canvas)
canvas.pack(side=tkinter.LEFT)

scrollbar = tkinter.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand = scrollbar.set)
scrollbar.pack(side=tkinter.LEFT, fill='y')
canvas.pack(side="left", fill="both",expand=True)
canvas.create_window((4,4), window=app, anchor="nw")

app.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
monthValue="1"
dayValue = "1"
yearValue = "1111"
currenciesDictionary = dict()
try:
    with open("currencies.csv") as infile:
        for line in infile:
            currenciesDictionary[line.split(',')[0].strip()] = line.split(',')[1].strip()
        infile.closed
except:
    print("An error occurred while attempting to read the file.")
print(currenciesDictionary)
tkvar = tkinter.StringVar(app)
choices = list(currencyList())
choiceList = list()
count = 0
for item in choices:
    choiceList.append(item+" - "+ currenciesDictionary[item])
popupMenu = tkinter.OptionMenu(app,tkvar,*choiceList)
tkinter.Label(app, text="Base Currency").grid(row = 5, column = 4)
popupMenu.grid(row = 6, column =4,sticky="n")

def limitSizeYear(*args):
    value = tkyear.get()
    tkmonth.set("")
    tkday.set("")
    if len(value) > 4: 
        tkyear.set(value[:4])
    elif len(value) == 4 and (int(value)<1999):
        tkyear.set("1999")
    global yearValue
    yearValue = tkyear.get()
    
tkyear = tkinter.StringVar(app)
tkyear.trace('w', limitSizeYear)
tkinter.Label(app, text="Year(YYYY)").grid(row = 5, column = 5)
year = tkinter.Entry(app,width=10, textvariable = tkyear).grid(row = 6, column =5,sticky="n")

def limitSizeMonth(*args):
    value = tkmonth.get()
    global monthValue 
    monthValue = copy.deepcopy(value)
    tkday.set("")
    if len(value) > 2:
        tkmonth.set(value[:2])
        monthValue = copy.deepcopy(value[:2])
    elif len(value) == 2 and (int(value) > 12):
        tkmonth.set("12")
        monthValue = "12"    
        
tkmonth = tkinter.StringVar(app)
tkmonth.trace('w', limitSizeMonth)
tkinter.Label(app, text="Month(MM)").grid(row = 5, column = 6)
month = tkinter.Entry(app,width=10, textvariable = tkmonth).grid(row = 6, column =6,sticky="n")

def limitSizeDay(*args):
    #print(monthValue)
    value = tkday.get()
    if len(value) > 2:
        tkday.set(value[:2])
    elif len(value) == 2 and (int(monthValue) == 2) and (int(yearValue)%4 == 0) and (int(value)>29):
        tkday.set("29")
    elif len(value) == 2 and (int(monthValue) == 2) and (int(value)>28):
        tkday.set("28")
    elif len(value) == 2 and (int(monthValue) in [4, 6, 9, 11]) and (int(value) > 30):
        tkday.set("30")
    elif len(value) == 2 and (int(monthValue) in [1,3,5,7,8,10,12]) and (int(value) > 31):
        tkday.set("31")
    elif len(value) == 2 and (not monthValue) and (int(value) > 31):
        tkday.set("31")
        
tkday = tkinter.StringVar(app)
tkday.trace('w', limitSizeDay)
tkinter.Label(app, text="Day(DD)").grid(row = 5, column = 7)
day = tkinter.Entry(app,width=10, textvariable = tkday).grid(row = 6, column =7,sticky="n")


listbox = tkinter.Listbox(app, height=10,width=30,selectmode="multiple")
listbox.grid(column=21,row=6, sticky="nsew")
scrollbarList = tkinter.Scrollbar(listbox, orient="vertical")
listbox.config(yscrollcommand=scrollbarList.set)
scrollbarList.config(command=listbox.yview)

target = currencyList()
tkinter.Label(app, text="Target Currencies").grid(row = 5, column = 21)
#listbox.insert(tkinter.END, "Target Currencies")

for item in target:
    listbox.insert(tkinter.END, item)


values1=""
day=""
month=""
def callback():
    
    for label in labels:
            label.destroy()
    currentDate = datetime.datetime.now()
    
    if not tkvar.get():
        error = "Select a Base Currency to proceed."
        messagebox.showinfo("Error",error)
        return

    if tkyear.get() and currentDate.year < int(tkyear.get()):
        error = "Entered date has to be less than "+ str(currentDate)[0:10]
        messagebox.showinfo("Error",error)
        for label in labels:
            label.destroy()
        return
    elif (tkyear.get() and int(tkyear.get()) == currentDate.year) and tkmonth.get() and (currentDate.month < int(tkmonth.get())):
        error = "Entered date has to be less than "+ str(currentDate)[0:10]
        messagebox.showinfo("Error",error)
        for label in labels:
            label.destroy()
        return
    elif (tkyear.get() and int(tkyear.get()) == currentDate.year) and tkmonth.get() and (int(tkmonth.get()) == currentDate.month) and tkday.get() and (currentDate.day < int(tkday.get())):
        error = "Entered date has to be less than "+ str(currentDate)[0:10]
        messagebox.showinfo("Error",error)
        for label in labels:
            label.destroy()
        return
    elif tkyear.get() and tkmonth.get() and tkday.get():
        
        
        if len(tkday.get()) == 1:
            
            day = "0"+tkday.get()
        else:
           
            day = tkday.get()
        if len(tkmonth.get()) == 1:
            
            month = "0"+tkmonth.get()
        else:
            
            month = tkmonth.get()
            
        date = tkyear.get() +"-"+month+"-"+day
    else:
        date = None
    print("Date check - "+str(date))

    
    result = list()
    symbols = listbox.curselection()
    for i in symbols:
        entry = listbox.get(i)
        result.append(entry)
    global values1
    values1 = ""
    for val in result:
#        print(val)
        if(len(val) > 0):
            values1 = values1 + val+","
            print(values1[:-1])
            
    if(not symbols):
        values1 = ""
    
    currency = latestRates(tkvar.get().split("-")[0].strip(),date,values1[:-1])
    print(currency)
    a=0
    for key, value in currency:
        currencyLabel = tkinter.Label(app,text = key)
        currencyLabel.grid(row = a+16, column = 4)
        labels.append(currencyLabel)
        valueLabel = tkinter.Label(app,text = value)
        valueLabel.grid(row = a+16, column = 5)
        labels.append(valueLabel)
        a=a+1

b = tkinter.Button(app, text ="Get Forex Rates",command=callback)
b.grid(row = 14, column = 6)

root.mainloop()