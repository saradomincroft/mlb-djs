from env import session, clear
from colorama import Fore, Style
from models import Dj, Genre, Subgenre, Venue
from components import add_dj, update_dj, search_dj
from styling import heading, subheading, error_message, success_message, clear_prev_line

# MAIN MENU FUNCTIONS

def main_menu():
    clear()
    heading("DJ DATABASS")
    print("1. Display all DJs")
    print("2. Display all Genres & Subgenres")
    print("3. Display all Venues")
    print("4. Add a DJ")
    print("5. Search for a DJ")
    print("6. Update DJ Info")
    print("7. Delete records")
    print("8. Exit")
    choice = input("Enter your choice: ")
    return choice


def start():
    clear()
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
            update_dj()
        elif choice == '8':
            break
        else:
            clear()
            clear_prev_line()
            error_message("Invalid choice, please enter a valid option.")
    success_message("Thank you for using the DJ App!")

def display_djs():
    clear()
    subheading("ALL DJs")
    djs = session.query(Dj).all()
    for dj in djs:
        print(dj)
    input("\nPress Enter to go back to the main menu. ")

def display_genres_subgenres():
    clear()
    print("ALL GENRES & SUBGENRES")
    genres = session.query(Genre).all()
    for genre in genres:
        print(f"{genre.title}:")
        subgenres = session.query(Subgenre).filter(Subgenre.genre_id == genre.id).all()
        for subgenre in subgenres:
            print(f"  - {subgenre.subtitle}")
    input("\nPress Enter to go back to the main menu. ")

def display_venues():
    clear()
    print("ALL VENUES")
    venues = session.query(Venue).all()
    for venue in venues:
        print(venue)
    input("\nPress Enter to go back to the main menu. ")

if __name__ == "__main__":
    start()
