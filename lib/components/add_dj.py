from sqlalchemy import func
from models import Dj, Genre, Subgenre, Venue
from env import session, os

# Function to add a DJ
def add_dj():
    while True:
        name = input("Enter DJ name: ")
        if not name.strip():
            print("Name cannot be blank. Please enter a valid name.")
            continue
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
        if not genre_title.strip():
            print("Genre cannot be blank. Please enter a valid genre.")
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
            if not genre_title.strip():
                print("Subgenre cannot be blank. Please enter a valid subgenre.")
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
