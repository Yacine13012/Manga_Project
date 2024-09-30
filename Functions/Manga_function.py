def write_to_file(filename, content, mode='a'):    
    """Writes the given log to the log file.

    Args:
        filename (str): The name of the file to add the content.
        content (str): The content to write to the file.
        mode (str, optional): The file opening mode. Defaults to 'a' (append).
            Other modes include:
            - 'w' (write)
            - 'r+' (read and write)
    """

    # Import Datetime
    from datetime import datetime
    
    try:
        with open(filename, mode, encoding='utf-8') as file:
            file.write(str(datetime.now()) + ": " + content + "\n")
    except IOError as e:
        print(f"Error writing to content to log file.': {e}")

def create_soup(url,sleep = 1):
    """Extract data from the url.

    Args:
        url (str): The link to the data to be extracted.
        sleep (int, optional): The time to wait before extracted the page web. Defaults to 1s.
    """

    # Import Webdriver
    from selenium import webdriver

    # Beautiful soup
    from bs4 import BeautifulSoup # this module helps in web scrapping.

    # time
    import time


    driver = webdriver.Firefox() 
    # Webscrape the URL
    driver.get(url)
    # wait 5s
    time.sleep(sleep)
    # Create a Beautiful soup object
    soup = BeautifulSoup(driver.page_source,"html.parser")
    # close driver
    driver.close()
    return soup     

def extract_date(date):
    """Extract date from the beautiful soup..

    Args:
        date (str): String including the date extracted from beautiful soup.
    """
    for i in range(10):
        if "Épisode" in date[i].text:
            date = date[i].text
            date_list=[]
            date_list = date[date.find("le")+3:].split()
            day = int(date_list[0])
            month = int(date_list[1].replace("janv.","01").replace("févr.","02").replace("mars","03").replace("avr.","04").replace("mai","05").replace("juin","06").replace("juil.","07").replace("août","08").replace("sept.","09").replace("oct.","10").replace("nov.","11").replace("déc.","12"))
            year = int(date_list[2])
            return day,month,year
        
def extract_episod(ep):
    """Extract episod from the beautiful soup..

    Args:
        ep (str): String including the episod extracted from beautiful soup.
    """
    ep_list=[]
    ep_list = ep.split(".E")
    season = int(ep_list[0][-1])
    episod_season = int(ep_list[1])
    return season,episod_season

def extract_link(link):
    """Extract link from the beautiful soup..

    Args:
        link (str): String including the link extracted from beautiful soup.
    """
    link = "https://www.imdb.com/" + link[0:link.find("/?ref")]
    return link

def extract_title(title):
    """Extract title from the beautiful soup..

    Args:
        title (str): String including the title extracted from beautiful soup.
    """
    if "," in title:
        title = title.replace(",","")
    return title                 