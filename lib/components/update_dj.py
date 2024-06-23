from sqlalchemy import func
from config import session
from env import clear
from models import Dj, Genre, Subgenre, Venue, DjGenre, DjSubgenre
from styling import subheading, error_message, success_message, check_quit, clear_prev_line
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
        print("UPDATE DJ")

        name = input("Enter the name of the DJ to update: ").strip()
        dj = session.query(Dj).filter(func.lower(Dj.name) == name.lower()).first()
        
        if dj:
            while True:
                clear()
                print(f"UPDATE {dj.name} ")
                print("1. Update Name")
                print("2. Update Production Status")
                print("3. Update Genres and Subgenres")
                print("4. Update Venues")
                print("5. Return to Main Menu")

                choice = input("Please select an option: ").strip()
                if choice == "1":
                    clear()
                    update_name(dj)
                elif choice == "2":
                    clear()
                    while True:
                        produces_input = input(f"Does {dj.name} produce music? Yes/Y or No/N? ").lower()
                        if produces_input in ["y", "yes", "ys"]:
                            produces = True
                            break
                        elif produces_input in ["n", "no"]:
                            produces = False
                            break
                        else:
                            error_message("Invalid input, please enter Yes/Y or No/N")
                    dj.produces = produces
                    session.commit()
                    success_message(f"{dj.name}'s production status has been successfully updated.")
                    
                elif choice == "3":
                    update_dj_genres_and_subgenres(dj)
                elif choice == "4":
                    update_dj_venues(dj)
                elif choice == "5":
                    return
                else:
                    error_message("Invalid choice, please enter a valid option.")
        else:
            error_message(f"No DJ found with the name {name}")
            while True:
                clear()
                choice = input("Do you want to continue searching? Yes/Y or return to main menu No/N: ").strip().lower()
                if choice in ["yes", "y", "ys"]:
                    clear_prev_line()
                    break
                elif choice in ["no", "n"]:
                    return
                else:
                    error_message("Invalid input, please enter Yes/Y or No/N")

# Update DJ name
def update_name(dj):
    while True:
        new_name = input("Enter new name: ").strip()
        if new_name:
            dj.name = new_name
            session.commit()
            success_message(f"{new_name} has successfully been updated.")
            return
        else:
            error_message("Name cannot be blank, please enter a valid name.")

# Update genres and subgenres
def update_dj_genres_and_subgenres(dj):
    while True:
        clear()
        print(f"Update Genres and Subgenres\n{dj.name}'s current genres and subgenres")      
        for genre in dj.genres:
            print(f"- {genre.title}")
            subgenres = session.query(Subgenre).join(DjSubgenre).filter(
                DjSubgenre.dj_id == dj.id,
                Subgenre.genre_id == genre.id
            ).all()
            for subgenre in subgenres:
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
            error_message("Invalid choice, please enter a valid option.")


def add_genre_and_subgenre_to_dj(dj):
    while True:
        genre_title = input("Enter Genre: ").strip().title()
        if not genre_title:
            error_message("Genre cannot be blank, please enter a valid genre.")
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

            add_subgenres = input(f"Do you want to add subgenres to {mapped_genre_title}? (yes/no): ").strip().lower()
            if add_subgenres in ["yes", "y"]:
                add_subgenre_to_genre(dj, existing_genre)
        else:
            error_message(f"{existing_genre.title} already exists for {dj.name}.")

        choice = input("Do you want to continue adding genres? (yes/no): ").strip().lower()
        if choice in ["no", "n"]:
            return

def add_subgenre_to_genre(dj, genre):
    while True:
        subgenre_title = input(f"Enter Subgenre of {genre.title}: ").strip().title()
        if not subgenre_title:
            error_message("Subgenre cannot be blank. Please enter a valid subgenre.")
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
    # print("Update Existing Genres and Subgenres")
    
    # genres = dj.genres
    # for genre in genres:
    #     print(f"- {genre.title}")
    #     for subgenre in genre.subgenres:
    #         print(f"  - {subgenre.subtitle}")
    clear_prev_line()
    genre_title = input("Enter the genre title to update: ").strip().title()
    genre = session.query(Genre).filter(func.lower(Genre.title) == genre_title.lower()).first()
    
    if genre and genre in dj.genres:
        while True:
            clear()
            print(f"Update {genre.title}")
            print(f"Current subgenres for {genre.title}:")
            for genre in dj.genres:
                print(f"- {genre.title}")
                subgenres = session.query(Subgenre).join(DjSubgenre).filter(
                    DjSubgenre.dj_id == dj.id,
                    Subgenre.genre_id == genre.id
                ).all()
                for subgenre in subgenres:
                    print(f"  - {subgenre.subtitle}")

            print("1. Add Subgenre")
            print("2. Remove Subgenre")
            print("3. Return to previous menu")

            choice = input("Select an option: ").strip().lower()
            if choice == '1':
                add_subgenre_to_genre(dj, genre)
            elif choice == '2':
                remove_subgenre_from_genre(dj, genre)
            elif choice == '3':
                return
            else:
                error_message("Invalid choice, please enter a valid option.")
    else:
        error_message(f"{genre_title} is not associated with {dj.name}.")

