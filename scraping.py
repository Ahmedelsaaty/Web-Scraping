import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
location_name = []
skills = []
links = []
page_num = 0


while True:
#2nd step use requests to fetch the url 
    try:
        results = requests.get(f"https://wuzzuf.net/search/jobs/?a=navbl&q=python&start={page_num}")

    #3rd step save page content/markup
        src = results.content
    #print(src)

    #4th step create soup object to parse content
        soup = BeautifulSoup(src,"lxml")

        page_limit = int(soup.find("strong").text)
        
        if(page_num > page_limit //15):
            print("pages ended")
            break
    #5th step find the elements containing info. we need 
    #Examples:job titles,job skills,company name,location names ,post time 
        job_titles = soup.find_all("h2",{"class":"css-m604qf"})
        company_names = soup.find_all("a",{"class":"css-17s97q8"})
        locations_names = soup.find_all("span",{"class":"css-5wys0k"})
        job_skills = soup.find_all("div",{"class":"css-y4udm8"})


    # 6th step loop over returned lists to extract needed info into other lists(لووب بترجع كل الداتا اللي جمعتها)
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)
            
        page_num += 1
        print("page switched")
    except:
        print("error occured")
        break


for link in links:
    results = requests.get(link)
    src = results.content
    soup = BeautifulSoup(src,"lxml")


#7th step create csv file and fill it with values
file_list = [job_title , company_name , location_name ,skills,links,]
exported = zip_longest(*file_list)
with open("F:\AHMED\Python\Web Scraping with python\data.csv","w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job title","company name","location","skills","links"])
    wr.writerows(exported)