import fire
from env import session, clear
from colorama import Fore, Style
from models import Dj, Genre, Subgenre, Venue
from components import add_dj, update_dj, search_dj, delete_dj
from styling import heading, subheading_two, error_message, success_message, clear_prev_line

def display_djs():
    clear()
    subheading_two("ALL DJs")
    djs = session.query(Dj).all()
    for dj in djs:
        print(dj)
    input("\nPress Enter to go back to the main menu. ")

def display_genres_subgenres():
    clear()
    subheading_two("ALL GENRES & SUBGENRES")
    genres = session.query(Genre).all()
    for genre in genres:
        print(f"{genre.title}:")
        subgenres = session.query(Subgenre).filter(Subgenre.genre_id == genre.id).all()
        for subgenre in subgenres:
            print(f"  - {subgenre.subtitle}")
    input("\nPress Enter to go back to the main menu. ")

def display_venues():
    clear()
    subheading_two("ALL VENUES")
    venues = session.query(Venue).all()
    for venue in venues:
        print(venue)
    input("\nPress Enter to go back to the main menu. ")

def start():
    """Starts DJ App.""" # Docstring
    clear()
    while True:
        heading("DJ DATABASS")
        print(f"{Fore.MAGENTA}1. Display DJs{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}2. Display Genres & Subgenres{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}3. Display Venues{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}4. Display DJ{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}5. Add DJ{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}6. Update DJ{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}7. Delete DJ{Style.RESET_ALL}")
        print(f"{Fore.RED}8. Exit{Style.RESET_ALL}")
        choice = input("Enter your choice: ")
        if choice == '1':
            display_djs()
        elif choice == '2':
            display_genres_subgenres()
        elif choice == '3':
            display_venues()
        elif choice == '4':
            search_dj()
        elif choice == '5':
            add_dj()
        elif choice == '6':
            update_dj()
        elif choice == '7':
            delete_dj()
        elif choice == '8':
            break
        else:
            clear()
            clear_prev_line()
            error_message("Invalid choice, please enter a valid option.")
    success_message("Thank you for using the DJ App!")

if __name__ == "__main__":
    fire.Fire(start)
