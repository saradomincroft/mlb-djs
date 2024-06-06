from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from env import session, os
from colorama import Fore, Style
from models import Dj, Genre, Subgenre, Venue, DjGenre, DjSubgenre, DjVenue
import time

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


# Function to add a DJ
def add_dj():
    while True:
        name = input("Enter DJ name: ")
        existing_dj = session.query(Dj).filter(func.lower(Dj.name) == name.lower()).first()
        if existing_dj:
            print(f"{existing_dj} already exists in the database.")
            while True:
                choice = input("Do you want to continue adding a new DJ (Yes/Y or No/N)? ").lower()
                if choice in ["yes", "ys", "y"]:
                    break
                elif choice in ["no", "n"]:
                    return
                else:
                    print("Invalid input, please enter Yes/Y or No/N")
        else:
            break
    
    while True:
        produces_input = input(f"Does {name} produce music? Yes/Y or No/N? ").lower()
        if produces_input in ["y", "yes", "ys"]:
            produces = True
            break
        elif produces_input in ["n", "no"]:
            produces = False
            break
        else:
            print("Invalid input, please enter Yes/Y or No/N ")

    new_dj = Dj(name=name, produces=produces)

    session.add(new_dj)

    genre_mapping = {
        "drum n bass": "Drum & Bass",
        "dnb": "Drum & Bass",
        "d&b": "Drum & Bass",
        "drum and bass": "Drum & Bass",
        "d & b": "Drum & Bass",
        "d n b": "Drum & Bass"
    }

    genre_mapping = {
        "Dubstep": "Dubstep/140",
        "140": "Dubstep/140",
    }

    while True:
        genre_title = input("Enter Genre: ").title()
        if not genre_title:
            print("Genre title cannot be empty.")
            continue
        

        mapped_genre_title = genre_mapping.get(genre_title.lower(), genre_title)
        genre = session.query(Genre).filter(func.lower(Genre.title) == mapped_genre_title.lower()).first()
        if genre is None:
            genre = Genre(title=mapped_genre_title)
            session.add(genre)
            session.commit()
        elif genre not in new_dj.genres:
            new_dj.genres.append(genre)

        while True:
            subgenre_title = input(f"Enter Subgenre of {mapped_genre_title} that {name} plays: ").title()
            if not subgenre_title:
                print("Subgenre title cannot be empty.")
                continue
            
            mapped_subgenre_title = genre_mapping.get(subgenre_title.lower(), subgenre_title)
            subgenre = session.query(Subgenre).filter(func.lower(Subgenre.subtitle) == mapped_subgenre_title.lower(), Subgenre.genre_id == genre.id).first()
            if subgenre is None:
                subgenre = Subgenre(subtitle=mapped_subgenre_title, genre=genre)
                session.add(subgenre)
                session.commit()
            elif subgenre not in genre.subgenres:
                genre.subgenres.append(subgenre)

            add_another_subgenre = input(f"Do you want to add another subgenre of {mapped_genre_title} that {name} plays? (yes/no): ").lower()
            if add_another_subgenre in ["yes", "y", "ys"]:
                continue
            elif add_another_subgenre in ["no", "n"]:
                break
            else:
                print("Invalid input, please enter Yes/Y or No/N")

        add_another_genre = input(f"Do you want to add another genre for {name}? (yes/no): ").lower()
        if add_another_genre in ["yes", "y", "ys"]:
            continue
        elif add_another_genre in ["no", "n"]:
            break
        else:
            print("Invalid input, please enter Yes/Y or No/N")

    while True:
        venue_name = input("Enter a venue where the DJ has played: ").title()
        if not venue_name:
            print("Venue name cannot be empty.")
            continue
        
        venue = session.query(Venue).filter(func.lower(Venue.venuename) == venue_name.lower()).first()
        if venue is None:
            venue = Venue(venuename=venue_name)
            session.add(venue)
            session.commit()
        elif venue not in new_dj.venues:
            new_dj.venues.append(venue)

        add_another_venue = input(f"Do you want to add another venue for {name}? (yes/no): ").lower()
        if add_another_venue in ["yes", "y", "ys"]:
            continue
        elif add_another_venue in ["no", "n"]:
            break
        else:
            print("Invalid input, please enter Yes/Y or No/N")


    session.commit()
    print(f"{name} added successfully.")

# display dj for search function
def display_dj_details(dj):
    while True:
        clear()
        heading(f"{dj.name}:")
        print("1. View All Details")
        print("2. View Genres and Subgenres")
        print("3. View Venues")
        print("4. View Production Status")
        print("6. Return to Main Menu")
        choice = input("Please select an option")

        if choice == "1":
            clear()
            heading(f"{dj.name}'s Full Details")
            print(f"Producer: {'Y' if dj.produces else 'N'}\n")

            print("Genres and Subgenres:")
            genres = dj.genres
            for genre in genres:
                print(f"- {genre.title}")
                subgenres = session.query(Subgenre).filter_by(genre_id=genre.id).all()
                for subgenre in subgenres:
                    print(f"  - {subgenre.subtitle}")

            print("\nVenues:")
            venues = [venue.venuename for venue in dj.venues]
            for venue in venues:
                print(f"- {venue}")

            input("\nPress Enter to return to the previous menu. ")
            



# search for a DJ via name function
def search_dj():
    clear()
    heading("SEARCH FOR A DJ")
    dj_name = input("Enter DJ name: ")
    dj = session.query(Dj).filter(func.lower(Dj.name) == dj_name.lower()).first()

    if dj:
        display_dj_details(dj)
    else:
        print(f"No Dj found with the name {dj_name}")
        while True:
            choice = input("Do you want to continue searching? Yes/Y or return to main menu No/N: ").lower()
            if choice in ["yes", "y", "ys"]:
                break
            elif choice in ["no", "n"]:
                return
            else:
                print("Invalid input, please enter Yes/Y or No/N")



def main_menu():
    clear()
    print("DJ App Main Menu")
    print("1. Display all DJs")
    print("2. Display all Genres")
    print("3. Display all Subgenres")
    print("4. Display all Venues")
    print("5. Add a DJ")
    print("6. Search for a DJ")
    print("7. Update records")
    print("Exit")
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
            add_dj()
        elif choice == '6':
            search_dj()
        elif choice == "exit":
            break
        else:
            print(Fore.RED + "Invalid choice, please enter a vaild option." + Style.RESET_ALL)
            time.sleep(2)
    print("Thank you for using the DJ App!")

if __name__ == "__main__":
    start()
