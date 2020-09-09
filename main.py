import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.filedialog import asksaveasfile 
import os

root = tk.Tk()
root.title("Web Scarping Model")
root.resizable(False, False)
root.config(background="skyblue")

def CreateModule():
    path_label = Label(root, text='Enter Url : ', bg="skyblue")
    path_label.grid(row=0, column=0, padx=10, pady=5)

    root.path_label_entry = Entry(root, width=36, textvariable=url)
    root.path_label_entry.grid(row=0, column=1, padx=10, pady=5)

    path_label_button = Button(root, text="Scrap", command=callUrl, width=15)
    path_label_button.grid(row=0, column=2, padx=5, pady=5)

def callUrl():
    global link, r, urlLink, soup, htmlContent
    link = url.get()
    if link == '':
        messagebox.showinfo("Error", "Please Enter Url")
        return CreateModule()
    if link.find('http://') == -1 and link.find('https://') == -1 :
        link = "http://" + link
    r = requests.get(link)
    if(r):
        urlLink = link
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        SaveFile()

def SaveFile():
    destinationLabel = Label(root, text="Save File : ", bg='skyblue')
    destinationLabel.grid(row=2, column=0, pady=5, padx=5)

    root.destinationText = Entry(root, width=38)
    root.destinationText.grid(row=2, column=1, pady=5)

    browseButton = Button(root, text="BROWSE", command=BROWSE, width=15)
    browseButton.grid(row=2, column=2, pady=5)

    dwldButton = Button(root, text="Save", command=SaveScrape, width=15)
    dwldButton.grid(row=3, column=1, pady=5, padx=5)

def BROWSE():
    files = [('All Files', '*.*'),  
             ('Python Files', '*.py'), 
             ('Text Document', '*.txt')] 
    root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = files)
    root.destinationText.insert('1', root.filename)

def SaveScrape():
    
    savePath = root.destinationText.get()
    
    with open(savePath, 'w', encoding='utf-8') as f_out:

        f_out.write('\n\n#######################  Start  #######################\n\n')
        f_out.write(f'\n\n#######################  Scrape -- {urlLink}  #######################\n\n')

        f_out.write('\n\n=======================  Code Inspect  =======================\n\n')
        f_out.write(soup.prettify())

        f_out.write('\n\n=======================  Title  =======================\n\n')
        f_out.write(soup.title.string)

        links = soup.find_all('a')
        list_link = set()
        for link in links:
            if link != '#':
                list_link.add(link.get('href'))

        f_out.write('\n\n=======================  Links  =======================\n\n')
        for link in links:
            f_out.write('\n'+str(link)+'\n')

        f_out.write('\n\n=======================  Nav  =======================\n\n')
        navabar = soup.find_all('nav')
        for nav in navabar:
            f_out.write(nav)

        f_out.write('\n\n=======================  Links in shorts  =======================\n\n')
        for sLink in list_link:
            f_out.write('\n'+str(sLink)+'\n')

        f_out.write('\n\n=======================  P tag  =======================\n\n')
        pTag = soup.find_all('p')
        for p in pTag:
            f_out.write('\n'+str(p)+'\n')

        f_out.write('\n\n=======================  All Text  =======================\n\n')
        f_out.write(soup.get_text())

        f_out.write('\n\n#######################  End Of File  #######################\n\n')

        f_out.close()

url = tk.StringVar()

link = None
r = None
urlLink = None
soup = None
htmlContent = None

CreateModule()

root.mainloop()
