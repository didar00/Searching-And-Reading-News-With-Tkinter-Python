from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from settings import MY_API_KEY
from tkinter import *
import pandas as pd
import requests
import csv

newsapi = NewsApiClient(api_key=MY_API_KEY)

def search():
    text = entry.get()
    # make the query according to the category
    data = newsapi.get_everything(q=text, language="en", page_size=25, sources="the-verge")
    articles = data["articles"]
    for article in articles:
        title = article["title"]
        url = article["url"]
        content = article["content"]
        print(url)
        # place clickable title lables to the news_frame
        title_lbl = Label(news_frame, text=title, font=("Times", 14, "bold"), textvariable=url)
        title_lbl.pack()
        title_lbl.bind("<Button-1>", callback)
        # place clickable content lables to the news_frame
        content_lbl = Label(news_frame, text=content, font=("Times", 10, "bold"), textvariable=url)
        content_lbl.pack()
        content_lbl.bind("<Button-1>", callback)

'''
def callback(event):
    txt = event.widget.cget("text")
    print(txt)
    txt = event.widget.cget("textvariable")
    print(txt)
'''
def callback(event):
    #title = event.widget.cget("text")
    url = event.widget.cget("textvariable")
    #print(title, "    " , url)
    # make a request to the url
    source = requests.get(url)
    soup = BeautifulSoup(source.content, "html.parser")
    #print(soup.encode("utf-8"))
    content = soup.find("div", class_="c-entry-content")
    #full_text = ""
    #for paragraph in content.find_all("p"):
    #    full_text += paragraph.text
    new_window = Toplevel(master)
    new_window.geometry("800x400") 
    text = Text(new_window)
    text.insert(END, content.text)
    text.pack()

        


# show all these articles' titles in the window to be selected by the user
#for x, y in enumerate(articles):
#    print(f'{x} {y["title"]}')


'''
for paragraph in content.find_all("p"):
    print(paragraph.text)
'''


# creates a Tk() object 
master = Tk() 
master.resizable(width=False, height=False)
#master.configure(bg="white")
master.title("Breaking News")
master.geometry("1200x600") 


frame = Frame(master, bg="red")
frame.pack(side="left", fill=Y)

label = Label(frame, bg="white", text="Welcome to the ... News.", anchor="center") 
label.config(font=("Times", 18, "bold"))
label.pack() 

label_detail = Label(frame, bg="white", text="Find the most up-to-date news as if on the wings of the wind!", anchor="center") 
label_detail.config(font=("Times", 12))
label_detail.pack()

search_bar_exp = Label(frame, bg="white", text="Use the search bar below to find the news.", anchor="center") 
search_bar_exp.config(font=("Times", 12))
search_bar_exp.pack()

# get user search keys to perform the query
entry = Entry(frame)
entry.pack()

enter_btn = Button(frame, text="Search", command=search)
enter_btn.pack()

news_frame = Frame(master)
news_frame.pack(side="right", fill=Y)

mylabel=Label(news_frame)
mylabel.pack(side="right")
text=Text(mylabel)
text.grid(row=0,column=1)
scrollbar =Scrollbar(mylabel,command=text.yview)
text.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0,column=0,sticky=NSEW)
text.insert(END,"arrayarrayarrayarrayarrayarrayarrayarrayarray")

mainloop() 