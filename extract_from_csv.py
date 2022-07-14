import requests
from bs4 import BeautifulSoup
from csv import DictReader
from random import choice


def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        quotes = list(csv_reader)
        return quotes
          

def start_game(quotes):
    quote_data = choice(quotes)
#     print ("Here's a Quote: ")
#     print(f"{quote_data['text']} \n who said it?")

    guess = ""
    guess_num = 4
    while guess.lower() != quote_data["author"].lower():
        guess = input(f" Here's a Quote: {quote_data['text']} \n who said it? \n Guesses remaining: {guess_num}")
        guess_num -=1
        if guess_num == 3:
            res = requests.get(f"{base_url}{quote_data['bio-link']}")
            soup =BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_location = soup.find(class_="author-born-location").get_text()
            print (f"Here's a hint, author was born on {birth_date}")
        elif guess_num == 2:
            print(f"Here's another hint, author was born in {birth_location}")
        elif guess_num == 1:
            last_initial= quote_data['author'].split(" ")[1][0]
            print(f"Here's a final hint, author's first and last name starts with  {quote_data['author'][0]} and {last_initial}")
        else:
            print (f"Sorry you ran out of answers. The answer is {quote_data['author']}") if guess_num == 0 else None
            break

    again =""

    while again.lower() not in ("y","yes","n","no"):
        again = input("would you like to play again?")
    if again.lower() in ("yes", "y"):
        print("Okay, you play again")
        return start_game(quotes)
    else:
        print("Okay. GOODBYE")

quotes = read_quotes("quote.csv")

start_game(quotes)