def remove_subgenre_from_genre(dj, genre):
    clear_prev_line()
    subgenre_title = input(f"Enter the subgenre of {genre.title} to remove: ").strip().title()
    subgenre = session.query(Subgenre).filter(func.lower(Subgenre.subtitle) == subgenre_title.lower(), Subgenre.genre_id == genre.id).first()
    
    if subgenre:
        if subgenre in dj.subgenres:
            dj.subgenres.remove(subgenre)
            session.commit()
            success_message(f"Removed subgenre {subgenre.subtitle} from {genre.title}")
        else:
            error_message(f"{dj.name} does not have the subgenre {subgenre.subtitle} under {genre.title}.")
    else:
        error_message(f"Subgenre {subgenre_title} not found under {genre.title}.")


def remove_genre_from_dj(dj):
    genre_title = input("Enter the genre to remove from DJ: ").strip().title()
    genre = session.query(Genre).filter(func.lower(Genre.title) == genre_title.lower()).first()
    
    if genre and genre in dj.genres:
        for subgenre in genre.subgenres:
            if subgenre in dj.subgenres:
                dj.subgenres.remove(subgenre)
        dj.genres.remove(genre)
        session.commit()
        success_message(f"Removed genre {genre.title} and its subgenres from {dj.name}")
    else:
        error_message(f"Genre {genre_title} not found for {dj.name}.")

# Update venues for DJ
def update_dj_venues(dj):
    clear()
    while True:
        print(f"UPDATE VENUES FOR {dj.name} ")   
        
        print("1. Add a new venue")
        print("2. Remove a venue")
        print("3. Return to previous menu")
        
        choice = input("Select an option: ").strip().lower()
        if choice == '1':
            add_venue_to_dj(dj)
            return
        elif choice == '2':
            remove_venue_from_dj(dj)
            return
        elif choice == '3':
            return
        else:
            error_message("Invalid choice, please enter a valid option.")

# Add a new venue to DJ
def add_venue_to_dj(dj):
    clear()
    subheading(f"\n{dj.name}'s current venues")  
    venues = dj.venues
    for venue in venues:
        print(f"- {venue.venuename}")
    while True:
        venue_name = input("Enter new venue name: ").strip().title()
        if check_quit(venue_name):
            session.rollback()
            return
        elif venue_name.strip() == "":
            error_message("Venue name cannot be blank, please enter a valid venue. ")
            while True:
                choice = input("Do you want to continue adding a venue? Yes/Y or return to main menu No/N: ").strip().lower()
                if choice in ["yes", "y", "ys"]:
                    clear_prev_line()
                    break
                elif choice in ["no", "n"]:
                    return
                else:
                    error_message("Invalid input, please enter Yes/Y or No/N")
            continue

        existing_venue = session.query(Venue).filter(func.lower(Venue.venuename) == venue_name.lower()).first()
        if existing_venue is None:
            clear_prev_line()
            new_venue = Venue(venuename=venue_name)
            session.add(new_venue)
            dj.venues.append(new_venue)
            session.commit()
            existing_venue = new_venue
            success_message(f"Successfully added {existing_venue.venuename} to {dj.name}")
            break

        if existing_venue not in dj.venues:
            clear_prev_line()
            session.add(existing_venue)
            dj.venues.append(existing_venue)
            session.commit()
            success_message(f"Successfully added {existing_venue.venuename} to {dj.name}")
            break
        else:
            error_message(f"{existing_venue.venuename} already exists for {dj.name}")
            while True:
                choice = input("Do you want to continue adding a venue? Yes/Y or return to main menu No/N: ").strip().lower()
                if choice in ["yes", "y", "ys"]:
                    clear_prev_line()
                    break
                elif choice in ["no", "n"]:
                    return
                else:
                    error_message("Invalid input, please enter Yes/Y or No/N")

# Delete a venue from DJ
def remove_venue_from_dj(dj):
    clear()
    subheading(f"\n{dj.name}'s current venues")  
    venues = dj.venues
    for venue in venues:
        print(f"- {venue.venuename}")
    venue_name = input("Enter the venue to remove from DJ: ").strip().title()
    venue = session.query(Venue).filter(func.lower(Venue.venuename) == venue_name.lower()).first()
    while True:
        if venue and venue in dj.venues:
            dj.venues.remove(venue)
            session.commit()
            success_message(f"Successfuly removed venue {venue.venuename} from {dj.name}")
            break
        else:
            error_message(f"Venue {venue_name} not found for {dj.name}")
