import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

BASE_URL = "http://quotes.toscrape.com"


def scrape_quote(): 
  all_quotes = []
  url = "/page/1"
  #while loop to loop through the pages a quotes
  while url:
    #setting our request method to pull the BASE_URL and the url
    res = requests.get(f"{BASE_URL}{url}")
    # using the beautifulSoup html parser to display the info
    soup = BeautifulSoup(res.text, "html.parser")
    # setting quotes to all items with the html class "quote"
    quotes = soup.find_all(class_="quote")
    #looping through the quotes
    for quote in quotes:
      #adding quotes to our all_quotes list
      all_quotes.append({
        #getting the text from all the html class "text" items
        "text":quote.find(class_="text").get_text(),
        #getting the text from all the html class "author" items
        "author":quote.find(class_="author").get_text(),
        #grabbing the first a tag item in the div that holds quotes
        "bio-link": quote.find("a")["href"]
        })
    #setting next_btn to the next button at the bottom of the webpage
    next_btn = soup.find(class_="next")
    #updating the url var to next_btn if there is one, if not return None
    url= next_btn.find("a")["href"] if next_btn else None
    #be polite and don't bog servers with requests
    sleep(1)
    return all_quotes

def write_quotes(quotes): 
  with open("quotes.csv", "w") as file:
    headers = ["text", "author", "bio-link" ]
    csv_writer = DictWriter(file, fieldnames = headers)
    csv_writer.writeheader()
    for quote in quotes:
      csv_writer.writerow(quote)

quotes = scrape_quote()
write_quotes(quotes)
  
