
import requests
from bs4 import BeautifulSoup
import datetime
import time

url_to_scrape = "http://www.kijiji.ca/b-electronics/edmonton/c15l1700203"
filename = 'ads.txt'

# Set the delay in (s) that the programs waits before scraping again.
scrape_delay = 600 # 600 = 10 mins


def ParseAd(html): # Parses ad html trees and sorts relevant data into a dictionary
    ad_info = {}
    try:
        ad_info["Url"] = 'http://www.kijiji.ca' + html.get("data-vip-url")
    except:
        log('[Error] Unable to parse URL data.')
    try:
        ad_info["Title"] = html.find_all('a',{"class":"title"})[0].text.strip()
    except:
        log('[Error] Unable to parse Title data.')
    try:
        ad_info["Description"] = html.find_all("div", {"class":"description"})[0].text.strip()
    except:
        log('[Error] Unable to parse Description data.')
    try:
        ad_info["Price"] = html.find_all('div',{"class":"price"})[0].text.strip()
    except:
        log('[Error] Unable to parse Price data.')
    return ad_info


def WriteAds(ad_dict,filename): # Writes ads to given file
    try:
        file = open(filename,'a')
        for ad_id in ad_dict:
            file.write(ad_id)
            file.write(str(ad_dict[ad_id]) + "\n")
            log('[Okay] Ad ' + ad_id + ' written to database.')
        file.close()
    except:
        log('[Error] Unable to write ad(s) to database.')

def log(text): # writes log data to log.txt with datetime.
    date_time = datetime.datetime.now()
    file = open('log.txt','a')
    date_time = str(date_time) + '\n'
    text = text + '\n\n'
    file.write(date_time)
    file.write(text)
    file.close()
    
def ReadAds(filename): # Reads given file and creates a dict of ads in file
    import ast
    import os.path
    if not os.path.isfile(filename): # If the file doesn't exist, it makes it.
        file = open(filename,'w')
        file.close()   
    ad_dict = {}
    file = open(filename,'r')
    for line in file:
        if line.strip() != '':
            index = line.find('{')
            ad_id = line[:index]
            dictionary = line[index:]
            dictionary = ast.literal_eval(dictionary)
            ad_dict[ad_id] = dictionary
    file.close()
    return ad_dict


#print(ad_dict)

def main(old_ad_dict): # Main function, brings it all together.
    try:
        page = requests.get(url_to_scrape)
        log("[Okay] Retrieved HTML data from: " + url_to_scrape)
    except:
        log("[Error] Unable to load html data from: " + url_to_scrape)
    soup = BeautifulSoup(page.content,"html.parser")
    page = None
    
    kijiji_ads = soup.find_all("div",{"class":"regular-ad"})
    
    ad_dict = {}

    for ad in kijiji_ads:
        try:
            ad_id = ad.find_all('div',{'class':"watch"})[0].get('data-adid')
            
            if ad_id not in old_ad_dict:
                log('[Okay] New ad found! Ad id: '+ ad_id)
                ad_dict[ad_id] = ParseAd(ad)
            #ad_dict[ad_id] = ParseAd(ad)
            #title = ad.find_all('a',{"class":"title"})[0].text.strip()
        except:
            pass
        
    if ad_dict != {}: # If dict not emtpy, write ads to text file and send email.
        WriteAds(ad_dict,filename)
        try:
            old_ad_dict = ReadAds(filename)
            log("[Okay] Database succesfully reloaded.")
        except:
            log("[Error] Unable to reload database.")
    time.sleep(scrape_delay)
    main(old_ad_dict)
    
if __name__ == "__main__":
    old_ad_dict = ReadAds(filename)
    log("[Okay] Ad database succesfully loaded.")
    file = open('log.txt','w') # Create/Empty log file
    file.close()   
    main(old_ad_dict)
