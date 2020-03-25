import urllib.request
from bs4 import BeautifulSoup
from newspaper import Article
import requests
import time
import MySQLdb

#SQL connection data to connect and save the data in
HOST = "localhost"
USERNAME = "scraping_user"
PASSWORD = ""
DATABASE = "taskdb"

url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"
# Open the URL as Browser, not as python urllib

page = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'}) 
infile = urllib.request.urlopen(page).read()
soup = BeautifulSoup(infile,'lxml')

section = soup.findAll("h3", {"class": "ipQwMb ekueJc gEATFF RD0gLb"})
sec = soup.findAll("div", {"class": "SbNwzf"})

words = ["surge","acquisitions","initial public offering(IPO)"]


for a,b in zip(section,sec):#.find('a',href=True):
    s=a.find('a')
    l=s['href']
    link="https://news.google.com"+l[1:]
    
    db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    toi_article = Article(link, language="en")
    toi_article.download() 
    toi_article.parse() 
    toi_article.nlp()
    r=toi_article.title
    s= toi_article.summary
    t=toi_article.publish_date

    print("Article's Title:")
    print(r) 
    print("\n")

    
    sql = "INSERT INTO Main_News(Title, Summary, Date_Time, URL) VALUES(?,?,?,?) ",(r,s, t,link)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        #get the just inserted class id
    sql = "SELECT LAST_INSERT_ID()"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Get the result
        result = cursor.fetchone()
        # Set the class id to the just inserted class
        class_id = result[0]
    except:
        # Rollback in case there is any error
        db.rollback()
        # disconnect from server
        db.close()
        # on error set the class_id to -1
        class_id = -1

    s2 = b.findAll("a", {"class": "DY5T1d"})
    
    for x in s2:
        p=x['href']
        l="https://news.google.com"+p[1:]
        toi = Article(l, language="en")
        toi.download()
        toi.parse() 
        toi.nlp()

        r=toi.title
        s= toi.summary
        t=toi.publish_date
        #print("Sunbnews's Title:")
        print(r) 
        #print("\n") 
        db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        
        sql = "INSERT INTO Sub_News(news_id,Title, Summary, Date_Time, URL) VALUES (?,?,?,?,?)",(class_id, r, s ,t,l)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()

    print("-"*20)
    time.sleep(5)

def search(words):
    r=requests.get(url)
    soupy = BeautifulSoup((r.content),'lxml')
    for w in words:
        f=soupy.find_all(lambda tag: w in tag.string if tag.string else False)
        sen =list( map(lambda element: element.string, f))
        for a in sen:
            print(a)
            time.sleep(5)

search(words)