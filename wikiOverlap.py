import wikipediaapi
from bs4 import BeautifulSoup
import requests

def get_list(soup):
    hi = soup.find(id="pagehistory")
    ul = hi.find_all("li")
    li = []
    for u in ul:
        u0 = u.find(attrs={"class": "history-user"})
        u1 = u0.find("bdi")
        li.append(u1.string)
    return li
    
def count_list(li):
    result = []
    done = []
    for entry in li:
        if (entry in done) == False:
            done.append(entry)
            n = li.count(entry)
            result.append([entry,n])
    return result

wiki = wikipediaapi.Wikipedia('en')

jl = []

site_list = open("site_list")
for name in site_list:
    if name.endswith('\n'):
        name = name.rstrip('\n')
    print(name)
    
    page = wiki.page("Talk:" + name)
    sections = page.sections
    
    eh = BeautifulSoup(requests.get("https://en.wikipedia.org/w/index.php?title=" + name + "&offset=&limit=500&action=history").content, features="html.parser")
    el = get_list(eh)
    elc = count_list(el)

    th = BeautifulSoup(requests.get("https://en.wikipedia.org/w/index.php?title=" + "Talk:" + name + "&offset=&limit=500&action=history").content, features="html.parser")
    tl = get_list(th)
    tlc = count_list(tl)

    ol = []
    for e in elc:
        for t in tlc:
            if e[0] == t[0]:
               ol.append([e[0],e[1],t[1]])

    j = len(ol)/(len(elc)+len(tlc)-len(ol))
    jl.append(j)
    
aj = sum(jl)/len(jl)
print("Average Jaccard index: " + str(aj))
print("Max Jaccard index: " + str(max(jl)))
print("Min Jaccard index: " + str(min(jl)))