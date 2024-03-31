import requests,pandas as pd
import csv,time
from requests.api import head

url = 'https://newsapi.org/v2/top-headlines?country=in&sortBy=top&apiKey=8b7f9fe063f74535acbc6a422d7716c7'
response = requests.request("GET",url,data={})
myjson = response.json()
ourdata = []
df=pd.read_csv('sample.csv')
rows=len(df)
c=0
csvheader = ['title','author','description','label']
for x in myjson['articles']:
    for y in range(0,rows):
        if df['title'][y] not in x['title']:
            c=c+1
            if c == rows:
                listing = [x['title'],x['author'],x['description'],'REAL']
                ourdata.append(listing)      
    c=0
if ourdata!=[]:
    with open('sample.csv','a',encoding='UTF8',newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(csvheader)   // for new dataset file
        writer.writerows(ourdata)



for z in range(0,rows):
    if df['title'][z]=="US Removes India From Its Currency Monitoring List; What Does It Mean, Criteria? - News18":
        print(z+1,df['label'][z])
        break;
    elif "insufficient data" in df['title'][z]:
        print("INSUFFICIENT DATA!")
        break;
    elif z == rows-1:
        print("MAY BE FAKE!!!")
        