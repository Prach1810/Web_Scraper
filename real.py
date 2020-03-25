import requests
import time
from bs4 import BeautifulSoup

c=0
x=[]
y=[]

def change():
    url = "https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9"

    # Request with fake header, otherwise you will get an 403 HTTP error
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"class": "tbldata14 bdrtpg"})
    cells = table.findAll("td",{"class":"brdrgtgry","style":"color:#16a903"})
    for i in cells:
        x.append(i.text)
        y.append(i.text)

    return (y)

while True:
    arr=[]
    
    c=c+30
    arr.append(change())
    l=len(arr)
    if(l>=2):
        for i in range(50):
            m=arr[l-2]
            n=arr[l-1]
            if(abs(m[i]-n[i])>=2):
                print("alert")
    
    time.sleep(30)
    if(c>=1200):
        break
    

