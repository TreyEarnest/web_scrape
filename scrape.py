import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

BASE_URL = "http://quotes.toscrape.com"


def scrape_quote(): 
  all_quotes = []
  url = "/page/1"
  #while loop to loop through the pages a quotes
  while url:
    #setting our request method to pull the BASE_URL and the url
    res = requests.get(f"{BASE_URL}{url}")
    # print(f"Now scraping {BASE_URL}{url}.....")
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
    sleep(2)
    return all_quotes

def start_game(quotes): 
  quote = choice(quotes)
  remaining_guesses = 4
  print("Here's a quote: ")
  print(quote["text"])
  print(quote["author"])
  guess = ""
  while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
    guess = input(f"who said this quote? Guesses remaining: {remaining_guesses}\n")
    if guess.lower() == quote["author"].lower():
      print("YOU GOT IT RIGHT!")
      break
    remaining_guesses -= 1
    if remaining_guesses ==3:
      res = requests.get(f"{BASE_URL}{quote['bio-link']}")
      soup = BeautifulSoup(res.text, "html.parser")
      birth_date = soup.find(class_="author-born-date").get_text()
      birth_place = soup.find(class_="author-born-location").get_text()
      print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 2:
      print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
    elif remaining_guesses == 1:
      last_initial = quote['author'].split(" ")[1][0]
      print(f"Here's a hint: The author's last name starts with: {last_initial}")
    else:
      print(f"Sorry you ran our of guesses. The answer was {quote['author']}")

  again = ""
  while again.lower() not in ('y', 'yes', 'n', 'no'):
    again = input("Would you like to play again (y/n)?")
  if again.lower() in ('yes', 'y'):
    return start_game(quotes) 
  else: 
    print("OK, GOODBYE")

quotes = scrape_quote()
start_game(quotes)