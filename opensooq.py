import csv
import requests
from bs4 import BeautifulSoup
import os
import io


cost = []
title = []
link = []
city= []
neighborhood = []
status = []
details = []
j = 1
os.chdir(os.path.dirname(os.path.abspath(__file__)))
item = input("put the item you want: ")
while(j < 7):
    
    url = f"https://jo.opensooq.com/ar/find?have_images=&allposts=&onlyPremiumAds=&onlyDonation=&onlyPrice=&onlyUrgent=&onlyShops=&onlyMemberships=&onlyBuynow=&memberId=&sort=record_posted_date.desc&term={item}&cat_id=&scid=&city=&page={j}&per-page=30"

    reselt = requests.get(url)

    src = reselt.content

    soup = BeautifulSoup(src, "html.parser") 

    titles = soup.find_all("h2", {"class":"fRight mb15"})
    costs = soup.find_all("div", {"class":"price-wrapper"})
    links = soup.find_all("h2", {"class":"fRight"})


    for i in range(len(titles)):
        link.append("https://jo.opensooq.com"+links[i].find("a").attrs["href"])
        title.append(titles[i].text.strip())
        cost.append(costs[i].text.strip())

    for urls in link:
        # print(urls)
        reselt = requests.get(urls)
        soup = BeautifulSoup(reselt.content, "html.parser")
        try:
            data = soup.find_all("a", {"data-role":"dynamicFieldsSearchLink"})
            city.append(data[0].text.strip())
            neighborhood.append(data[1].text.strip())
            status.append(data[5].text.strip())
        except:
            city.append("----")
            neighborhood.append("----")
            status.append("----")
        try:
            detail = soup.find("p", {"class":"firstPart"}).text
            details.append(detail.strip())
        except:
            details.append("no detail")
        

    j += 1
    print("page swicthed")



with open("prodact.csv", "w", encoding='utf-8-sig') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(['Titles', "Cost in JD", "City", "Neighborhood", "Status", "Link to the prodact","Details"])
    for i in range(len(title)):
        wr.writerow([title[i], cost[i], city[i].strip(), neighborhood[i], status[i], link[i],details[i]])



