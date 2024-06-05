from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env import session, os
from colorama import Fore, Style
from models import Dj, Genre, Subgenre, Venue, DjGenre, DjSubgenre, DjVenue

engine = create_engine("sqlite:///lib/data.db")
Session = sessionmaker(bind=engine)
session = Session()

def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def heading(text):
    print("*" * 30)
    print(text)
    print("*" * 30)

def display_djs():
    clear()
    heading("ALL DJs")
    djs = session.query(Dj).all()
    for dj in djs:
        print(dj)
    input("\nPress Enter to continue...")

def display_genres():
    clear()
    heading("ALL GENRES")
    genres = session.query(Genre).all()
    for genre in genres:
        print(genre)
    input("\nPress Enter to continue...")

def display_subgenres():
    clear()
    heading("ALL SUBGENRES")
    subgenres = session.query(Subgenre).all()
    for subgenre in subgenres:
        print(subgenre)
    input("\nPress Enter to continue...")

def display_venues():
    clear()
    heading("ALL VENUES")
    venues = session.query(Venue).all()
    for venue in venues:
        print(venue)
    input("\nPress Enter to continue...")

def main_menu():
    clear()
    print("DJ App Main Menu")
    print("1. Display all DJs")
    print("2. Display all Genres")
    print("3. Display all Subgenres")
    print("4. Display all Venues")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice

def start():
    while True:
        choice = main_menu()
        if choice == '1':
            display_djs()
        elif choice == '2':
            display_genres()
        elif choice == '3':
            display_subgenres()
        elif choice == '4':
            display_venues()
        elif choice == '5':
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
    print("Thank you for using the DJ App!")

if __name__ == "__main__":
    start()
