from sqlalchemy import func
from models import Dj, Genre, Subgenre, Venue
from env import session, os
from styling import clear, heading, error_message, success_message, clear_prev_line, clear_prev_two_line
import time

def check_quit(input_str):
    return input_str.lower() == "quit"

# FUNCTION TO ADD DJ INTO THE DB
def add_dj():
    heading("ADD NEW DJ\nTo return to the main menu, type 'quit' and press enter at any time. ")

    # Add DJ by DJ name, error message displays if blank or if DJ already exists in db.
    while True:
        name = input("DJ Name: ")
        if check_quit(name):
            session.rollback()
            return
        elif not name.strip():
            error_message("Name cannot be blank, please enter a valid name.")
            time.sleep(1)
            clear_prev_two_line()
            continue

        existing_dj = session.query(Dj).filter(func.lower(Dj.name) == name.lower()).first()
        if existing_dj:
            error_message(f"{name} already exists in the database.")
            time.sleep(1)
            clear_prev_two_line()
            continue
        else:
            break
    
    # Add music production status
    while True:
            produces_input = input(f"Does {name} produce music? Yes/Y or No/N? ").lower()
            if check_quit(produces_input):
                session.rollback()
                return
            elif produces_input in ["y", "yes", "ys"]:
                clear_prev_line()
                produces = True
                print("Producer: Yes")
                break
            elif produces_input in ["n", "no"]:
                clear_prev_line()
                produces = False
                print("Producer: No")
                break
            else:
                error_message("Invalid input, please enter Yes/Y or No/N ")
                time.sleep(1)
                clear_prev_two_line()

    # Add to session (not commit until end)
    new_dj = Dj(name=name, produces=produces)
    session.add(new_dj)

    # Genre mapping to avoid duplicates for genres which go by multiple names (e.g Dnb, D&B, Drum n Bass etc)
    genre_mapping = {
        "drum n bass": "Drum & Bass",
        "dnb": "Drum & Bass",
        "d&b": "Drum & Bass",
        "drum and bass": "Drum & Bass",
        "d & b": "Drum & Bass",
        "d n b": "Drum & Bass",
        "Dubstep": "Dubstep/140",
        "140": "Dubstep/140",
    }

    # Add genre to DJ, option to add multiple genres, checks if genre exists in db to avoid adding duplicates but can still add to DJ
    while True:
        genre_title = input(f"Enter a genre of music that {name} plays: ").title()
        if check_quit(genre_title):
            session.rollback()
            return
        elif not genre_title.strip():
            error_message("Genre cannot be blank. Please enter a valid genre.")
            time.sleep(1)
            clear_prev_two_line()
            continue

        mapped_genre_title = genre_mapping.get(genre_title.lower(), genre_title)
        genre = session.query(Genre).filter(func.lower(Genre.title) == mapped_genre_title.lower()).first()
        if genre is None:
            genre = Genre(title=mapped_genre_title)
            session.add(genre)
        elif genre not in new_dj.genres:
            new_dj.genres.append(genre)

        # Add subgenres
        while True:
            clear_prev_line()
            subgenre_title = input(f"Enter Subgenre of {mapped_genre_title} that {name} plays: ").title()
            if check_quit(subgenre_title):
                    session.rollback()
                    return
            elif not subgenre_title.strip():
                error_message("Subgenre cannot be blank. Please enter a valid subgenre.")
                time.sleep(1)
                clear_prev_line()
                continue
                
            mapped_subgenre_title = genre_mapping.get(subgenre_title.lower(), subgenre_title)
            subgenre = session.query(Subgenre).filter(func.lower(Subgenre.subtitle) == mapped_subgenre_title.lower(), Subgenre.genre_id == genre.id).first()
            if not subgenre:
                subgenre = Subgenre(subtitle=mapped_subgenre_title, genre=genre)
                session.add(subgenre)
            if subgenre not in genre.subgenres:
                genre.subgenres.append(subgenre)
            if subgenre not in new_dj.subgenres:
                new_dj.subgenres.append(subgenre)

            while True:
                clear_prev_line()
                add_another_subgenre = input(f"Do you want to add another subgenre of {mapped_genre_title} that {name} plays? (yes/no): ").lower()
                if check_quit(add_another_subgenre):
                    session.rollback()
                    return
                elif add_another_subgenre in ["yes", "y", "ys"]:
                    break
                elif add_another_subgenre in ["no", "n"]:
                    break
                else:
                    error_message("Invalid input, please enter Yes/Y or No/N")
                    time.sleep(1)
                    clear_prev_line()

            if add_another_subgenre in ["no", "n"]:
                break

        # Once all subgenres for this genre have been added, ask if the user wants to add another genre
        while True:
            clear_prev_line()
            add_another_genre = input(f"Do you want to add another genre that {name} plays? (yes/no): ").lower()
            if check_quit(add_another_genre):
                session.rollback()
                return
            elif add_another_genre in ["yes", "y", "ys"]:
                clear_prev_line()
                break
            elif add_another_genre in ["no", "n"]:
                clear_prev_line()
                break
            else:
                error_message("Invalid input, please enter Yes/Y or No/N")
                time.sleep(1)
                clear_prev_line()

        if add_another_genre in ["no", "n"]:
            break


    # Add venue(s) that DJ has played at
    while True:
        venue_name = input(f"Enter a venue where the {name} has played: ").title()
        if check_quit(venue_name):
            session.rollback()
            return
        elif venue_name.strip() == "":
            error_message("Venue name cannot be blank.")
            time.sleep(1)
            clear_prev_two_line()
            continue
        
        venue = session.query(Venue).filter(func.lower(Venue.venuename) == venue_name.lower()).first()
        if venue is None:
            venue = Venue(venuename=venue_name)
            session.add(venue)
        elif venue not in new_dj.venues:
            new_dj.venues.append(venue)

        while True:
            clear_prev_line()
            add_another_venue = input(f"Do you want to add another venue for {name}? (yes/no): ").lower()
            if check_quit(add_another_venue):
                session.rollback()
                return
            elif add_another_venue in ["yes", "y", "ys"]:
                clear_prev_line()
                break
            elif add_another_venue in ["no", "n"]:
                clear_prev_line()
                break
            else:
                error_message("Invalid input, please enter Yes/Y or No/N")
                time.sleep(1)
                clear_prev_line()

        if add_another_venue in ["no", "n"]:
            break

    success_message(f"{name} added successfully.")
    time.sleep(1)
    session.commit()

