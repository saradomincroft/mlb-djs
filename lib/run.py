from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from env import session, os
from colorama import Fore, Style
from models import Dj, Genre, Subgenre, Venue, DjGenre, DjSubgenre, DjVenue
from components import add_dj
from components.search_display_dj import search_dj
from styling import heading, clear
import time

engine = create_engine("sqlite:///lib/data.db")
Session = sessionmaker(bind=engine)
session = Session()


def display_djs():
    clear()
    heading("ALL DJs")
    djs = session.query(Dj).all()
    for dj in djs:
        print(dj)
    input("\nPress Enter to continue...")


def display_genres_subgenres():
    clear()
    heading("ALL GENRES & SUBGENRES")
    genres = session.query(Genre).all()
    for genre in genres:
        print(f"{genre.title}:")
        subgenres = session.query(Subgenre).filter(Subgenre.genre_id == genre.id).all()
        if subgenres:
            for subgenre in subgenres:
                print(f"  - {subgenre.subtitle}")
        else:
            print("  No subgenres found for this genre.")
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
    print("2. Display all Genres & Subgenres")
    print("3. Display all Venues")
    print("4. Add a DJ")
    print("5. Search for a DJ")
    print("6. Update records")
    print("Exit")
    choice = input("Enter your choice: ")
    return choice


def start():
    while True:
        choice = main_menu()
        if choice == '1':
            display_djs()
        elif choice == '2':
            display_genres_subgenres()
        elif choice == '3':
            display_venues()
        elif choice == '4':
            add_dj()
        elif choice == '5':
            search_dj()
        elif choice == '6':
            pass
        elif choice == "exit":
            break
        else:
            print(Fore.RED + "Invalid choice, please enter a vaild option." + Style.RESET_ALL)
            time.sleep(1)
    print("Thank you for using the DJ App!")

if __name__ == "__main__":
    start()
