from bs4 import BeautifulSoup
from newsapi import NewsApiClient
from tkinter import *
import requests
# personal file "setting.py" that contains
# api key of newsapi
from settings import MY_API_KEY


newsapi = NewsApiClient(api_key=MY_API_KEY)


def search():
    # add a vertical scrollbar to the canvas
    scrollbar = Scrollbar(second_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # create a news frame inside canvas to place the widgets later
    news_frame = Frame(canvas)
    # create canvas window with news frame
    canvas.create_window((0,0), window=news_frame, anchor="nw")

    # get the query text entered by the user
    text = entry.get()
    # perform the query
    data = newsapi.get_everything(q=text, language="en", page_size=20, sources="the-verge")
    articles = data["articles"]
    # for each article, obtain the title and
    # summary content to link it with its url
    for article in articles:
        title = article["title"]
        url = article["url"]
        content = article["content"]
        # place clickable title lables to the news_frame
        title_lbl = Label(news_frame, text=title, font=("monospace", 14, "bold"), textvariable=url)
        title_lbl.pack(pady=5)
        title_lbl.bind("<Button-1>", callback)
        # place clickable content lables to the news_frame
        content_lbl = Label(news_frame, text=content, font=("monospace", 11), textvariable=url)
        content_lbl.pack()
        content_lbl.bind("<Button-1>", callback)
        print(title)

# when the title or the content of the news
# is clicked
def callback(event):
    # get title and url from the call
    title = event.widget.cget("text")
    url = event.widget.cget("textvariable")
    # make a request to the url
    source = requests.get(url)
    soup = BeautifulSoup(source.content, "html.parser")
    content = soup.find("div", class_="c-entry-content")
    # get the article from its website
    full_text = ""
    for paragraph in content.find_all("p"):
        full_text += paragraph.text
    # open a new window
    new_window = Toplevel(master)
    new_window.geometry("800x400")
    # place the label of the article
    Label(new_window, text=title, font=("monospace", 16, "bold")).pack()
    # place all of the content
    text = Text(new_window, font=("monospace", 12))
    text.insert(END, full_text)
    text.pack(fill="both")



# creates a Tk() object 
master = Tk() 
master.resizable(width=False, height=False)
master.configure(bg="white")
master.title("Breaking News")
master.geometry("900x660") 

# upper frame that involves search bar 
# and additional information labels
frame = Frame(master, bg="white")
frame.pack(fill=BOTH, expand=1)

# greeting label
label = Label(frame, bg="white", text="Welcome to the ... News.", anchor="center") 
label.config(font=("monospace", 18, "bold"))
label.pack() 

label_detail = Label(frame, bg="white", text="Find the most up-to-date news as if on the wings of the wind!", anchor="center") 
label_detail.config(font=("monospace", 12))
label_detail.pack()

search_bar_exp = Label(frame, bg="white", text="Use the search bar below to find the news.", anchor="center") 
search_bar_exp.config(font=("monospace", 12))
search_bar_exp.pack()

# get user search keys to perform the query
entry = Entry(frame, width=50, borderwidth=2)
entry.pack()

enter_btn = Button(frame, text="Search", command=search, height=2, width=20, bg="#20bebe", fg="white")
enter_btn.pack()


# --- bottom frame for news ---

# create the bottom frame to place canvas
second_frame = Frame(master, bg="blue")
second_frame.pack(fill=BOTH, expand=1)

# create canvas inside the second frame
# this canvas is used to place labels relevant to
# searched news and scrollbar
canvas = Canvas(second_frame, width=880, height=500)
canvas.pack(side=LEFT, fill=BOTH, expand=1)


# start main loop
mainloop() 