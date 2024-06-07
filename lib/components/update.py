from sqlalchemy import func
from config import session
from models import Dj, Genre, Subgenre, DjGenre, DjSubgenre
from styling import heading, clear
from colorama import Fore, Style


# Genre mappings
genre_mapping = {
    "drum n bass": "Drum & Bass",
    "dnb": "Drum & Bass",
    "d&b": "Drum & Bass",
    "drum and bass": "Drum & Bass",
    "d & b": "Drum & Bass",
    "d n b": "Drum & Bass",
    "dubstep": "Dubstep/140",
    "140": "Dubstep/140",
}

def update_dj():
    while True:
        clear()
        heading("Update DJ")
        
        dj_name = input("Enter the name of the DJ to update: ").strip()
        dj = session.query(Dj).filter(func.lower(Dj.name) == dj_name.lower()).first()

        if dj:
            clear()
            heading(f"Update {dj.name}")
            print("1. Update Name")
            print("2. Update Production Status")
            print("3. Update Genres and Subgenres")
            print("4. Update Venues")
            print("5. Return to Main Menu")

            choice = input("Please select an option: ").strip()
            if choice == "1":
                new_name = input("Enter new name: ").strip()
                dj.name = new_name
            elif choice == "2":
                new_produces = input("Produces (Y/N): ").strip().lower() == 'y'
                dj.produces = new_produces
            elif choice == "3":
                update_dj_genres_and_subgenres(dj)
            elif choice == "4":
                update_dj_venues(dj)
            elif choice == "5":
                return
            else:
                print(Fore.RED + "Invalid choice, please enter a valid option." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"No DJ found with the name {dj_name}" + Style.RESET_ALL)
            while True:
                choice = input("Do you want to continue searching? Yes/Y or return to main menu No/N: ").strip().lower()
                if choice in ["yes", "y", "ys"]:
                    break
                elif choice in ["no", "n"]:
                    return
                else:
                    print(Fore.RED + "Invalid input, please enter Yes/Y or No/N" + Style.RESET_ALL)


def update_dj_genres_and_subgenres(dj):
    while True:
        clear()
        heading(f"Update Genres and Subgenres\n{dj.name}'s current genres and subgenres")

        genres = dj.genres
        for genre in genres:
            print(f"- {genre.title}")
            for subgenre in genre.subgenres:
                print(f"  - {subgenre.subtitle}")
        print("1. Add a new genre")
        print("2. Update existing genres and subgenres")
        print("3. Remove a genre (and its subgenres) from DJ")
        print("4. Return to previous menu")
        
        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            add_genre_and_subgenre_to_dj(dj)
        elif choice == '2':
            update_genre_subgenres(dj)
        elif choice == '3':
            remove_genre_from_dj(dj)
        elif choice == '4':
            return
        else:
            print(Fore.RED + "Invalid choice, please enter a valid option." + Style.RESET_ALL)

def add_genre_and_subgenre_to_dj(dj):
    while True:
        genre_title = input("Enter Genre: ").strip().title()
        if not genre_title:
            print(Fore.RED + "Genre cannot be blank. Please enter a valid genre." + Style.RESET_ALL)
            continue

        mapped_genre_title = genre_mapping.get(genre_title.lower(), genre_title)
        existing_genre = session.query(Genre).filter(func.lower(Genre.title) == mapped_genre_title.lower()).first()
        if not existing_genre:
            new_genre = Genre(title=mapped_genre_title)
            session.add(new_genre)
            session.commit()
            existing_genre = new_genre

        if existing_genre not in dj.genres:
            dj.genres.append(existing_genre)
            session.commit()

            add_subgenres = input(f"Do you want to add subgenres to {mapped_genre_title}? (yes/no): ").lower()
            if add_subgenres in ["yes", "y"]:
                add_subgenre_to_genre(dj, existing_genre)
        else:
            print(Fore.RED + f"{existing_genre.title} already exists for {dj.name}." + Style.RESET_ALL)

        choice = input("Do you want to continue adding genres? (yes/no): ").lower()
        if choice in ["no", "n"]:
            return


def add_subgenre_to_genre(dj, genre):
    while True:
        subgenre_title = input(f"Enter Subgenre of {genre.title}: ").strip().title()
        if not subgenre_title:
            print(Fore.RED + "Subgenre cannot be blank. Please enter a valid subgenre." + Style.RESET_ALL)
            continue

        mapped_subgenre_title = genre_mapping.get(subgenre_title.lower(), subgenre_title)
        existing_subgenre = session.query(Subgenre).filter(func.lower(Subgenre.subtitle) == mapped_subgenre_title.lower(), Subgenre.genre_id == genre.id).first()
        if not existing_subgenre:
            new_subgenre = Subgenre(subtitle=mapped_subgenre_title, genre=genre)
            session.add(new_subgenre)
            session.commit()
            existing_subgenre = new_subgenre

        if existing_subgenre not in dj.subgenres:
            dj.subgenres.append(existing_subgenre)
            session.commit()

        add_another_subgenre = input(f"Add another subgenre of {genre.title}? (yes/no): ").strip().lower()
        if add_another_subgenre not in ['yes', 'y']:
            break

def update_genre_subgenres(dj):
    pass

def remove_genre_from_dj(dj):
    pass

def update_dj_venues(dj):
    pass
