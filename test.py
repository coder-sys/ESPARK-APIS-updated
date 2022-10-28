import urllib.request
from bs4 import BeautifulSoup
array_description=[]
for i in list(search(query)):
    page = urllib.request.urlopen('https://www.google.com/?safe=active&ssui=on')
    html = BeautifulSoup(page.read(),'html.parser')
    for tags in html.find_all('meta'):
        array_description.append(tags.get("content"))
print(array_description[0])