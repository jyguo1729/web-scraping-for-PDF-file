#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import the library used to query a website
import urllib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.parse import urljoin
import os
import sys




#specify the url
try:
    url=sys.argv[1]
except IndexError:
    url='http://web.cs.ucla.edu/~yzsun/classes/2018Fall_CS145/schedule.html'
    
#Query the website and return the html to the variable 'page'
page = urllib.request.urlopen(url)


#Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page)
#print(soup.prettify())

all_link=soup.find_all("a") 
A=[]
B=[]
for link in all_link:
    A.append(link.contents[0])
    B.append(urljoin(url,link['href']))

df=pd.DataFrame(A,columns=['Description'])
df['link']=B


dirname = os.path.dirname(__file__)
#dirname="C:\py\crawler"
relpath='output'
path= os.path.join(dirname, relpath,"output.csv")
df.to_csv(path)


for link in B:
    file_name = link.split('/')[-1]
    print("start with ",file_name)

    #test if link is open
    try: u=urllib.request.urlopen(link)
    except urllib.error.URLError as e:
        print(e.reason)
        continue
    
    #determine file name end with .pdf, skip this file otherwise
    meta = u.info()
    if(meta['Content-Type']!='application/pdf'):
        print(file_name," is not a PDF file")
        continue
        
    #set abosolute path for the file
    path_file_name = os.path.join(dirname, relpath,file_name)
    print("path_file_name is",path_file_name)
        
    #download file  
    f = open(path_file_name, 'wb')
    file_size=int(meta['Content-Length'])
    print (f"Downloading: %s Bytes: %s" % (file_name, file_size))
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        #status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        #status = status + chr(8)*(len(status)+1)
        #print (status),
    print("downloading finished")
    f.close()
    #'''


# In[ ]:




