import wikipediaapi
import nltk
import nltk.data
import pandas as pd
import datefinder
from bs4 import BeautifulSoup
import requests

def process_date(s1):
    dates = datefinder.find_dates(s1, index = True)
    res = []
    fin = []
    for d in dates:
        fin = d
    if fin != []:
        res.append(fin[0])
        res.append(s1[0:fin[1][0]])
    return res

def find_user(c, tl):
    for u in tl:
        if u in c:
            return u
    return "N/A"
    
def get_list(soup):
    hi = soup.find(id="pagehistory")
    ul = hi.find_all("li")
    li = []
    for u in ul:
        u0 = u.find(attrs={"class": "history-user"})
        u1 = u0.find("bdi")
        li.append(u1.string)
    return li

wiki = wikipediaapi.Wikipedia('en')

#site_list = open()
#for site in site_list:
name = "Asterisk"
page = wiki.page("Talk:" + name)

sections = page.sections

sen_det = nltk.data.load("tokenizers/punkt/english.pickle")
df = pd.DataFrame([],columns=['Section','Comment','User','Datetime'])
n=0

th = BeautifulSoup(requests.get("https://en.wikipedia.org/w/index.php?title=" + "Talk:" + name + "&offset=&limit=500&action=history").content, features="html.parser")
tl = get_list(th)



for sec in sections:
    title = sec.title
    comments = sec.text.splitlines()
    
    for comment in comments:
        sents = sen_det.tokenize(comment)
        if len(sents) > 1:
            met = sents[-1]
        else:
            met = comment
        
        if '...' in met:
            met = met.split('...')[-1]
        
        d = process_date(met)
        if d == []:
            d.append('N/A')
        u = find_user(comment, tl)
            
        df = pd.concat([df,pd.DataFrame({'Section':title,'Comment':comment,'User':u,'Datetime':d[0]}, index = [n])])
        n = n+1

print(df)
out = open("wiki_comments.csv", "x")
df.to_csv(path_or_buf=out)